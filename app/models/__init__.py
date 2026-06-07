"""
Database models.
"""
from app.models.user import Profile, User  # User is alias for Profile
from app.models.anime import Anime, Genre, Studio, Tag, AnimeEmbedding
from app.models.rating import Rating
from app.models.watchlist import WatchlistEntry
from app.models.review import Review, ReviewVote
from app.models.ops import DatasetVersion, ModelVersion, RecommendationEvent, SearchEvent, InferenceLog

__all__ = [
    "Profile",
    "User",  # Alias for backwards compatibility
    "Anime",
    "Genre",
    "Studio",
    "Tag",
    "AnimeEmbedding",
    "Rating",
    "WatchlistEntry",
    "Review",
    "ReviewVote",
    "DatasetVersion",
    "ModelVersion",
    "RecommendationEvent",
    "SearchEvent",
    "InferenceLog",
]
