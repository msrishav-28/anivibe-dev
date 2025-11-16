"""
User management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.core.database import get_db
from app.core.security import get_current_user, get_current_active_user
from app.models.user import User
from app.models.rating import Rating
from app.models.watchlist import WatchlistEntry
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user profile
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user profile
    """
    # Update user fields
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user by ID (public profile)
    """
    result = await db.execute(
        select(User).filter(User.id == user_id, User.is_active == True)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user


@router.get("/{user_id}/stats")
async def get_user_statistics(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user statistics
    """
    # Get user
    result = await db.execute(
        select(User).filter(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get ratings count and average
    ratings_result = await db.execute(
        select(
            func.count(Rating.id),
            func.avg(Rating.score)
        ).filter(Rating.user_id == user_id)
    )
    ratings_count, avg_rating = ratings_result.one()
    
    # Get watchlist stats
    watchlist_result = await db.execute(
        select(
            func.count(WatchlistEntry.id)
        ).filter(WatchlistEntry.user_id == user_id)
    )
    watchlist_count = watchlist_result.scalar()
    
    # Get watchlist by status
    status_counts = {}
    for status_enum in ["Plan to Watch", "Watching", "Completed", "On Hold", "Dropped"]:
        result = await db.execute(
            select(func.count(WatchlistEntry.id))
            .filter(
                WatchlistEntry.user_id == user_id,
                WatchlistEntry.status == status_enum
            )
        )
        status_counts[status_enum.lower().replace(" ", "_")] = result.scalar()
    
    return {
        "user_id": user_id,
        "username": user.username,
        "anime_watched": user.anime_watched,
        "episodes_watched": user.episodes_watched,
        "watch_time_hours": user.watch_time_hours,
        "ratings_count": ratings_count or 0,
        "average_rating": float(avg_rating) if avg_rating else 0.0,
        "watchlist_total": watchlist_count or 0,
        "watchlist_by_status": status_counts,
        "member_since": user.created_at.isoformat()
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete current user account
    """
    await db.delete(current_user)
    await db.commit()
    
    return None
