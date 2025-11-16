"""
Anime schemas
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class GenreResponse(BaseModel):
    """Genre response schema"""
    id: int
    name: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class StudioResponse(BaseModel):
    """Studio response schema"""
    id: int
    name: str
    established: Optional[int] = None
    
    class Config:
        from_attributes = True


class TagResponse(BaseModel):
    """Tag response schema"""
    id: int
    name: str
    category: Optional[str] = None
    description: Optional[str] = None
    
    class Config:
        from_attributes = True


class AnimeBase(BaseModel):
    """Base anime schema"""
    title: str
    title_english: Optional[str] = None
    title_japanese: Optional[str] = None


class AnimeResponse(AnimeBase):
    """Anime response schema"""
    id: int
    mal_id: Optional[int] = None
    anilist_id: Optional[int] = None
    synopsis: Optional[str] = None
    image_url: Optional[str] = None
    trailer_url: Optional[str] = None
    type: Optional[str] = None
    status: Optional[str] = None
    episodes: Optional[int] = None
    duration_minutes: Optional[int] = None
    aired_from: Optional[datetime] = None
    aired_to: Optional[datetime] = None
    season: Optional[str] = None
    year: Optional[int] = None
    score: Optional[float] = None
    scored_by: Optional[int] = None
    rank: Optional[int] = None
    popularity: Optional[int] = None
    members: Optional[int] = None
    favorites: Optional[int] = None
    rating: Optional[str] = None
    source: Optional[str] = None
    is_nsfw: bool = False
    is_hidden_gem: bool = False
    genres: Optional[List[GenreResponse]] = []
    studios: Optional[List[StudioResponse]] = []
    tags: Optional[List[TagResponse]] = []
    
    class Config:
        from_attributes = True


class AnimeSearch(BaseModel):
    """Anime search parameters"""
    query: Optional[str] = Field(None, description="Search query")
    genres: Optional[List[str]] = Field(None, description="Filter by genres")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    type: Optional[str] = Field(None, description="Filter by type (TV, Movie, etc.)")
    status: Optional[str] = Field(None, description="Filter by status")
    year_from: Optional[int] = Field(None, ge=1960, le=2030)
    year_to: Optional[int] = Field(None, ge=1960, le=2030)
    score_min: Optional[float] = Field(None, ge=0, le=10)
    score_max: Optional[float] = Field(None, ge=0, le=10)
    episodes_min: Optional[int] = Field(None, ge=1)
    episodes_max: Optional[int] = Field(None, ge=1)
    order_by: Optional[str] = Field("score", description="Order by field")
    sort: Optional[str] = Field("desc", description="Sort direction (asc/desc)")
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)


class AnimeStatistics(BaseModel):
    """Anime statistics schema"""
    total_anime: int
    total_genres: int
    total_studios: int
    total_tags: int
    average_score: float
    most_popular_genre: str
    newest_anime: AnimeResponse
    highest_rated: AnimeResponse
