"""
Test GNN models
"""
import pytest
import torch


def test_graphsage_model():
    """Test GraphSAGE model creation"""
    from app.models.gnn_model import GraphSAGERecommender
    
    model = GraphSAGERecommender(
        num_users=100,
        num_anime=500,
        embedding_dim=64,
        hidden_dim=128,
        num_layers=2
    )
    
    assert model is not None
    assert model.num_users == 100
    assert model.num_anime == 500


def test_gat_model():
    """Test GAT model creation"""
    from app.models.gnn_model import GATRecommender
    
    model = GATRecommender(
        num_users=100,
        num_anime=500,
        embedding_dim=64,
        hidden_dim=128,
        num_layers=2
    )
    
    assert model is not None
    assert model.num_users == 100


def test_build_graph_data():
    """Test graph data construction"""
    from app.models.gnn_model import build_graph_data
    
    user_ids = [0, 0, 1, 1, 2]
    anime_ids = [0, 1, 0, 2, 1]
    ratings = [8.0, 9.0, 7.5, 8.5, 9.5]
    
    data, num_users = build_graph_data(user_ids, anime_ids, ratings)
    
    assert data is not None
    assert data.edge_index.shape[1] > 0
    assert num_users == 3


def test_bert4rec_model():
    """Test BERT4Rec model creation"""
    from app.models.bert4rec_model import BERT4Rec
    
    model = BERT4Rec(
        num_items=1000,
        hidden_size=128,
        num_layers=2,
        num_heads=4
    )
    
    assert model is not None
    assert model.num_items == 1000
