"""
Explainability service using SHAP and LIME
Provides interpretable explanations for recommendations
"""
import logging
from typing import Dict, List, Any
from importlib.util import find_spec
import numpy as np

logger = logging.getLogger(__name__)

SHAP_AVAILABLE = find_spec("shap") is not None
LIME_AVAILABLE = find_spec("lime") is not None
if not SHAP_AVAILABLE:
    logger.info("SHAP not available. Install requirements-ml.txt to enable it.")
if not LIME_AVAILABLE:
    logger.info("LIME not available. Install requirements-ml.txt to enable it.")


class RecommendationExplainer:
    """Explains why recommendations were made"""
    
    def __init__(self):
        self.shap_explainer = None
        self.lime_explainer = None
    
    def explain_collaborative_filtering(
        self,
        anime_id: int,
        user_profile: Dict,
        similar_users: List[Dict],
        top_n_features: int = 5
    ) -> Dict[str, Any]:
        """
        Explain collaborative filtering recommendation
        
        Args:
            anime_id: Recommended anime ID
            user_profile: User's profile and preferences
            similar_users: Similar users who liked this anime
            top_n_features: Number of top features to explain
        
        Returns:
            Explanation dictionary
        """
        explanation = {
            "method": "collaborative_filtering",
            "anime_id": anime_id,
            "factors": []
        }
        
        # User similarity factor
        if similar_users:
            avg_similarity = np.mean([u.get("similarity", 0) for u in similar_users])
            explanation["factors"].append({
                "feature": "user_similarity",
                "importance": float(avg_similarity),
                "description": f"Based on {len(similar_users)} similar users who enjoyed this anime"
            })
        
        # Rating patterns
        if user_profile.get("average_rating"):
            explanation["factors"].append({
                "feature": "rating_pattern",
                "importance": 0.3,
                "description": f"Matches your average rating preference ({user_profile['average_rating']:.1f})"
            })
        
        return explanation
    
    def explain_content_based(
        self,
        anime_id: int,
        anime_features: Dict,
        user_preferences: Dict,
        top_n_features: int = 5
    ) -> Dict[str, Any]:
        """
        Explain content-based recommendation
        
        Args:
            anime_id: Recommended anime ID
            anime_features: Features of the recommended anime
            user_preferences: User's genre/tag preferences
            top_n_features: Number of top features to explain
        
        Returns:
            Explanation dictionary
        """
        explanation = {
            "method": "content_based",
            "anime_id": anime_id,
            "factors": []
        }
        
        # Genre matching
        anime_genres = set(anime_features.get("genres", []))
        user_genres = set(user_preferences.get("favorite_genres", []))
        genre_overlap = anime_genres & user_genres
        
        if genre_overlap:
            importance = len(genre_overlap) / len(anime_genres) if anime_genres else 0
            explanation["factors"].append({
                "feature": "genre_match",
                "importance": float(importance),
                "description": f"Matches your favorite genres: {', '.join(list(genre_overlap)[:3])}"
            })
        
        # Studio matching
        anime_studios = set(anime_features.get("studios", []))
        user_studios = set(user_preferences.get("favorite_studios", []))
        studio_overlap = anime_studios & user_studios
        
        if studio_overlap:
            explanation["factors"].append({
                "feature": "studio_match",
                "importance": 0.2,
                "description": f"From studio(s) you like: {', '.join(list(studio_overlap))}"
            })
        
        # Score similarity
        if anime_features.get("score") and user_preferences.get("average_rating"):
            score_diff = abs(anime_features["score"] - user_preferences["average_rating"])
            score_match = 1.0 - (score_diff / 10.0)
            
            explanation["factors"].append({
                "feature": "score_match",
                "importance": float(score_match),
                "description": f"Score ({anime_features['score']:.1f}) aligns with your preferences"
            })
        
        # Tag matching
        anime_tags = set(anime_features.get("tags", []))
        user_tags = set(user_preferences.get("favorite_tags", []))
        tag_overlap = anime_tags & user_tags
        
        if tag_overlap:
            importance = len(tag_overlap) / max(len(anime_tags), 1)
            explanation["factors"].append({
                "feature": "tag_match",
                "importance": float(importance),
                "description": f"Has tags you enjoy: {', '.join(list(tag_overlap)[:3])}"
            })
        
        # Sort by importance
        explanation["factors"] = sorted(
            explanation["factors"],
            key=lambda x: x["importance"],
            reverse=True
        )[:top_n_features]
        
        return explanation
    
    def explain_semantic_search(
        self,
        anime_id: int,
        query: str,
        visual_score: float,
        text_score: float,
        matched_elements: Dict
    ) -> Dict[str, Any]:
        """
        Explain semantic search result
        
        Args:
            anime_id: Recommended anime ID
            query: User's search query
            visual_score: CLIP visual similarity score
            text_score: BERT text similarity score
            matched_elements: Elements that matched the query
        
        Returns:
            Explanation dictionary
        """
        explanation = {
            "method": "semantic_search",
            "anime_id": anime_id,
            "query": query,
            "factors": []
        }
        
        # Visual matching
        if visual_score > 0 and matched_elements.get("visual_elements"):
            explanation["factors"].append({
                "feature": "visual_aesthetic",
                "importance": float(visual_score),
                "description": f"Visual match for: {', '.join(matched_elements['visual_elements'])}"
            })
        
        # Text matching
        if text_score > 0:
            explanation["factors"].append({
                "feature": "text_semantic",
                "importance": float(text_score),
                "description": "Synopsis and themes match your query"
            })
        
        # Emotion matching
        if matched_elements.get("emotions"):
            explanation["factors"].append({
                "feature": "emotional_tone",
                "importance": 0.4,
                "description": f"Matches mood: {', '.join(matched_elements['emotions'])}"
            })
        
        # Genre matching
        if matched_elements.get("genres"):
            explanation["factors"].append({
                "feature": "genre_match",
                "importance": 0.3,
                "description": f"Matches genres: {', '.join(matched_elements['genres'])}"
            })
        
        return explanation
    
    def explain_hybrid(
        self,
        anime_id: int,
        component_scores: Dict[str, float],
        component_explanations: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """
        Explain hybrid recommendation combining multiple methods
        
        Args:
            anime_id: Recommended anime ID
            component_scores: Scores from each component
            component_explanations: Explanations from each component
        
        Returns:
            Explanation dictionary
        """
        explanation = {
            "method": "hybrid",
            "anime_id": anime_id,
            "components": component_scores,
            "factors": []
        }
        
        # Combine factors from all components
        all_factors = []
        
        for method, weight in component_scores.items():
            if method in component_explanations:
                method_explanation = component_explanations[method]
                for factor in method_explanation.get("factors", []):
                    all_factors.append({
                        "feature": f"{method}_{factor['feature']}",
                        "importance": factor["importance"] * weight,
                        "description": factor["description"],
                        "source_method": method
                    })
        
        # Sort and take top factors
        all_factors.sort(key=lambda x: x["importance"], reverse=True)
        explanation["factors"] = all_factors[:10]
        
        # Calculate confidence
        total_importance = sum(f["importance"] for f in explanation["factors"])
        explanation["confidence"] = min(total_importance, 1.0)
        
        return explanation
    
    def generate_natural_language_explanation(self, explanation: Dict) -> str:
        """
        Generate human-readable explanation
        
        Args:
            explanation: Explanation dictionary
        
        Returns:
            Natural language explanation
        """
        if not explanation.get("factors"):
            return "This anime was recommended based on our algorithm."
        
        # Start with top factor
        top_factor = explanation["factors"][0]
        text = f"Recommended because: {top_factor['description']}"
        
        # Add additional factors
        if len(explanation["factors"]) > 1:
            additional = [f["description"] for f in explanation["factors"][1:3]]
            text += ". Also, " + ", and ".join(additional) + "."
        
        # Add confidence if available
        if explanation.get("confidence"):
            confidence = explanation["confidence"]
            confidence_text = "high" if confidence > 0.7 else "moderate" if confidence > 0.4 else "low"
            text += f" (Confidence: {confidence_text})"
        
        return text


# Global explainer instance
explainer = RecommendationExplainer()


def explain_recommendation(
    anime_id: int,
    recommendation_method: str,
    context: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Explain a recommendation
    
    Args:
        anime_id: Recommended anime ID
        recommendation_method: Method used (collaborative, content, semantic, hybrid)
        context: Context information for explanation
    
    Returns:
        Explanation dictionary with factors and natural language
    """
    if recommendation_method == "collaborative":
        explanation = explainer.explain_collaborative_filtering(
            anime_id=anime_id,
            user_profile=context.get("user_profile", {}),
            similar_users=context.get("similar_users", [])
        )
    elif recommendation_method == "content":
        explanation = explainer.explain_content_based(
            anime_id=anime_id,
            anime_features=context.get("anime_features", {}),
            user_preferences=context.get("user_preferences", {})
        )
    elif recommendation_method == "semantic":
        explanation = explainer.explain_semantic_search(
            anime_id=anime_id,
            query=context.get("query", ""),
            visual_score=context.get("visual_score", 0),
            text_score=context.get("text_score", 0),
            matched_elements=context.get("matched_elements", {})
        )
    elif recommendation_method == "hybrid":
        explanation = explainer.explain_hybrid(
            anime_id=anime_id,
            component_scores=context.get("component_scores", {}),
            component_explanations=context.get("component_explanations", {})
        )
    else:
        explanation = {
            "method": recommendation_method,
            "anime_id": anime_id,
            "factors": [],
            "description": "Recommendation based on our algorithm"
        }
    
    # Add natural language explanation
    explanation["natural_language"] = explainer.generate_natural_language_explanation(explanation)
    
    return explanation
