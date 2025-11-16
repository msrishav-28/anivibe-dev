"""
Test recommendation endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_personalized_recommendations(client: AsyncClient, auth_headers):
    """Test personalized recommendations"""
    response = await client.post(
        "/api/v1/recommendations/personalized",
        headers=auth_headers,
        json={
            "top_k": 10,
            "method": "hybrid"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data
    assert "method" in data
    assert data["method"] == "hybrid"


@pytest.mark.asyncio
async def test_similar_anime(client: AsyncClient):
    """Test similar anime recommendations"""
    response = await client.post(
        "/api/v1/recommendations/similar",
        json={
            "anime_id": 1,
            "top_k": 5
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data


@pytest.mark.asyncio
async def test_hidden_gems(client: AsyncClient):
    """Test hidden gem discovery"""
    response = await client.post(
        "/api/v1/recommendations/hidden-gems",
        json={
            "top_k": 10,
            "max_popularity": 50000,
            "min_score": 7.5
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data


@pytest.mark.asyncio
async def test_mood_based_recommendations(client: AsyncClient):
    """Test mood-based recommendations"""
    response = await client.post(
        "/api/v1/recommendations/mood-based",
        json={
            "mood": "happy and uplifting",
            "top_k": 10
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "recommendations" in data


@pytest.mark.asyncio
async def test_taste_profile(client: AsyncClient, auth_headers):
    """Test user taste profile"""
    response = await client.get(
        "/api/v1/recommendations/taste-profile",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "dominant_genres" in data
