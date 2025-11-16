"""
Background tasks for recommendation precomputation
"""
from celery import Task
from app.tasks.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def precompute_recommendations_for_user(self, user_id: int):
    """
    Precompute and cache recommendations for a user
    
    Args:
        user_id: User ID
    
    Returns:
        Number of recommendations cached
    """
    import asyncio
    from app.services.recommendations import get_personalized_recommendations
    from app.core.database import AsyncSessionLocal
    
    logger.info(f"Precomputing recommendations for user {user_id}...")
    
    async def _compute():
        async with AsyncSessionLocal() as session:
            try:
                result = await get_personalized_recommendations(
                    user_id=user_id,
                    top_k=50,  # Cache top 50
                    method="hybrid",
                    db=session
                )
                return len(result.get("recommendations", []))
            except Exception as e:
                logger.error(f"Error computing recommendations: {e}")
                return 0
    
    count = asyncio.run(_compute())
    logger.info(f"✅ Cached {count} recommendations for user {user_id}")
    return count


@celery_app.task
def precompute_all_user_recommendations(batch_size: int = 100):
    """
    Precompute recommendations for all active users
    
    Args:
        batch_size: Number of users to process per batch
    
    Returns:
        Number of users processed
    """
    import asyncio
    from app.core.database import AsyncSessionLocal
    from app.models.user import User
    from sqlalchemy import select
    
    logger.info("Precomputing recommendations for all users...")
    
    async def _get_active_users():
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(User.id).filter(User.is_active == True)
            )
            return [row[0] for row in result]
    
    user_ids = asyncio.run(_get_active_users())
    
    logger.info(f"Found {len(user_ids)} active users")
    
    # Queue tasks for each user
    for i in range(0, len(user_ids), batch_size):
        batch = user_ids[i:i+batch_size]
        for user_id in batch:
            precompute_recommendations_for_user.delay(user_id)
    
    return len(user_ids)


@celery_app.task
def compute_anime_similarity_matrix():
    """
    Compute pairwise similarity matrix for all anime
    
    Returns:
        Status message
    """
    import numpy as np
    from pathlib import Path
    
    logger.info("Computing anime similarity matrix...")
    
    embeddings_dir = Path("data/embeddings")
    
    # Load embeddings
    try:
        sbert_embeddings = np.load(embeddings_dir / "sbert_embeddings.npy")
        anime_ids = np.load(embeddings_dir / "sbert_anime_ids.npy")
        
        # Compute cosine similarity matrix
        from sklearn.metrics.pairwise import cosine_similarity
        
        similarity_matrix = cosine_similarity(sbert_embeddings)
        
        # Save matrix
        output_path = embeddings_dir / "anime_similarity_matrix.npy"
        np.save(output_path, similarity_matrix)
        
        # Save anime IDs
        np.save(embeddings_dir / "similarity_anime_ids.npy", anime_ids)
        
        logger.info(f"✅ Computed similarity matrix: {similarity_matrix.shape}")
        return f"Computed {similarity_matrix.shape[0]}x{similarity_matrix.shape[1]} similarity matrix"
        
    except Exception as e:
        logger.error(f"Error computing similarity matrix: {e}")
        raise
