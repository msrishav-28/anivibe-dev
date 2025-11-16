"""
Test explainability service
"""
import pytest


def test_collaborative_filtering_explanation():
    """Test collaborative filtering explanation"""
    from app.services.explainability import RecommendationExplainer
    
    explainer = RecommendationExplainer()
    
    explanation = explainer.explain_collaborative_filtering(
        anime_id=1,
        user_profile={"average_rating": 8.5},
        similar_users=[
            {"user_id": 2, "similarity": 0.9},
            {"user_id": 3, "similarity": 0.85}
        ]
    )
    
    assert explanation["method"] == "collaborative_filtering"
    assert len(explanation["factors"]) > 0
    assert any(f["feature"] == "user_similarity" for f in explanation["factors"])


def test_content_based_explanation():
    """Test content-based explanation"""
    from app.services.explainability import RecommendationExplainer
    
    explainer = RecommendationExplainer()
    
    explanation = explainer.explain_content_based(
        anime_id=1,
        anime_features={
            "genres": ["Action", "Adventure"],
            "studios": ["Studio A"],
            "score": 8.5,
            "tags": ["fantasy", "magic"]
        },
        user_preferences={
            "favorite_genres": ["Action", "Fantasy"],
            "favorite_studios": ["Studio A"],
            "average_rating": 8.0,
            "favorite_tags": ["fantasy"]
        }
    )
    
    assert explanation["method"] == "content_based"
    assert len(explanation["factors"]) > 0
    assert any(f["feature"] == "genre_match" for f in explanation["factors"])


def test_natural_language_explanation():
    """Test natural language explanation generation"""
    from app.services.explainability import RecommendationExplainer
    
    explainer = RecommendationExplainer()
    
    explanation = {
        "factors": [
            {"feature": "genre_match", "importance": 0.8, "description": "Matches your favorite genres"},
            {"feature": "score_match", "importance": 0.6, "description": "High rating aligns with your preferences"}
        ],
        "confidence": 0.75
    }
    
    text = explainer.generate_natural_language_explanation(explanation)
    
    assert isinstance(text, str)
    assert len(text) > 0
    assert "Recommended because" in text


def test_explain_recommendation_function():
    """Test main explain_recommendation function"""
    from app.services.explainability import explain_recommendation
    
    explanation = explain_recommendation(
        anime_id=1,
        recommendation_method="content",
        context={
            "anime_features": {
                "genres": ["Action"],
                "score": 8.0
            },
            "user_preferences": {
                "favorite_genres": ["Action"],
                "average_rating": 7.5
            }
        }
    )
    
    assert "natural_language" in explanation
    assert explanation["method"] == "content"
