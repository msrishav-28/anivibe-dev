"""
Recommendation endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationBatchResponse,
    SimilarAnimeRequest,
    HiddenGemRequest,
    MoodBasedRequest,
    TasteProfileResponse
)
from app.services.recommendations import (
    get_personalized_recommendations,
    get_similar_anime,
    discover_hidden_gems,
    get_mood_based_recommendations,
    get_user_taste_profile
)

router = APIRouter()


@router.post("/personalized", response_model=RecommendationBatchResponse)
async def personalized_recommendations(
    request: RecommendationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get personalized recommendations for current user
    Uses hybrid system: collaborative filtering + content-based + GNN
    """
    try:
        results = await get_personalized_recommendations(
            user_id=current_user.id,
            top_k=request.top_k,
            method=request.method,
            filters=request.filters,
            exclude_watched=request.exclude_watched,
            popularity_attenuation=request.popularity_attenuation,
            diversity_weight=request.diversity_weight,
            db=db
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation generation failed: {str(e)}"
        )


@router.post("/similar", response_model=RecommendationBatchResponse)
async def similar_anime(
    request: SimilarAnimeRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Find anime similar to a given anime
    Uses multimodal features (CLIP + BERT + metadata)
    """
    try:
        results = await get_similar_anime(
            anime_id=request.anime_id,
            top_k=request.top_k,
            method=request.method,
            db=db
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Similar anime search failed: {str(e)}"
        )


@router.post("/hidden-gems", response_model=RecommendationBatchResponse)
async def hidden_gems(
    request: HiddenGemRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Discover hidden gem anime
    High-quality, low-popularity titles
    """
    try:
        results = await discover_hidden_gems(
            user_id=request.user_id,
            top_k=request.top_k,
            max_popularity=request.max_popularity,
            min_score=request.min_score,
            genres=request.genres,
            tags=request.tags,
            db=db
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Hidden gem discovery failed: {str(e)}"
        )


@router.post("/mood-based", response_model=RecommendationBatchResponse)
async def mood_based_recommendations(
    request: MoodBasedRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Get recommendations based on mood/emotional state
    Uses sentiment analysis and LLM parsing
    """
    try:
        results = await get_mood_based_recommendations(
            mood=request.mood,
            top_k=request.top_k,
            user_id=request.user_id,
            db=db
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Mood-based recommendations failed: {str(e)}"
        )


@router.get("/taste-profile", response_model=TasteProfileResponse)
async def taste_profile(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get user's taste profile
    Analyzes rating patterns, genres, studios, etc.
    """
    try:
        profile = await get_user_taste_profile(
            user_id=current_user.id,
            db=db
        )
        
        return profile
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Taste profile generation failed: {str(e)}"
        )


@router.get("/cold-start")
async def cold_start_recommendations(
    top_k: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Get recommendations for new users (cold start)
    Returns popular, highly-rated anime across diverse genres
    """
    from sqlalchemy import select, func
    from sqlalchemy.orm import selectinload
    from app.models.anime import Anime
    import random
    
    # Get top-rated anime with diverse genres
    result = await db.execute(
        select(Anime)
        .options(
            selectinload(Anime.genres),
            selectinload(Anime.studios),
            selectinload(Anime.tags)
        )
        .filter(
            Anime.score >= 8.0,
            Anime.scored_by >= 10000
        )
        .order_by(func.random())
        .limit(top_k * 2)
    )
    
    anime_list = result.scalars().all()
    
    # Diversify by genres
    selected = []
    seen_genres = set()
    
    for anime in anime_list:
        anime_genres = {g.name for g in anime.genres}
        if not seen_genres or len(anime_genres & seen_genres) < 2:
            selected.append(anime)
            seen_genres.update(anime_genres)
            if len(selected) >= top_k:
                break
    
    # Fill remaining with random picks
    if len(selected) < top_k:
        remaining = [a for a in anime_list if a not in selected]
        selected.extend(remaining[:top_k - len(selected)])
    
    recommendations = []
    for i, anime in enumerate(selected, 1):
        recommendations.append({
            "anime_id": anime.id,
            "anime": anime.to_dict(include_relationships=True),
            "score": anime.score or 0.0,
            "rank": i,
            "explanation": None,
            "similarity_reasons": ["Popular and highly-rated", "Diverse genre selection"]
        })
    
    return {
        "recommendations": recommendations,
        "total": len(recommendations),
        "method": "cold_start",
        "user_id": None,
        "execution_time_ms": 0.0
    }
