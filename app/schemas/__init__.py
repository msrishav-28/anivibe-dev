"""
Pydantic schemas for API request/response validation
"""
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, Token
from app.schemas.anime import AnimeResponse, AnimeSearch, GenreResponse, StudioResponse, TagResponse
from app.schemas.rating import RatingCreate, RatingUpdate, RatingResponse
from app.schemas.watchlist import WatchlistEntryCreate, WatchlistEntryUpdate, WatchlistEntryResponse
from app.schemas.recommendation import RecommendationRequest, RecommendationResponse, SemanticSearchRequest

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "Token",
    "AnimeResponse",
    "AnimeSearch",
    "GenreResponse",
    "StudioResponse",
    "TagResponse",
    "RatingCreate",
    "RatingUpdate",
    "RatingResponse",
    "WatchlistEntryCreate",
    "WatchlistEntryUpdate",
    "WatchlistEntryResponse",
    "RecommendationRequest",
    "RecommendationResponse",
    "SemanticSearchRequest"
]
