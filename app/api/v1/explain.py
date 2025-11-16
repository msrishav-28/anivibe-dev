"""
Explainability API endpoints
Provide explanations for recommendations
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional, Dict, Any

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.services.explainability import explain_recommendation

router = APIRouter()


class ExplanationRequest(BaseModel):
    """Request for recommendation explanation"""
    anime_id: int
    recommendation_method: str
    context: Optional[Dict[str, Any]] = {}


class ExplanationResponse(BaseModel):
    """Explanation response"""
    anime_id: int
    method: str
    natural_language: str
    factors: list
    confidence: Optional[float] = None


@router.post("/recommendation", response_model=ExplanationResponse)
async def explain_recommendation_endpoint(
    request: ExplanationRequest,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get explanation for a recommendation
    
    Explains why a specific anime was recommended using the given method
    """
    try:
        explanation = explain_recommendation(
            anime_id=request.anime_id,
            recommendation_method=request.recommendation_method,
            context=request.context
        )
        
        return explanation
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate explanation: {str(e)}"
        )


@router.get("/anime/{anime_id}/why-recommended")
async def why_recommended(
    anime_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Explain why this anime might be recommended to the user
    
    Analyzes user profile and anime features to explain potential match
    """
    from sqlalchemy import select
    from app.models.anime import Anime
    from app.models.rating import Rating
    
    # Get anime
    result = await db.execute(select(Anime).filter(Anime.id == anime_id))
    anime = result.scalar_one_or_none()
    
    if not anime:
        raise HTTPException(status_code=404, detail="Anime not found")
    
    # Get user's ratings for analysis
    ratings_result = await db.execute(
        select(Rating).filter(Rating.user_id == current_user.id).limit(10)
    )
    user_ratings = ratings_result.scalars().all()
    
    # Build context
    user_preferences = {
        "average_rating": sum(r.score for r in user_ratings) / len(user_ratings) if user_ratings else 0,
        "favorite_genres": [],  # Could be computed from ratings
        "favorite_studios": []
    }
    
    anime_features = {
        "genres": [g.name for g in anime.genres],
        "studios": [s.name for s in anime.studios],
        "tags": [t.name for t in anime.tags],
        "score": anime.score
    }
    
    explanation = explain_recommendation(
        anime_id=anime_id,
        recommendation_method="content",
        context={
            "anime_features": anime_features,
            "user_preferences": user_preferences
        }
    )
    
    return explanation


@router.get("/methods")
async def list_explanation_methods():
    """
    List available explanation methods
    
    Returns information about different recommendation methods
    """
    return {
        "methods": [
            {
                "name": "collaborative",
                "description": "Based on similar users who enjoyed this anime",
                "factors": ["user_similarity", "rating_patterns", "viewing_history"]
            },
            {
                "name": "content",
                "description": "Based on anime features matching your preferences",
                "factors": ["genre_match", "studio_match", "tag_match", "score_match"]
            },
            {
                "name": "semantic",
                "description": "Based on natural language understanding of your query",
                "factors": ["visual_aesthetic", "text_semantic", "emotional_tone"]
            },
            {
                "name": "hybrid",
                "description": "Combines multiple recommendation methods",
                "factors": ["collaborative_score", "content_score", "confidence"]
            },
            {
                "name": "gnn",
                "description": "Based on graph neural network analysis",
                "factors": ["graph_proximity", "network_effects"]
            },
            {
                "name": "bert4rec",
                "description": "Based on sequential viewing patterns",
                "factors": ["sequence_similarity", "temporal_patterns"]
            }
        ]
    }
