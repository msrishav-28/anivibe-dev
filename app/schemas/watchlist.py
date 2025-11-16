"""
Watchlist schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WatchlistEntryBase(BaseModel):
    """Base watchlist entry schema"""
    anime_id: int = Field(..., description="Anime ID")
    status: str = Field(..., description="Watch status")


class WatchlistEntryCreate(WatchlistEntryBase):
    """Schema for creating a watchlist entry"""
    episodes_watched: int = Field(0, ge=0)
    is_favorite: bool = False
    notes: Optional[str] = Field(None, max_length=1000)


class WatchlistEntryUpdate(BaseModel):
    """Schema for updating a watchlist entry"""
    status: Optional[str] = None
    episodes_watched: Optional[int] = Field(None, ge=0)
    is_favorite: Optional[bool] = None
    is_rewatching: Optional[bool] = None
    notes: Optional[str] = Field(None, max_length=1000)


class WatchlistEntryResponse(WatchlistEntryBase):
    """Watchlist entry response schema"""
    id: int
    user_id: int
    episodes_watched: int
    is_favorite: bool
    is_rewatching: bool
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    anime: Optional[dict] = None  # AnimeResponse
    
    class Config:
        from_attributes = True


class WatchlistStats(BaseModel):
    """Watchlist statistics schema"""
    total_entries: int
    plan_to_watch: int
    watching: int
    completed: int
    on_hold: int
    dropped: int
    total_episodes: int
    total_watch_time_hours: float
    completion_rate: float
