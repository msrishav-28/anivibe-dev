"""
Test explainability API endpoints
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_explain_recommendation(client: AsyncClient, auth_headers):
    """Test recommendation explanation endpoint"""
    response = await client.post(
        "/api/v1/explain/recommendation",
        headers=auth_headers,
        json={
            "anime_id": 1,
            "recommendation_method": "content",
            "context": {
                "anime_features": {"genres": ["Action"]},
                "user_preferences": {"favorite_genres": ["Action"]}
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "natural_language" in data
    assert "factors" in data


@pytest.mark.asyncio
async def test_list_explanation_methods(client: AsyncClient):
    """Test listing explanation methods"""
    response = await client.get("/api/v1/explain/methods")
    
    assert response.status_code == 200
    data = response.json()
    assert "methods" in data
    assert len(data["methods"]) > 0
