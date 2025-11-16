"""
Content-based filtering using anime features
"""
import logging
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from app.models.anime import Anime

logger = logging.getLogger(__name__)


async def get_content_based_recommendations(
    user_ratings: Dict[int, float],
    top_k: int = 20,
    db: AsyncSession = None
) -> Dict[int, float]:
    """
    Get content-based recommendations using anime features
    
    Args:
        user_ratings: Dictionary of anime_id -> score
        top_k: Number of recommendations
        db: Database session
    
    Returns:
        Dictionary mapping anime_id to recommendation score
    """
    if not user_ratings:
        return {}
    
    try:
        # Get all anime with features
        result = await db.execute(
            select(Anime)
            .options(
                selectinload(Anime.genres),
                selectinload(Anime.studios),
                selectinload(Anime.tags)
            )
        )
        all_anime = result.scalars().all()
        
        if not all_anime:
            return {}
        
        # Build feature vectors
        # Collect all unique features
        all_genres = set()
        all_studios = set()
        all_tags = set()
        
        for anime in all_anime:
            all_genres.update(g.name for g in anime.genres)
            all_studios.update(s.name for s in anime.studios)
            all_tags.update(t.name for t in anime.tags)
        
        genre_list = sorted(list(all_genres))
        studio_list = sorted(list(all_studios))
        tag_list = sorted(list(all_tags))
        
        genre_to_idx = {g: idx for idx, g in enumerate(genre_list)}
        studio_to_idx = {s: idx for idx, s in enumerate(studio_list)}
        tag_to_idx = {t: idx for idx, t in enumerate(tag_list)}
        
        # Create feature matrix
        feature_dim = len(genre_list) + len(studio_list) + len(tag_list) + 2  # +2 for score and year
        feature_matrix = np.zeros((len(all_anime), feature_dim))
        anime_id_to_idx = {}
        
        for idx, anime in enumerate(all_anime):
            anime_id_to_idx[anime.id] = idx
            
            # Genre features
            for genre in anime.genres:
                genre_idx = genre_to_idx[genre.name]
                feature_matrix[idx, genre_idx] = 1.0
            
            # Studio features
            for studio in anime.studios:
                studio_idx = studio_to_idx[studio.name]
                feature_matrix[idx, len(genre_list) + studio_idx] = 1.0
            
            # Tag features
            for tag in anime.tags:
                tag_idx = tag_to_idx[tag.name]
                feature_matrix[idx, len(genre_list) + len(studio_list) + tag_idx] = 1.0
            
            # Score feature (normalized)
            if anime.score:
                feature_matrix[idx, -2] = anime.score / 10.0
            
            # Year feature (normalized)
            if anime.year:
                feature_matrix[idx, -1] = (anime.year - 1960) / (2024 - 1960)
        
        # Build user profile from rated anime
        user_profile = np.zeros(feature_dim)
        total_weight = 0
        
        for anime_id, score in user_ratings.items():
            if anime_id in anime_id_to_idx:
                anime_idx = anime_id_to_idx[anime_id]
                weight = score / 10.0  # Normalize score to 0-1
                user_profile += feature_matrix[anime_idx] * weight
                total_weight += weight
        
        if total_weight > 0:
            user_profile /= total_weight
        
        # Calculate similarity with all anime
        user_profile = user_profile.reshape(1, -1)
        similarities = cosine_similarity(user_profile, feature_matrix)[0]
        
        # Create recommendations (exclude already rated)
        recommendations = {}
        
        for anime_id, anime_idx in anime_id_to_idx.items():
            if anime_id not in user_ratings:
                recommendations[anime_id] = float(similarities[anime_idx])
        
        return recommendations
        
    except Exception as e:
        logger.error(f"Content-based filtering failed: {e}")
        return {}
