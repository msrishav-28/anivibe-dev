"""
Vector similarity search using Supabase pgvector
Replaces FAISS implementation for production readiness
"""
import logging
import json
import httpx
from typing import Dict, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from config import settings
from app.core.ml_models import encode_text_sbert
from app.models.anime import Anime

logger = logging.getLogger(__name__)


async def search_by_clip(query: str, top_k: int = 10) -> Dict[int, float]:
    """
    Search anime using CLIP embeddings via Modal microservice
    This is for TEXT-TO-IMAGE search (finding anime by visual description)
    
    Args:
        query: Text query
        top_k: Number of results
    
    Returns:
        Dictionary mapping anime_id to similarity score
    """
    if not settings.enable_image_search:
        return {}
        
    # For text-to-image search, we need to embed the text into CLIP space
    # Ideally this runs on Modal too, but we can call the semantic_search endpoint
    # that handles multimodal queries if implemented there.
    
    # Current implementation strategy:
    # 1. We assume the Modal service has a dedicated text-to-image search endpoint
    #    OR we just use SBERT for now as a fallback if Modal isn't set up for text-clip
    
    logger.warning("CLIP text-search via Modal not fully implemented, falling back to SBERT")
    return await search_by_sbert(query, top_k)


async def search_by_image(image_base64: str, top_k: int = 20) -> Dict[int, float]:
    """
    Search anime by Image using Modal microservice (CLIP)
    """
    if not settings.ml_service_url:
        logger.warning("ML Service URL not set")
        return {}
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.ml_service_url}/clip_image_search",
                json={"image_base64": image_base64, "limit": top_k},
                timeout=settings.ml_service_timeout
            )
            
            if response.status_code != 200:
                logger.error(f"ML Service Error: {response.text}")
                return {}
                
            data = response.json()
            # Convert list [{"id": 1, "similarity": 0.9}] to dict {1: 0.9}
            # Note: Modal returns "id" or "anime_id" depending on RPC
            results = {}
            for item in data.get("results", []):
                aid = item.get("id") or item.get("anime_id")
                score = item.get("similarity", 0.0)
                if aid:
                    results[aid] = float(score)
            
            return results
            
    except Exception as e:
        logger.error(f"Image search failed: {e}")
        return {}


async def search_by_sbert(query: str, top_k: int = 10, db: AsyncSession = None) -> Dict[int, float]:
    """
    Search anime using SBERT embeddings (Local execution + DB Query)
    
    Args:
        query: Text query
        top_k: Number of results
        db: Database session (Required for pgvector query)
    
    Returns:
        Dictionary mapping anime_id to similarity score
    """
    if not db:
        logger.error("Database session required for vector search")
        return {}
        
    try:
        # 1. Encode query locally (lightweight model)
        query_embedding = encode_text_sbert(query)
        embedding_list = query_embedding.tolist()[0] if hasattr(query_embedding, "tolist") else query_embedding
        
        # 2. Query Supabase using pgvector <=> operator (cosine distance)
        # 1 - (a <=> b) = cosine similarity
        stmt = text("""
            SELECT id, 1 - (embedding_sbert <=> :embedding) as similarity
            FROM anime
            WHERE embedding_sbert IS NOT NULL
            ORDER BY embedding_sbert <=> :embedding
            LIMIT :limit
        """)
        
        result = await db.execute(stmt, {"embedding": str(embedding_list), "limit": top_k})
        rows = result.fetchall()
        
        return {row[0]: float(row[1]) for row in rows}
        
    except Exception as e:
        logger.error(f"SBERT search failed: {e}")
        return {}
