"""
Fetch complete anime dataset from MyAnimeList via Jikan API
Handles pagination, rate limiting, and data persistence
"""
import asyncio
import aiohttp
import json
import logging
from pathlib import Path
from typing import List, Dict, Optional
import time
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.anime import Anime, Genre, Studio, AnimeType, AnimeStatus, AnimeSeason
from app.models.anime import anime_genres, anime_studios

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

JIKAN_BASE_URL = "https://api.jikan.moe/v4"
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


class MALDataFetcher:
    """Fetches anime data from MyAnimeList via Jikan API"""
    
    def __init__(self, limit: Optional[int] = None):
        self.limit = limit
        self.session: Optional[aiohttp.ClientSession] = None
        self.anime_data: List[Dict] = []
        self.genres_map: Dict[int, str] = {}
        self.studios_map: Dict[int, str] = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def fetch_with_retry(self, url: str, params: dict = None, max_retries: int = 3) -> Optional[Dict]:
        """Fetch with exponential backoff retry"""
        for attempt in range(max_retries):
            try:
                await asyncio.sleep(0.4)  # Rate limiting: 3 req/sec
                
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    elif response.status == 429:  # Rate limited
                        wait_time = 2 ** attempt
                        logger.warning(f"Rate limited. Waiting {wait_time}s...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"Error {response.status}: {url}")
                        return None
            except Exception as e:
                logger.error(f"Exception on attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2 ** attempt)
        
        return None
    
    async def fetch_genres(self):
        """Fetch all anime genres"""
        logger.info("Fetching genres...")
        url = f"{JIKAN_BASE_URL}/genres/anime"
        data = await self.fetch_with_retry(url)
        
        if data and "data" in data:
            self.genres_map = {g["mal_id"]: g["name"] for g in data["data"]}
            logger.info(f"✅ Fetched {len(self.genres_map)} genres")
            
            # Save to file
            with open(DATA_DIR / "genres.json", 'w', encoding='utf-8') as f:
                json.dump(data["data"], f, indent=2, ensure_ascii=False)
    
    async def fetch_all_anime(self):
        """Fetch all anime with pagination"""
        logger.info(f"Fetching anime (limit: {self.limit or 'all'})...")
        
        page = 1
        has_next = True
        
        while has_next:
            if self.limit and len(self.anime_data) >= self.limit:
                break
            
            url = f"{JIKAN_BASE_URL}/anime"
            params = {
                "page": page,
                "limit": 25,
                "order_by": "members",
                "sort": "desc"
            }
            
            data = await self.fetch_with_retry(url, params)
            
            if not data or "data" not in data:
                break
            
            anime_list = data["data"]
            if not anime_list:
                break
            
            self.anime_data.extend(anime_list)
            logger.info(f"Page {page}: {len(anime_list)} anime, Total: {len(self.anime_data)}")
            
            has_next = data.get("pagination", {}).get("has_next_page", False)
            page += 1
            
            # Save progress periodically
            if page % 10 == 0:
                self.save_progress()
        
        logger.info(f"✅ Fetched {len(self.anime_data)} anime total")
    
    async def enrich_anime_details(self):
        """Fetch detailed information for each anime"""
        logger.info("Enriching anime with full details...")
        
        enriched_data = []
        
        for idx, anime in enumerate(self.anime_data, 1):
            mal_id = anime.get("mal_id")
            
            # Fetch full details
            url = f"{JIKAN_BASE_URL}/anime/{mal_id}/full"
            full_data = await self.fetch_with_retry(url)
            
            if full_data and "data" in full_data:
                enriched_data.append(full_data["data"])
            else:
                enriched_data.append(anime)
            
            if idx % 10 == 0:
                logger.info(f"Enriched {idx}/{len(self.anime_data)}")
        
        self.anime_data = enriched_data
        logger.info("✅ Enrichment complete")
    
    def save_progress(self):
        """Save current progress to file"""
        filepath = DATA_DIR / f"anime_progress_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.anime_data, f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Progress saved: {filepath}")
    
    def save_final_data(self):
        """Save final dataset"""
        # Save JSON
        json_file = DATA_DIR / "anime_full.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.anime_data, f, indent=2, ensure_ascii=False)
        logger.info(f"✅ Saved JSON: {json_file}")
        
        # Save CSV
        import pandas as pd
        df = pd.json_normalize(self.anime_data)
        csv_file = DATA_DIR / "anime_full.csv"
        df.to_csv(csv_file, index=False)
        logger.info(f"✅ Saved CSV: {csv_file}")


async def import_to_database(anime_data: List[Dict]):
    """Import anime data to PostgreSQL database"""
    logger.info("Importing to database...")
    
    async with AsyncSessionLocal() as session:
        # Import genres first
        logger.info("Importing genres...")
        genres_file = DATA_DIR / "genres.json"
        if genres_file.exists():
            with open(genres_file, 'r', encoding='utf-8') as f:
                genres_data = json.load(f)
            
            for genre_data in genres_data:
                result = await session.execute(
                    select(Genre).filter(Genre.mal_id == genre_data["mal_id"])
                )
                if not result.scalar_one_or_none():
                    genre = Genre(
                        name=genre_data["name"],
                        mal_id=genre_data["mal_id"]
                    )
                    session.add(genre)
            
            await session.commit()
            logger.info("✅ Genres imported")
        
        # Import anime
        logger.info("Importing anime...")
        imported_count = 0
        
        for anime_data_item in anime_data:
            try:
                mal_id = anime_data_item.get("mal_id")
                
                # Check if exists
                result = await session.execute(
                    select(Anime).filter(Anime.mal_id == mal_id)
                )
                if result.scalar_one_or_none():
                    continue
                
                # Parse aired dates
                aired_from = None
                aired_to = None
                aired = anime_data_item.get("aired", {})
                if aired.get("from"):
                    aired_from = datetime.fromisoformat(aired["from"].replace("Z", "+00:00"))
                if aired.get("to"):
                    aired_to = datetime.fromisoformat(aired["to"].replace("Z", "+00:00"))
                
                # Parse type and status
                anime_type = None
                if anime_data_item.get("type"):
                    try:
                        anime_type = AnimeType(anime_data_item["type"])
                    except ValueError:
                        pass
                
                anime_status = None
                if anime_data_item.get("status"):
                    try:
                        anime_status = AnimeStatus(anime_data_item["status"])
                    except ValueError:
                        pass
                
                # Parse season
                season = None
                if anime_data_item.get("season"):
                    try:
                        season = AnimeSeason(anime_data_item["season"].capitalize())
                    except ValueError:
                        pass
                
                # Create anime
                anime = Anime(
                    mal_id=mal_id,
                    title=anime_data_item.get("title", ""),
                    title_english=anime_data_item.get("title_english"),
                    title_japanese=anime_data_item.get("title_japanese"),
                    title_synonyms=json.dumps(anime_data_item.get("title_synonyms", [])),
                    synopsis=anime_data_item.get("synopsis"),
                    background=anime_data_item.get("background"),
                    image_url=anime_data_item.get("images", {}).get("jpg", {}).get("large_image_url"),
                    trailer_url=anime_data_item.get("trailer", {}).get("url"),
                    type=anime_type,
                    status=anime_status,
                    episodes=anime_data_item.get("episodes"),
                    duration_minutes=parse_duration(anime_data_item.get("duration")),
                    aired_from=aired_from,
                    aired_to=aired_to,
                    season=season,
                    year=anime_data_item.get("year"),
                    score=anime_data_item.get("score"),
                    scored_by=anime_data_item.get("scored_by"),
                    rank=anime_data_item.get("rank"),
                    popularity=anime_data_item.get("popularity"),
                    members=anime_data_item.get("members"),
                    favorites=anime_data_item.get("favorites"),
                    rating=anime_data_item.get("rating"),
                    source=anime_data_item.get("source")
                )
                
                session.add(anime)
                await session.flush()
                
                # Add genres
                for genre_data in anime_data_item.get("genres", []):
                    result = await session.execute(
                        select(Genre).filter(Genre.mal_id == genre_data["mal_id"])
                    )
                    genre = result.scalar_one_or_none()
                    if genre:
                        anime.genres.append(genre)
                
                # Add studios
                for studio_data in anime_data_item.get("studios", []):
                    result = await session.execute(
                        select(Studio).filter(Studio.name == studio_data["name"])
                    )
                    studio = result.scalar_one_or_none()
                    
                    if not studio:
                        studio = Studio(
                            name=studio_data["name"],
                            mal_id=studio_data.get("mal_id")
                        )
                        session.add(studio)
                        await session.flush()
                    
                    anime.studios.append(studio)
                
                imported_count += 1
                
                if imported_count % 100 == 0:
                    await session.commit()
                    logger.info(f"Imported {imported_count} anime...")
            
            except Exception as e:
                logger.error(f"Error importing anime {anime_data_item.get('mal_id')}: {e}")
                continue
        
        await session.commit()
        logger.info(f"✅ Imported {imported_count} anime to database")


def parse_duration(duration_str: Optional[str]) -> Optional[int]:
    """Parse duration string to minutes"""
    if not duration_str:
        return None
    
    try:
        # Examples: "24 min per ep", "1 hr 30 min", "2 hr"
        minutes = 0
        if "hr" in duration_str:
            hours = int(duration_str.split("hr")[0].strip())
            minutes += hours * 60
        if "min" in duration_str:
            mins = int(duration_str.split("min")[0].split()[-1])
            minutes += mins
        return minutes if minutes > 0 else None
    except:
        return None


async def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch MAL anime data")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of anime to fetch")
    parser.add_argument("--enrich", action="store_true", help="Fetch full details for each anime")
    parser.add_argument("--import-db", action="store_true", help="Import to database")
    args = parser.parse_args()
    
    start_time = time.time()
    
    async with MALDataFetcher(limit=args.limit) as fetcher:
        # Fetch genres
        await fetcher.fetch_genres()
        
        # Fetch all anime
        await fetcher.fetch_all_anime()
        
        # Enrich if requested
        if args.enrich:
            await fetcher.enrich_anime_details()
        
        # Save data
        fetcher.save_final_data()
        
        # Import to database if requested
        if args.import_db:
            await import_to_database(fetcher.anime_data)
    
    elapsed = time.time() - start_time
    logger.info(f"✅ Complete! Time: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
