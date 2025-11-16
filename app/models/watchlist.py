"""
Watchlist model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class WatchStatus(str, enum.Enum):
    """Watch status enumeration"""
    PLAN_TO_WATCH = "Plan to Watch"
    WATCHING = "Watching"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    DROPPED = "Dropped"


class WatchlistEntry(Base):
    """User watchlist entry model"""
    
    __tablename__ = "watchlist"
    __table_args__ = (
        UniqueConstraint('user_id', 'anime_id', name='unique_user_anime_watchlist'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    anime_id = Column(Integer, ForeignKey('anime.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Status
    status = Column(SQLEnum(WatchStatus), nullable=False, default=WatchStatus.PLAN_TO_WATCH)
    
    # Progress
    episodes_watched = Column(Integer, default=0, nullable=False)
    
    # Flags
    is_favorite = Column(Boolean, default=False)
    is_rewatching = Column(Boolean, default=False)
    
    # Dates
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Notes
    notes = Column(String(1000), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="watchlist")
    anime = relationship("Anime", back_populates="watchlist_entries")
    
    def __repr__(self):
        return f"<WatchlistEntry(user_id={self.user_id}, anime_id={self.anime_id}, status={self.status})>"
    
    def to_dict(self, include_anime=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "anime_id": self.anime_id,
            "status": self.status.value,
            "episodes_watched": self.episodes_watched,
            "is_favorite": self.is_favorite,
            "is_rewatching": self.is_rewatching,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_anime and self.anime:
            data["anime"] = self.anime.to_dict(include_relationships=True)
        
        return data
