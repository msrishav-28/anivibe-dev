"""
Database models
"""
from app.models.user import User
from app.models.anime import Anime, Genre, Studio, Tag
from app.models.rating import Rating
from app.models.watchlist import WatchlistEntry

__all__ = [
    "User",
    "Anime",
    "Genre",
    "Studio",
    "Tag",
    "Rating",
    "WatchlistEntry"
]
