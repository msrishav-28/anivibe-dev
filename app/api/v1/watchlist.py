"""
Watchlist endpoints
"""
from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.models.user import User
from app.models.watchlist import WatchlistEntry, WatchStatus
from app.models.anime import Anime
from app.schemas.watchlist import WatchlistEntryCreate, WatchlistEntryUpdate, WatchlistEntryResponse, WatchlistStats

router = APIRouter()


@router.post("/", response_model=WatchlistEntryResponse, status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(
    entry_data: WatchlistEntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Add anime to watchlist
    """
    # Check if anime exists
    anime_result = await db.execute(
        select(Anime).filter(Anime.id == entry_data.anime_id)
    )
    anime = anime_result.scalar_one_or_none()
    if not anime:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Anime not found"
        )
    
    # Check if entry already exists
    existing_result = await db.execute(
        select(WatchlistEntry).filter(
            and_(
                WatchlistEntry.user_id == current_user.id,
                WatchlistEntry.anime_id == entry_data.anime_id
            )
        )
    )
    if existing_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Anime already in watchlist"
        )
    
    # Create entry
    entry = WatchlistEntry(
        user_id=current_user.id,
        anime_id=entry_data.anime_id,
        status=WatchStatus(entry_data.status),
        episodes_watched=entry_data.episodes_watched,
        is_favorite=entry_data.is_favorite,
        notes=entry_data.notes
    )
    
    # Set started_at if watching
    if entry.status == WatchStatus.WATCHING:
        entry.started_at = datetime.utcnow()
    
    db.add(entry)
    await db.commit()
    await db.refresh(entry)
    
    return entry


@router.get("/", response_model=List[WatchlistEntryResponse])
async def get_watchlist(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
    status: str = Query(None, description="Filter by status"),
    include_anime: bool = Query(True, description="Include anime details")
):
    """
    Get user's watchlist
    """
    query = select(WatchlistEntry).filter(WatchlistEntry.user_id == current_user.id)
    
    if include_anime:
        query = query.options(selectinload(WatchlistEntry.anime))
    
    if status:
        try:
            status_enum = WatchStatus(status)
            query = query.filter(WatchlistEntry.status == status_enum)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status"
            )
    
    query = query.order_by(WatchlistEntry.updated_at.desc())
    
    result = await db.execute(query)
    entries = result.scalars().all()
    
    return [entry.to_dict(include_anime=include_anime) for entry in entries]


@router.get("/stats", response_model=WatchlistStats)
async def get_watchlist_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get watchlist statistics
    """
    # Get counts by status
    stats = {}
    for status in WatchStatus:
        result = await db.execute(
            select(func.count(WatchlistEntry.id))
            .filter(
                and_(
                    WatchlistEntry.user_id == current_user.id,
                    WatchlistEntry.status == status
                )
            )
        )
        stats[status.value.lower().replace(" ", "_")] = result.scalar()
    
    total = sum(stats.values())
    completed = stats.get("completed", 0)
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    return {
        "total_entries": total,
        "plan_to_watch": stats.get("plan_to_watch", 0),
        "watching": stats.get("watching", 0),
        "completed": completed,
        "on_hold": stats.get("on_hold", 0),
        "dropped": stats.get("dropped", 0),
        "total_episodes": current_user.episodes_watched,
        "total_watch_time_hours": current_user.watch_time_hours,
        "completion_rate": completion_rate
    }


@router.put("/{entry_id}", response_model=WatchlistEntryResponse)
async def update_watchlist_entry(
    entry_id: int,
    entry_update: WatchlistEntryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update watchlist entry
    """
    result = await db.execute(
        select(WatchlistEntry).filter(
            and_(
                WatchlistEntry.id == entry_id,
                WatchlistEntry.user_id == current_user.id
            )
        )
    )
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist entry not found"
        )
    
    # Update fields
    for field, value in entry_update.dict(exclude_unset=True).items():
        if field == "status" and value:
            value = WatchStatus(value)
            # Update timestamps based on status
            if value == WatchStatus.WATCHING and not entry.started_at:
                entry.started_at = datetime.utcnow()
            elif value == WatchStatus.COMPLETED:
                entry.completed_at = datetime.utcnow()
        
        setattr(entry, field, value)
    
    await db.commit()
    await db.refresh(entry)
    
    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_from_watchlist(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Remove anime from watchlist
    """
    result = await db.execute(
        select(WatchlistEntry).filter(
            and_(
                WatchlistEntry.id == entry_id,
                WatchlistEntry.user_id == current_user.id
            )
        )
    )
    entry = result.scalar_one_or_none()
    
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Watchlist entry not found"
        )
    
    await db.delete(entry)
    await db.commit()
    
    return None
