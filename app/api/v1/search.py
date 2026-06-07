"""
Semantic search endpoints
"""
import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.recommendation import SemanticSearchRequest, RecommendationBatchResponse
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

class VisualSearchRequest(BaseModel):
    image_url: str
    top_k: int = Field(10, ge=1, le=50)


async def _record_search_event(db: AsyncSession, **kwargs) -> None:
    """Best-effort search event logging; never block user-facing search."""
    try:
        from app.models.ops import SearchEvent

        db.add(SearchEvent(**kwargs))
        await db.commit()
    except Exception as exc:
        await db.rollback()
        logger.warning("Search event logging failed: %s", exc)

@router.post("/visual", response_model=dict)
async def visual_search(
    request: VisualSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Visual search using image URL or Base64
    """
    if not settings.enable_image_search:
        raise HTTPException(status_code=404, detail="Visual search is disabled until local CLIP evaluation passes")

    from app.services.vector_search import search_by_image
    from app.models.anime import Anime
    from sqlalchemy import select
    
    # 1. Get similar anime IDs from Vector Service
    results = await search_by_image(request.image_url, top_k=request.top_k)
    
    if not results:
        await _record_search_event(
            db,
            query=request.image_url[:500],
            search_type="visual",
            result_ids=[],
            model_name=f"clip-{settings.clip_model_name}-{settings.clip_pretrained}",
            model_version="poster-baseline",
            fallback_used=None,
        )
        return {
            "results": [],
            "model_name": f"clip-{settings.clip_model_name}-{settings.clip_pretrained}",
            "model_version": "poster-baseline",
            "fallback_used": False,
            "score_source": "ml_service",
        }
        
    # 2. Fetch details from DB
    anime_ids = list(results.keys())
    query = select(Anime).filter(Anime.id.in_(anime_ids))
    db_results = await db.execute(query)
    anime_list = db_results.scalars().all()
    
    # 3. Format response
    response_data = []
    for anime in anime_list:
        response_data.append({
            "id": anime.id,
            "title": anime.title,
            "similarity": results.get(anime.id, 0.0),
            "image_url": anime.image_url
        })
        
    # Sort by similarity
    response_data.sort(key=lambda x: x["similarity"], reverse=True)
    await _record_search_event(
        db,
        query=request.image_url[:500],
        search_type="visual",
        result_ids=[item["id"] for item in response_data],
        model_name=f"clip-{settings.clip_model_name}-{settings.clip_pretrained}",
        model_version="poster-baseline",
        fallback_used=None,
    )
    
    return {
        "results": response_data,
        "model_name": f"clip-{settings.clip_model_name}-{settings.clip_pretrained}",
        "model_version": "poster-baseline",
        "fallback_used": False,
        "score_source": "ml_service",
    }


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
        from app.services.semantic_search import semantic_vibe_search

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
        await _record_search_event(
            db,
            query=request.query,
            search_type="semantic",
            result_ids=[item["anime_id"] for item in results.get("recommendations", [])],
            model_name=settings.sbert_model_name,
            model_version="baseline",
            fallback_used="clip_to_sbert" if request.use_clip and not settings.enable_image_search else None,
            latency_ms=results.get("execution_time_ms"),
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
