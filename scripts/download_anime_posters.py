"""
Download anime poster images for CLIP processing
"""
import asyncio
import aiohttp
import logging
from pathlib import Path
from typing import List
import sys
from PIL import Image
from io import BytesIO

sys.path.insert(0, str(Path(__file__).parents[1]))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.anime import Anime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

POSTERS_DIR = Path("data/posters")
POSTERS_DIR.mkdir(parents=True, exist_ok=True)


async def download_poster(session: aiohttp.ClientSession, anime_id: int, image_url: str) -> bool:
    """Download and save anime poster"""
    try:
        output_path = POSTERS_DIR / f"{anime_id}.jpg"
        
        # Skip if already exists
        if output_path.exists():
            return True
        
        async with session.get(image_url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            if response.status == 200:
                image_data = await response.read()
                
                # Verify it's a valid image
                try:
                    img = Image.open(BytesIO(image_data))
                    # Convert to RGB if needed
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    # Resize to consistent size (224x224 for CLIP)
                    img = img.resize((224, 224), Image.Resampling.LANCZOS)
                    # Save as JPEG
                    img.save(output_path, 'JPEG', quality=95)
                    return True
                except Exception as e:
                    logger.error(f"Invalid image for anime {anime_id}: {e}")
                    return False
            else:
                logger.warning(f"Failed to download {anime_id}: {response.status}")
                return False
    
    except Exception as e:
        logger.error(f"Error downloading anime {anime_id}: {e}")
        return False


async def download_all_posters(limit: int = None):
    """Download posters for all anime in database"""
    logger.info("Starting poster download...")
    
    async with AsyncSessionLocal() as db_session:
        # Get all anime with image URLs
        query = select(Anime).filter(Anime.image_url.isnot(None))
        
        if limit:
            query = query.limit(limit)
        
        result = await db_session.execute(query)
        anime_list = result.scalars().all()
        
        logger.info(f"Found {len(anime_list)} anime with images")
        
        # Download concurrently
        async with aiohttp.ClientSession() as session:
            downloaded = 0
            failed = 0
            
            for idx, anime in enumerate(anime_list, 1):
                success = await download_poster(session, anime.id, anime.image_url)
                
                if success:
                    downloaded += 1
                else:
                    failed += 1
                
                if idx % 50 == 0:
                    logger.info(f"Progress: {idx}/{len(anime_list)} - Downloaded: {downloaded}, Failed: {failed}")
                
                # Rate limiting
                await asyncio.sleep(0.1)
            
            logger.info(f"✅ Download complete! Downloaded: {downloaded}, Failed: {failed}")


async def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Download anime posters")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of posters")
    args = parser.parse_args()
    
    await download_all_posters(limit=args.limit)


if __name__ == "__main__":
    asyncio.run(main())
