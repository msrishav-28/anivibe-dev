"""
Vector similarity search using FAISS
"""
import numpy as np
import faiss
import logging
from pathlib import Path
from typing import Dict, Optional
import pickle

from app.core.ml_models import encode_text_clip, encode_text_sbert
from config import settings

logger = logging.getLogger(__name__)

# Global FAISS indexes
clip_index: Optional[faiss.Index] = None
sbert_index: Optional[faiss.Index] = None
anime_id_mapping: Optional[Dict[int, int]] = None  # index_pos -> anime_id


def load_faiss_indexes():
    """Load FAISS indexes from disk"""
    global clip_index, sbert_index, anime_id_mapping
    
    faiss_dir = Path(settings.faiss_index_path)
    
    try:
        # Load CLIP index
        clip_path = faiss_dir / "clip_index.faiss"
        if clip_path.exists():
            clip_index = faiss.read_index(str(clip_path))
            logger.info(f"Loaded CLIP index with {clip_index.ntotal} vectors")
        
        # Load SBERT index
        sbert_path = faiss_dir / "sbert_index.faiss"
        if sbert_path.exists():
            sbert_index = faiss.read_index(str(sbert_path))
            logger.info(f"Loaded SBERT index with {sbert_index.ntotal} vectors")
        
        # Load ID mapping
        mapping_path = faiss_dir / "anime_id_mapping.pkl"
        if mapping_path.exists():
            with open(mapping_path, 'rb') as f:
                anime_id_mapping = pickle.load(f)
            logger.info(f"Loaded anime ID mapping with {len(anime_id_mapping)} entries")
        
    except Exception as e:
        logger.error(f"Failed to load FAISS indexes: {e}")


async def search_by_clip(query: str, top_k: int = 10) -> Dict[int, float]:
    """
    Search anime using CLIP embeddings
    
    Args:
        query: Text query
        top_k: Number of results
    
    Returns:
        Dictionary mapping anime_id to similarity score
    """
    global clip_index, anime_id_mapping
    
    if clip_index is None or anime_id_mapping is None:
        load_faiss_indexes()
    
    if clip_index is None:
        logger.warning("CLIP index not available")
        return {}
    
    try:
        # Encode query
        query_embedding = encode_text_clip(query)
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search
        distances, indices = clip_index.search(query_embedding.astype('float32'), top_k)
        
        # Convert to anime IDs and scores
        results = {}
        for idx, distance in zip(indices[0], distances[0]):
            if idx >= 0 and idx in anime_id_mapping:
                anime_id = anime_id_mapping[idx]
                results[anime_id] = float(distance)
        
        return results
        
    except Exception as e:
        logger.error(f"CLIP search failed: {e}")
        return {}


async def search_by_sbert(query: str, top_k: int = 10) -> Dict[int, float]:
    """
    Search anime using SBERT embeddings
    
    Args:
        query: Text query
        top_k: Number of results
    
    Returns:
        Dictionary mapping anime_id to similarity score
    """
    global sbert_index, anime_id_mapping
    
    if sbert_index is None or anime_id_mapping is None:
        load_faiss_indexes()
    
    if sbert_index is None:
        logger.warning("SBERT index not available")
        return {}
    
    try:
        # Encode query
        query_embedding = encode_text_sbert(query)
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        # Search
        distances, indices = sbert_index.search(query_embedding.astype('float32'), top_k)
        
        # Convert to anime IDs and scores
        results = {}
        for idx, distance in zip(indices[0], distances[0]):
            if idx >= 0 and idx in anime_id_mapping:
                anime_id = anime_id_mapping[idx]
                results[anime_id] = float(distance)
        
        return results
        
    except Exception as e:
        logger.error(f"SBERT search failed: {e}")
        return {}


def create_faiss_index(embeddings: np.ndarray, anime_ids: list, index_type: str = "clip"):
    """
    Create and save FAISS index
    
    Args:
        embeddings: Numpy array of embeddings
        anime_ids: List of anime IDs
        index_type: Type of index ("clip" or "sbert")
    """
    dimension = embeddings.shape[1]
    
    # Create index (using flat index for simplicity, can upgrade to IVF for large datasets)
    index = faiss.IndexFlatIP(dimension)  # Inner product = cosine similarity for normalized vectors
    index.add(embeddings.astype('float32'))
    
    # Save index
    faiss_dir = Path(settings.faiss_index_path)
    faiss_dir.mkdir(parents=True, exist_ok=True)
    
    index_path = faiss_dir / f"{index_type}_index.faiss"
    faiss.write_index(index, str(index_path))
    
    # Save ID mapping
    id_mapping = {i: anime_id for i, anime_id in enumerate(anime_ids)}
    mapping_path = faiss_dir / "anime_id_mapping.pkl"
    with open(mapping_path, 'wb') as f:
        pickle.dump(id_mapping, f)
    
    logger.info(f"Created and saved {index_type} FAISS index with {index.ntotal} vectors")
