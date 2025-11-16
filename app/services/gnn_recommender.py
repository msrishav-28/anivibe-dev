"""
GNN-based recommendation service
"""
import torch
import logging
from typing import List, Dict, Optional
from pathlib import Path
import pickle

from app.models.gnn_model import GraphSAGERecommender, GATRecommender, build_graph_data
from config import settings

logger = logging.getLogger(__name__)

# Global GNN model and embeddings
gnn_model: Optional[torch.nn.Module] = None
gnn_embeddings: Optional[torch.Tensor] = None
device = torch.device("cuda" if torch.cuda.is_available() and settings.use_gpu else "cpu")


def load_gnn_model(model_type: str = "graphsage"):
    """Load trained GNN model"""
    global gnn_model, gnn_embeddings
    
    model_path = Path(settings.model_cache_dir) / f"gnn_{model_type}.pt"
    
    if not model_path.exists():
        logger.warning(f"GNN model not found: {model_path}")
        return False
    
    try:
        checkpoint = torch.load(model_path, map_location=device)
        
        if model_type == "graphsage":
            gnn_model = GraphSAGERecommender(
                num_users=checkpoint['num_users'],
                num_anime=checkpoint['num_anime'],
                embedding_dim=checkpoint.get('embedding_dim', 128)
            )
        else:  # GAT
            gnn_model = GATRecommender(
                num_users=checkpoint['num_users'],
                num_anime=checkpoint['num_anime'],
                embedding_dim=checkpoint.get('embedding_dim', 128)
            )
        
        gnn_model.load_state_dict(checkpoint['model_state_dict'])
        gnn_model = gnn_model.to(device)
        gnn_model.eval()
        
        # Load pre-computed embeddings
        gnn_embeddings = checkpoint.get('embeddings')
        if gnn_embeddings is not None:
            gnn_embeddings = gnn_embeddings.to(device)
        
        logger.info(f"✅ Loaded GNN model: {model_type}")
        return True
        
    except Exception as e:
        logger.error(f"Error loading GNN model: {e}")
        return False


async def get_gnn_recommendations(
    user_id: int,
    top_k: int = 10,
    exclude_anime_ids: Optional[set] = None
) -> List[Dict]:
    """
    Get recommendations using GNN model
    
    Args:
        user_id: User ID
        top_k: Number of recommendations
        exclude_anime_ids: Set of anime IDs to exclude
    
    Returns:
        List of recommendations with scores
    """
    global gnn_model, gnn_embeddings
    
    if gnn_model is None or gnn_embeddings is None:
        # Try to load model
        if not load_gnn_model():
            logger.warning("GNN model not available")
            return []
    
    try:
        with torch.no_grad():
            recommendations = gnn_model.recommend(
                user_idx=user_id,
                embeddings=gnn_embeddings,
                top_k=top_k * 2,  # Get more to filter
                exclude_items=exclude_anime_ids
            )
        
        # Filter and format
        results = []
        for anime_idx, score in recommendations[:top_k]:
            results.append({
                "anime_id": anime_idx,
                "score": score,
                "method": "gnn"
            })
        
        return results
        
    except Exception as e:
        logger.error(f"GNN recommendation error: {e}")
        return []


async def compute_anime_similarity_gnn(anime_id: int, top_k: int = 10) -> List[Dict]:
    """
    Find similar anime using GNN embeddings
    
    Args:
        anime_id: Target anime ID
        top_k: Number of similar anime
    
    Returns:
        List of similar anime with scores
    """
    global gnn_model, gnn_embeddings
    
    if gnn_model is None or gnn_embeddings is None:
        logger.warning("GNN model not available")
        return []
    
    try:
        # Get anime embedding (offset by num_users)
        anime_idx = gnn_model.num_users + anime_id
        target_emb = gnn_embeddings[anime_idx:anime_idx+1]
        
        # Get all anime embeddings
        anime_embs = gnn_embeddings[gnn_model.num_users:]
        
        # Compute similarities
        with torch.no_grad():
            similarities = torch.matmul(target_emb, anime_embs.t()).squeeze()
            similarities[anime_id] = float('-inf')  # Exclude self
            
            top_scores, top_indices = torch.topk(similarities, k=top_k)
        
        results = []
        for idx, score in zip(top_indices, top_scores):
            results.append({
                "anime_id": int(idx),
                "similarity": float(score),
                "method": "gnn_similarity"
            })
        
        return results
        
    except Exception as e:
        logger.error(f"GNN similarity error: {e}")
        return []
