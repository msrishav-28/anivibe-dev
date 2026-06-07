"""
User management endpoints.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.core.storage import upload_avatar as upload_avatar_to_r2
from app.models.user import Profile
from app.models.rating import Rating
from app.models.watchlist import WatchlistEntry
from app.schemas.user import UserUpdate

router = APIRouter()


@router.get("/me")
async def get_current_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user profile from database
    """
    user_id = UUID(current_user["id"])
    
    result = await db.execute(
        select(Profile).filter(Profile.id == user_id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        # Return data from auth if profile not in DB yet
        return current_user
    
    return profile.to_dict()


@router.put("/me")
async def update_current_user_profile(
    user_update: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user profile
    """
    user_id = UUID(current_user["id"])
    
    result = await db.execute(
        select(Profile).filter(Profile.id == user_id)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update profile fields
    for field, value in user_update.dict(exclude_unset=True).items():
        if hasattr(profile, field):
            setattr(profile, field, value)
    
    await db.commit()
    await db.refresh(profile)
    
    return profile.to_dict()


@router.post("/me/avatar")
async def upload_avatar(
    avatar: UploadFile = File(...),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload user avatar to Cloudflare R2.
    """
    user_id = current_user["id"]
    public_url = await upload_avatar_to_r2(user_id, avatar)

    await db.execute(
        update(Profile).where(Profile.id == UUID(user_id)).values(avatar_url=public_url)
    )
    await db.commit()

    return {"avatar_url": public_url}


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user by ID (public profile)
    """
    try:
        uid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    result = await db.execute(
        select(Profile).filter(Profile.id == uid, Profile.is_active.is_(True))
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return profile.to_dict()


@router.get("/{user_id}/stats")
async def get_user_statistics(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user statistics
    """
    try:
        uid = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    # Get user profile
    result = await db.execute(
        select(Profile).filter(Profile.id == uid)
    )
    profile = result.scalar_one_or_none()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get ratings count and average
    ratings_result = await db.execute(
        select(
            func.count(Rating.id),
            func.avg(Rating.score)
        ).filter(Rating.user_id == uid)
    )
    ratings_count, avg_rating = ratings_result.one()
    
    # Get watchlist stats
    watchlist_result = await db.execute(
        select(func.count(WatchlistEntry.id))
        .filter(WatchlistEntry.user_id == uid)
    )
    watchlist_count = watchlist_result.scalar()
    
    # Get watchlist by status
    status_counts = {}
    for status_name in ["plan_to_watch", "watching", "completed", "on_hold", "dropped"]:
        result = await db.execute(
            select(func.count(WatchlistEntry.id))
            .filter(
                WatchlistEntry.user_id == uid,
                WatchlistEntry.status == status_name
            )
        )
        status_counts[status_name] = result.scalar() or 0
    
    return {
        "user_id": str(uid),
        "username": profile.username,
        "anime_watched": profile.anime_watched,
        "episodes_watched": profile.episodes_watched,
        "watch_time_hours": profile.watch_time_hours,
        "ratings_count": ratings_count or 0,
        "average_rating": float(avg_rating) if avg_rating else 0.0,
        "watchlist_total": watchlist_count or 0,
        "watchlist_by_status": status_counts,
        "member_since": profile.created_at.isoformat() if profile.created_at else None
    }


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Delete current user account
    Note: this deletes only the AniVibe profile. Clerk user deletion is handled in Clerk.
    """
    user_id = UUID(current_user["id"])
    
    result = await db.execute(
        select(Profile).filter(Profile.id == user_id)
    )
    profile = result.scalar_one_or_none()
    
    if profile:
        await db.delete(profile)
        await db.commit()
    
    return None
