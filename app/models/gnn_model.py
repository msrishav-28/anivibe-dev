"""
Graph Neural Network model for anime recommendations
Uses PyTorch Geometric for graph-based collaborative filtering
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch_geometric.nn import SAGEConv, GATConv
from torch_geometric.data import Data
import logging

logger = logging.getLogger(__name__)


class GraphSAGERecommender(nn.Module):
    """
    GraphSAGE model for anime recommendations
    Learns embeddings for users and anime through graph structure
    """
    
    def __init__(
        self,
        num_users: int,
        num_anime: int,
        embedding_dim: int = 128,
        hidden_dim: int = 256,
        num_layers: int = 3,
        dropout: float = 0.5
    ):
        super(GraphSAGERecommender, self).__init__()
        
        self.num_users = num_users
        self.num_anime = num_anime
        self.embedding_dim = embedding_dim
        
        # Initial embeddings
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.anime_embedding = nn.Embedding(num_anime, embedding_dim)
        
        # GraphSAGE layers
        self.convs = nn.ModuleList()
        self.convs.append(SAGEConv(embedding_dim, hidden_dim))
        
        for _ in range(num_layers - 2):
            self.convs.append(SAGEConv(hidden_dim, hidden_dim))
        
        self.convs.append(SAGEConv(hidden_dim, embedding_dim))
        
        # Batch normalization
        self.batch_norms = nn.ModuleList([
            nn.BatchNorm1d(hidden_dim) for _ in range(num_layers - 1)
        ])
        self.batch_norms.append(nn.BatchNorm1d(embedding_dim))
        
        self.dropout = dropout
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize embeddings"""
        nn.init.xavier_uniform_(self.user_embedding.weight)
        nn.init.xavier_uniform_(self.anime_embedding.weight)
    
    def forward(self, edge_index, user_indices=None, anime_indices=None):
        """
        Forward pass
        
        Args:
            edge_index: Edge connectivity [2, num_edges]
            user_indices: User node indices
            anime_indices: Anime node indices
        
        Returns:
            Node embeddings
        """
        # Get initial embeddings
        user_emb = self.user_embedding.weight
        anime_emb = self.anime_embedding.weight
        
        # Concatenate user and anime embeddings
        x = torch.cat([user_emb, anime_emb], dim=0)
        
        # Apply GraphSAGE layers
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index)
            x = self.batch_norms[i](x)
            
            if i < len(self.convs) - 1:
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
        
        return x
    
    def predict(self, user_indices, anime_indices, embeddings=None):
        """
        Predict ratings for user-anime pairs
        
        Args:
            user_indices: User indices
            anime_indices: Anime indices (offset by num_users in graph)
            embeddings: Pre-computed embeddings (optional)
        
        Returns:
            Predicted ratings
        """
        if embeddings is None:
            # Need to compute embeddings first
            raise ValueError("Embeddings must be provided for prediction")
        
        # Get user and anime embeddings
        user_emb = embeddings[user_indices]
        anime_emb = embeddings[anime_indices]
        
        # Compute dot product
        scores = (user_emb * anime_emb).sum(dim=1)
        
        return scores
    
    def recommend(self, user_idx, embeddings, top_k=10, exclude_items=None):
        """
        Get top-K recommendations for a user
        
        Args:
            user_idx: User index
            embeddings: Node embeddings
            top_k: Number of recommendations
            exclude_items: Set of anime indices to exclude
        
        Returns:
            List of (anime_idx, score) tuples
        """
        user_emb = embeddings[user_idx:user_idx+1]
        anime_emb = embeddings[self.num_users:]
        
        # Compute scores for all anime
        scores = torch.matmul(user_emb, anime_emb.t()).squeeze()
        
        # Exclude items
        if exclude_items:
            scores[list(exclude_items)] = float('-inf')
        
        # Get top-K
        top_scores, top_indices = torch.topk(scores, k=top_k)
        
        recommendations = [
            (int(idx), float(score))
            for idx, score in zip(top_indices, top_scores)
        ]
        
        return recommendations


class GATRecommender(nn.Module):
    """
    Graph Attention Network model for anime recommendations
    Uses attention mechanism to weight neighbor importance
    """
    
    def __init__(
        self,
        num_users: int,
        num_anime: int,
        embedding_dim: int = 128,
        hidden_dim: int = 256,
        num_layers: int = 3,
        num_heads: int = 4,
        dropout: float = 0.5
    ):
        super(GATRecommender, self).__init__()
        
        self.num_users = num_users
        self.num_anime = num_anime
        self.embedding_dim = embedding_dim
        
        # Initial embeddings
        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.anime_embedding = nn.Embedding(num_anime, embedding_dim)
        
        # GAT layers
        self.convs = nn.ModuleList()
        self.convs.append(GATConv(embedding_dim, hidden_dim // num_heads, heads=num_heads))
        
        for _ in range(num_layers - 2):
            self.convs.append(GATConv(hidden_dim, hidden_dim // num_heads, heads=num_heads))
        
        self.convs.append(GATConv(hidden_dim, embedding_dim, heads=1, concat=False))
        
        self.dropout = dropout
        
        # Initialize weights
        self._init_weights()
    
    def _init_weights(self):
        """Initialize embeddings"""
        nn.init.xavier_uniform_(self.user_embedding.weight)
        nn.init.xavier_uniform_(self.anime_embedding.weight)
    
    def forward(self, edge_index):
        """Forward pass with attention"""
        # Get initial embeddings
        user_emb = self.user_embedding.weight
        anime_emb = self.anime_embedding.weight
        
        # Concatenate user and anime embeddings
        x = torch.cat([user_emb, anime_emb], dim=0)
        
        # Apply GAT layers
        for i, conv in enumerate(self.convs):
            x = conv(x, edge_index)
            
            if i < len(self.convs) - 1:
                x = F.elu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
        
        return x
    
    def predict(self, user_indices, anime_indices, embeddings=None):
        """Predict ratings"""
        if embeddings is None:
            raise ValueError("Embeddings must be provided for prediction")
        
        user_emb = embeddings[user_indices]
        anime_emb = embeddings[anime_indices]
        
        scores = (user_emb * anime_emb).sum(dim=1)
        return scores
    
    def recommend(self, user_idx, embeddings, top_k=10, exclude_items=None):
        """Get top-K recommendations"""
        user_emb = embeddings[user_idx:user_idx+1]
        anime_emb = embeddings[self.num_users:]
        
        scores = torch.matmul(user_emb, anime_emb.t()).squeeze()
        
        if exclude_items:
            scores[list(exclude_items)] = float('-inf')
        
        top_scores, top_indices = torch.topk(scores, k=top_k)
        
        recommendations = [
            (int(idx), float(score))
            for idx, score in zip(top_indices, top_scores)
        ]
        
        return recommendations


def build_graph_data(user_ids, anime_ids, ratings):
    """
    Build PyTorch Geometric Data object from ratings
    
    Args:
        user_ids: List of user IDs
        anime_ids: List of anime IDs
        ratings: List of ratings
    
    Returns:
        PyTorch Geometric Data object
    """
    # Create edge index (bidirectional)
    # anime_ids are offset by max(user_ids) + 1 in the graph
    num_users = max(user_ids) + 1
    
    edge_index_list = []
    edge_attr_list = []
    
    for user_id, anime_id, rating in zip(user_ids, anime_ids, ratings):
        # User -> Anime
        edge_index_list.append([user_id, num_users + anime_id])
        edge_attr_list.append(rating)
        
        # Anime -> User (for undirected graph)
        edge_index_list.append([num_users + anime_id, user_id])
        edge_attr_list.append(rating)
    
    edge_index = torch.tensor(edge_index_list, dtype=torch.long).t()
    edge_attr = torch.tensor(edge_attr_list, dtype=torch.float)
    
    data = Data(edge_index=edge_index, edge_attr=edge_attr)
    
    return data, num_users
