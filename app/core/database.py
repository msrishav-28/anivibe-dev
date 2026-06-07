"""
Database connection management for Neon/Postgres.
"""
from typing import AsyncGenerator
import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

from config import settings

logger = logging.getLogger(__name__)

Base = declarative_base()

engine = None
AsyncSessionLocal = None


async def init_db() -> None:
    """Initialize the async SQLAlchemy engine."""
    global engine, AsyncSessionLocal

    if not settings.database_url:
        message = "DATABASE_URL is not configured; database-backed endpoints are disabled"
        if settings.is_production:
            raise RuntimeError(message)
        logger.warning(message)
        return

    engine = create_async_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))

    logger.info("Database connection verified")


async def close_db() -> None:
    """Dispose of database connections."""
    global engine

    if engine:
        await engine.dispose()
        logger.info("Database connections closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for async database sessions."""
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Set DATABASE_URL and restart the API.")

    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
