"""
Rating endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.ml_models import analyze_sentiment
from app.models.user import User
from app.models.rating import Rating
from app.models.anime import Anime
from app.schemas.rating import RatingCreate, RatingUpdate, RatingResponse

router = APIRouter()


@router.post("/", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(
    rating_data: RatingCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new rating
    """
    # Check if anime exists
    anime_result = await db.execute(
        select(Anime).filter(Anime.id == rating_data.anime_id)
    )
    anime = anime_result.scalar_one_or_none()
    if not anime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anime not found"
        )
    
    # Check if rating already exists
    existing_result = await db.execute(
        select(Rating).filter(
            and_(
                Rating.user_id == current_user.id,
                Rating.anime_id == rating_data.anime_id
            )
        )
    )
    if existing_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating already exists. Use PUT to update."
        )
    
    # Analyze sentiment if review text provided
    sentiment_score = None
    if rating_data.review_text:
        sentiment_result = analyze_sentiment(rating_data.review_text)
        # Convert to -1 to 1 scale
        sentiment_map = {"negative": -1.0, "neutral": 0.0, "positive": 1.0}
        sentiment_score = sentiment_map.get(sentiment_result["sentiment"], 0.0)
    
    # Create rating
    rating = Rating(
        user_id=current_user.id,
        anime_id=rating_data.anime_id,
        score=rating_data.score,
        review_text=rating_data.review_text,
        review_sentiment=sentiment_score
    )
    
    db.add(rating)
    await db.commit()
    await db.refresh(rating)
    
    return rating


@router.get("/", response_model=List[RatingResponse])
async def get_user_ratings(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Get current user's ratings
    """
    result = await db.execute(
        select(Rating)
        .filter(Rating.user_id == current_user.id)
        .order_by(Rating.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    ratings = result.scalars().all()
    
    return ratings


@router.get("/{rating_id}", response_model=RatingResponse)
async def get_rating(
    rating_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific rating
    """
    result = await db.execute(
        select(Rating).filter(
            and_(
                Rating.id == rating_id,
                Rating.user_id == current_user.id
            )
        )
    )
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    return rating


@router.put("/{rating_id}", response_model=RatingResponse)
async def update_rating(
    rating_id: int,
    rating_update: RatingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update a rating
    """
    result = await db.execute(
        select(Rating).filter(
            and_(
                Rating.id == rating_id,
                Rating.user_id == current_user.id
            )
        )
    )
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    # Update fields
    for field, value in rating_update.dict(exclude_unset=True).items():
        setattr(rating, field, value)
    
    # Re-analyze sentiment if review text updated
    if rating_update.review_text is not None and rating.review_text:
        sentiment_result = analyze_sentiment(rating.review_text)
        sentiment_map = {"negative": -1.0, "neutral": 0.0, "positive": 1.0}
        rating.review_sentiment = sentiment_map.get(sentiment_result["sentiment"], 0.0)
    
    await db.commit()
    await db.refresh(rating)
    
    return rating


@router.delete("/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rating(
    rating_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a rating
    """
    result = await db.execute(
        select(Rating).filter(
            and_(
                Rating.id == rating_id,
                Rating.user_id == current_user.id
            )
        )
    )
    rating = result.scalar_one_or_none()
    
    if not rating:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rating not found"
        )
    
    await db.delete(rating)
    await db.commit()
    
    return None
