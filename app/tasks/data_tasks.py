"""
Background tasks for data processing and synchronization
"""
from celery import Task
from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)


@celery_app.task
def sync_mal_data_task(limit: int = None):
    """
    Sync anime data from MyAnimeList
    
    Args:
        limit: Maximum number of anime to fetch
    
    Returns:
        Number of anime synced
    """
    import asyncio
    import sys
    from pathlib import Path
    
    sys.path.insert(0, str(Path(__file__).parents[2]))
    
    logger.info("Syncing MAL data...")
    
    from scripts.fetch_mal_data import MALDataFetcher, import_to_database
    
    async def _sync():
        async with MALDataFetcher(limit=limit) as fetcher:
            await fetcher.fetch_genres()
            await fetcher.fetch_all_anime()
            fetcher.save_final_data()
            await import_to_database(fetcher.anime_data)
            return len(fetcher.anime_data)
    
    count = asyncio.run(_sync())
    logger.info(f"✅ Synced {count} anime from MAL")
    return count


@celery_app.task
def download_posters_task(limit: int = None):
    """
    Download anime posters
    
    Args:
        limit: Maximum number of posters to download
    
    Returns:
        Number of posters downloaded
    """
    import asyncio
    import sys
    from pathlib import Path
    
    sys.path.insert(0, str(Path(__file__).parents[2]))
    
    logger.info("Downloading anime posters...")
    
    from scripts.download_anime_posters import download_all_posters
    
    asyncio.run(download_all_posters(limit=limit))
    
    return "Posters downloaded"


@celery_app.task
def cleanup_old_cache_task():
    """
    Clean up old cached data
    
    Returns:
        Status message
    """
    import asyncio
    from app.core.cache import redis_client
    
    logger.info("Cleaning up old cache...")
    
    async def _cleanup():
        # Delete old recommendation caches (older than 24 hours)
        pattern = "recommendations:*"
        deleted = 0
        
        async for key in redis_client.scan_iter(match=pattern):
            ttl = await redis_client.ttl(key)
            if ttl < 0 or ttl > 86400:  # No TTL or > 24 hours
                await redis_client.delete(key)
                deleted += 1
        
        return deleted
    
    deleted = asyncio.run(_cleanup())
    logger.info(f"✅ Deleted {deleted} old cache entries")
    return f"Deleted {deleted} entries"


@celery_app.task
def update_anime_statistics_task():
    """
    Update computed statistics for anime
    
    Returns:
        Status message
    """
    import asyncio
    from app.core.database import AsyncSessionLocal
    from app.models.anime import Anime
    from app.models.rating import Rating
    from sqlalchemy import select, func
    
    logger.info("Updating anime statistics...")
    
    async def _update_stats():
        async with AsyncSessionLocal() as session:
            # Get all anime
            result = await session.execute(select(Anime))
            anime_list = result.scalars().all()
            
            updated = 0
            for anime in anime_list:
                # Calculate popularity score
                members = anime.members or 0
                score = anime.score or 0
                
                # Logarithmic popularity dampening
                import math
                if members > 0:
                    popularity_score = score * (1 - 0.3 * math.log10(members) / 6)
                    anime.popularity_score = max(popularity_score, 0)
                    updated += 1
            
            await session.commit()
            return updated
    
    updated = asyncio.run(_update_stats())
    logger.info(f"✅ Updated {updated} anime statistics")
    return f"Updated {updated} anime"
