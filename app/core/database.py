"""
Database connection management for PostgreSQL and MongoDB
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
import logging

from config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()

# Async engine for PostgreSQL
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# MongoDB client
mongodb_client: AsyncIOMotorClient = None
mongodb_db = None


async def init_db():
    """Initialize database connections"""
    global mongodb_client, mongodb_db
    
    try:
        # Create PostgreSQL tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("PostgreSQL connection established")
        
        # Initialize MongoDB
        mongodb_client = AsyncIOMotorClient(settings.mongodb_url)
        mongodb_db = mongodb_client[settings.mongodb_db]
        # Test connection
        await mongodb_client.server_info()
        logger.info("MongoDB connection established")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def close_db():
    """Close database connections"""
    global mongodb_client
    
    try:
        # Close PostgreSQL
        await engine.dispose()
        logger.info("PostgreSQL connection closed")
        
        # Close MongoDB
        if mongodb_client:
            mongodb_client.close()
            logger.info("MongoDB connection closed")
            
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session
    Usage: db: AsyncSession = Depends(get_db)
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_mongodb():
    """
    Dependency for getting MongoDB database
    Usage: mongo_db = Depends(get_mongodb)
    """
    return mongodb_db
