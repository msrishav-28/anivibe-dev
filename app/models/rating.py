"""
Rating model
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Rating(Base):
    """User anime rating model"""
    
    __tablename__ = "ratings"
    __table_args__ = (
        UniqueConstraint('user_id', 'anime_id', name='unique_user_anime_rating'),
    )
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    anime_id = Column(Integer, ForeignKey('anime.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Rating
    score = Column(Float, nullable=False)  # 0-10 scale
    
    # Review
    review_text = Column(Text, nullable=True)
    review_sentiment = Column(Float, nullable=True)  # -1 to 1
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="ratings")
    anime = relationship("Anime", back_populates="ratings")
    
    def __repr__(self):
        return f"<Rating(user_id={self.user_id}, anime_id={self.anime_id}, score={self.score})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "anime_id": self.anime_id,
            "score": self.score,
            "review_text": self.review_text,
            "review_sentiment": self.review_sentiment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
