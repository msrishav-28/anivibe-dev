"""
BERT4Rec sequential recommendation service
"""
import torch
import logging
from typing import List, Dict, Optional
from pathlib import Path

from app.models.bert4rec_model import BERT4Rec
from config import settings

logger = logging.getLogger(__name__)

# Global BERT4Rec model
bert4rec_model: Optional[BERT4Rec] = None
device = torch.device("cuda" if torch.cuda.is_available() and settings.use_gpu else "cpu")


def load_bert4rec_model():
    """Load trained BERT4Rec model"""
    global bert4rec_model
    
    model_path = Path(settings.model_cache_dir) / "bert4rec.pt"
    
    if not model_path.exists():
        logger.warning(f"BERT4Rec model not found: {model_path}")
        return False
    
    try:
        checkpoint = torch.load(model_path, map_location=device)
        
        bert4rec_model = BERT4Rec(
            num_items=checkpoint['num_items'],
            hidden_size=checkpoint.get('hidden_size', 256),
            num_layers=checkpoint.get('num_layers', 2),
            num_heads=checkpoint.get('num_heads', 4),
            max_seq_length=checkpoint.get('max_seq_length', 50)
        )
        
        bert4rec_model.load_state_dict(checkpoint['model_state_dict'])
        bert4rec_model = bert4rec_model.to(device)
        bert4rec_model.eval()
        
        logger.info("✅ Loaded BERT4Rec model")
        return True
        
    except Exception as e:
        logger.error(f"Error loading BERT4Rec model: {e}")
        return False


async def get_sequential_recommendations(
    user_watch_history: List[int],
    top_k: int = 10,
    exclude_anime_ids: Optional[set] = None
) -> List[Dict]:
    """
    Get recommendations based on user's sequential watch history
    
    Args:
        user_watch_history: List of anime IDs in chronological order
        top_k: Number of recommendations
        exclude_anime_ids: Set of anime IDs to exclude
    
    Returns:
        List of recommendations with scores
    """
    global bert4rec_model
    
    if bert4rec_model is None:
        if not load_bert4rec_model():
            logger.warning("BERT4Rec model not available")
            return []
    
    if not user_watch_history:
        return []
    
    try:
        recommendations = bert4rec_model.recommend_for_user(
            user_sequence=user_watch_history,
            top_k=top_k * 2,  # Get more to filter
            exclude_items=exclude_anime_ids
        )
        
        # Format results
        results = []
        for anime_id, score in recommendations[:top_k]:
            results.append({
                "anime_id": anime_id,
                "score": score,
                "method": "bert4rec"
            })
        
        return results
        
    except Exception as e:
        logger.error(f"BERT4Rec recommendation error: {e}")
        return []
