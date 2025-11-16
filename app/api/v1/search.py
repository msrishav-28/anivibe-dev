"""
Semantic search endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.recommendation import SemanticSearchRequest, RecommendationBatchResponse
from app.services.semantic_search import semantic_vibe_search

router = APIRouter()


@router.post("/semantic", response_model=RecommendationBatchResponse)
async def semantic_search(
    request: SemanticSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Semantic vibe-based search using natural language
    Examples:
    - "anime with rain and pink skies"
    - "melancholic slice of life with beautiful backgrounds"
    - "dark cyberpunk aesthetic with intense action"
    """
    try:
        results = await semantic_vibe_search(
            query=request.query,
            top_k=request.top_k,
            use_clip=request.use_clip,
            use_sbert=request.use_sbert,
            visual_weight=request.visual_weight,
            text_weight=request.text_weight,
            filters=request.filters,
            db=db
        )
        
        return results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Semantic search failed: {str(e)}"
        )


@router.get("/autocomplete")
async def search_autocomplete(
    query: str,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    """
    Autocomplete anime titles
    """
    from sqlalchemy import select, or_
    from app.models.anime import Anime
    
    result = await db.execute(
        select(Anime.id, Anime.title, Anime.title_english, Anime.image_url)
        .filter(
            or_(
                Anime.title.ilike(f"%{query}%"),
                Anime.title_english.ilike(f"%{query}%")
            )
        )
        .limit(limit)
    )
    
    suggestions = []
    for row in result:
        suggestions.append({
            "id": row.id,
            "title": row.title,
            "title_english": row.title_english,
            "image_url": row.image_url
        })
    
    return {"suggestions": suggestions}
