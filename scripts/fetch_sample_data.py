"""
Fetch sample anime data from Jikan API (MyAnimeList)
"""
import asyncio
import aiohttp
import json
from pathlib import Path
import logging
from typing import List, Dict
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Jikan API base URL
JIKAN_BASE_URL = "https://api.jikan.moe/v4"

# Output directory
DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


async def fetch_top_anime(session: aiohttp.ClientSession, limit: int = 100) -> List[Dict]:
    """
    Fetch top anime from Jikan API
    
    Args:
        session: aiohttp session
        limit: Number of anime to fetch
    
    Returns:
        List of anime dictionaries
    """
    anime_list = []
    page = 1
    
    while len(anime_list) < limit:
        url = f"{JIKAN_BASE_URL}/top/anime"
        params = {"page": page, "limit": 25}
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    anime_data = data.get("data", [])
                    
                    if not anime_data:
                        break
                    
                    anime_list.extend(anime_data)
                    logger.info(f"Fetched page {page}, total anime: {len(anime_list)}")
                    
                    page += 1
                    
                    # Rate limiting (3 requests per second)
                    await asyncio.sleep(0.4)
                else:
                    logger.error(f"Error fetching page {page}: {response.status}")
                    break
                    
        except Exception as e:
            logger.error(f"Exception fetching page {page}: {e}")
            break
    
    return anime_list[:limit]


async def fetch_anime_genres(session: aiohttp.ClientSession) -> List[Dict]:
    """Fetch all anime genres"""
    url = f"{JIKAN_BASE_URL}/genres/anime"
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("data", [])
    except Exception as e:
        logger.error(f"Error fetching genres: {e}")
    
    return []


async def fetch_anime_details(session: aiohttp.ClientSession, anime_id: int) -> Dict:
    """Fetch detailed information for a specific anime"""
    url = f"{JIKAN_BASE_URL}/anime/{anime_id}/full"
    
    try:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data.get("data", {})
            await asyncio.sleep(0.4)  # Rate limiting
    except Exception as e:
        logger.error(f"Error fetching anime {anime_id}: {e}")
    
    return {}


def transform_anime_data(raw_anime: Dict) -> Dict:
    """Transform Jikan API data to our schema"""
    return {
        "mal_id": raw_anime.get("mal_id"),
        "title": raw_anime.get("title"),
        "title_english": raw_anime.get("title_english"),
        "title_japanese": raw_anime.get("title_japanese"),
        "title_synonyms": raw_anime.get("title_synonyms", []),
        "synopsis": raw_anime.get("synopsis"),
        "image_url": raw_anime.get("images", {}).get("jpg", {}).get("large_image_url"),
        "trailer_url": raw_anime.get("trailer", {}).get("url"),
        "type": raw_anime.get("type"),
        "status": raw_anime.get("status"),
        "episodes": raw_anime.get("episodes"),
        "duration": raw_anime.get("duration"),
        "aired_from": raw_anime.get("aired", {}).get("from"),
        "aired_to": raw_anime.get("aired", {}).get("to"),
        "season": raw_anime.get("season"),
        "year": raw_anime.get("year"),
        "score": raw_anime.get("score"),
        "scored_by": raw_anime.get("scored_by"),
        "rank": raw_anime.get("rank"),
        "popularity": raw_anime.get("popularity"),
        "members": raw_anime.get("members"),
        "favorites": raw_anime.get("favorites"),
        "rating": raw_anime.get("rating"),
        "source": raw_anime.get("source"),
        "genres": [g["name"] for g in raw_anime.get("genres", [])],
        "studios": [s["name"] for s in raw_anime.get("studios", [])],
        "themes": [t["name"] for t in raw_anime.get("themes", [])],
        "demographics": [d["name"] for d in raw_anime.get("demographics", [])]
    }


async def main():
    """Main function"""
    logger.info("Starting data fetch from Jikan API...")
    
    async with aiohttp.ClientSession() as session:
        # Fetch genres
        logger.info("Fetching genres...")
        genres = await fetch_anime_genres(session)
        
        genres_file = DATA_DIR / "genres.json"
        with open(genres_file, 'w', encoding='utf-8') as f:
            json.dump(genres, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved {len(genres)} genres to {genres_file}")
        
        # Fetch top anime
        logger.info("Fetching top 100 anime...")
        anime_list = await fetch_top_anime(session, limit=100)
        
        # Transform data
        transformed_anime = [transform_anime_data(anime) for anime in anime_list]
        
        # Save to file
        anime_file = DATA_DIR / "anime_sample.json"
        with open(anime_file, 'w', encoding='utf-8') as f:
            json.dump(transformed_anime, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved {len(transformed_anime)} anime to {anime_file}")
        
        # Also save as CSV for easy import
        import pandas as pd
        
        df = pd.json_normalize(transformed_anime)
        csv_file = DATA_DIR / "anime_sample.csv"
        df.to_csv(csv_file, index=False)
        
        logger.info(f"✅ Saved CSV to {csv_file}")
        logger.info("✅ Data fetch complete!")


if __name__ == "__main__":
    asyncio.run(main())
