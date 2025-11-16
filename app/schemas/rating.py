"""
Rating schemas
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RatingBase(BaseModel):
    """Base rating schema"""
    anime_id: int = Field(..., description="Anime ID")
    score: float = Field(..., ge=0, le=10, description="Rating score (0-10)")


class RatingCreate(RatingBase):
    """Schema for creating a rating"""
    review_text: Optional[str] = Field(None, max_length=5000, description="Review text")


class RatingUpdate(BaseModel):
    """Schema for updating a rating"""
    score: Optional[float] = Field(None, ge=0, le=10)
    review_text: Optional[str] = Field(None, max_length=5000)


class RatingResponse(RatingBase):
    """Rating response schema"""
    id: int
    user_id: int
    review_text: Optional[str] = None
    review_sentiment: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class RatingWithAnime(RatingResponse):
    """Rating response with anime details"""
    anime: dict  # AnimeResponse


class BulkRatingCreate(BaseModel):
    """Schema for bulk rating creation"""
    ratings: list[RatingCreate] = Field(..., max_items=100)
