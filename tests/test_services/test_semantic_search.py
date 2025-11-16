"""
Test semantic search service
"""
import pytest
from unittest.mock import Mock, patch


@pytest.mark.asyncio
async def test_semantic_vibe_search():
    """Test semantic vibe search"""
    from app.services.semantic_search import semantic_vibe_search
    
    # Mock the ML models and database
    with patch("app.services.semantic_search.parse_query_with_llm") as mock_llm:
        with patch("app.services.semantic_search.search_by_clip") as mock_clip:
            with patch("app.services.semantic_search.search_by_sbert") as mock_sbert:
                # Setup mocks
                mock_llm.return_value = {
                    "visual_elements": ["rain"],
                    "emotions": ["melancholic"],
                    "genres": [],
                    "themes": [],
                    "text_description": "melancholic anime with rain"
                }
                
                mock_clip.return_value = {1: 0.9, 2: 0.8}
                mock_sbert.return_value = {1: 0.85, 3: 0.75}
                
                # Mock database
                mock_db = Mock()
                
                # Test search
                result = await semantic_vibe_search(
                    query="anime with rain and melancholic atmosphere",
                    top_k=5,
                    db=mock_db
                )
                
                assert "recommendations" in result
                assert result["method"] == "semantic_vibe_search"


def test_llm_fallback_parser():
    """Test fallback query parser"""
    from app.services.llm_parser import fallback_query_parser
    
    result = fallback_query_parser("anime with rain and sad vibes")
    
    assert "visual_elements" in result
    assert "emotions" in result
    assert "rain" in result["visual_elements"]
    assert any(emotion in ["sad", "melancholic"] for emotion in result["emotions"])
