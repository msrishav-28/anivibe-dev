"""
Database setup script
Creates tables and initial data
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
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("✅ Database tables created successfully")


async def create_initial_data():
    """Create initial seed data"""
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy import select
    from app.models.user import User
    from app.models.anime import Genre
    from app.core.security import get_password_hash
    
    logger.info("Creating initial data...")
    
    async with AsyncSession(engine) as session:
        # Create admin user
        result = await session.execute(select(User).filter(User.username == "admin"))
        if not result.scalar_one_or_none():
            admin = User(
                username="admin",
                email="admin@anivibe.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Admin User",
                is_superuser=True,
                is_verified=True
            )
            session.add(admin)
            logger.info("Created admin user (username: admin, password: admin123)")
        
        # Create common genres if they don't exist
        common_genres = [
            "Action", "Adventure", "Comedy", "Drama", "Fantasy", 
            "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life",
            "Sports", "Supernatural", "Thriller", "Psychological", "Ecchi"
        ]
        
        existing_genres = await session.execute(select(Genre))
        existing_genre_names = {g.name for g in existing_genres.scalars().all()}
        
        for genre_name in common_genres:
            if genre_name not in existing_genre_names:
                genre = Genre(name=genre_name)
                session.add(genre)
        
        await session.commit()
        logger.info(f"✅ Created {len(common_genres)} common genres")


async def main():
    """Main setup function"""
    try:
        logger.info(f"Setting up database: {settings.postgres_db}")
        
        await create_tables()
        await create_initial_data()
        
        logger.info("✅ Database setup completed successfully!")
        logger.info(f"Database URL: {settings.database_url}")
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
