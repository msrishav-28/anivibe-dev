"""
Database setup script
Creates tables and initial data (genres)
"""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parents[1]))

from app.core.database import engine, Base
from app.models import *  # Import all models
from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_tables():
    """Create all database tables"""
    logger.info("Creating database tables...")
    
    # In Supabase, we prefer using the SQL schema file, but this can serve as a fallback
    # or for local development if not using Supabase local dev
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ Database tables created successfully")


async def create_initial_data():
    """Create initial seed data"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    from app.models.anime import Genre
    
    logger.info("Creating initial data...")
    
    # Note: We do NOT create users here because Supabase Auth handles user creation.
    # Users must sign up via the Auth API or be created in the Supabase Dashboard.
    
    async with AsyncSession(engine) as session:
        # Create common genres if they don't exist
        common_genres = [
            "Action", "Adventure", "Comedy", "Drama", "Fantasy", 
            "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life",
            "Sports", "Supernatural", "Thriller", "Psychological", "Ecchi"
        ]
        
        # Check existing genres
        # Note: In a fresh DB this table might be empty
        try:
            existing_genres = await session.execute(select(Genre))
            existing_genre_names = {g.name for g in existing_genres.scalars().all()}
        except Exception:
            existing_genre_names = set()
        
        count = 0
        for genre_name in common_genres:
            if genre_name not in existing_genre_names:
                genre = Genre(name=genre_name)
                session.add(genre)
                count += 1
        
        if count > 0:
            await session.commit()
            logger.info(f"✅ Created {count} common genres")
        else:
            logger.info("Generes already seeded")


async def main():
    """Main setup function"""
    try:
        logger.info(f"Setting up database: {settings.app_name}")
        
        # We skip table creation if using Supabase migration script (recommended)
        # But keeping this available for dev environments
        # await create_tables() 
        
        await create_initial_data()
        
        logger.info("✅ Database setup completed successfully!")
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        # Don't raise, just log, as this might be expected if tables don't exist yet
        # and we haven't run migrations


if __name__ == "__main__":
    asyncio.run(main())
