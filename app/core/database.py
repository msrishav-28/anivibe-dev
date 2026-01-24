"""
Database connection management for Supabase
"""
from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from supabase import create_client, Client
import logging

from config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy Base for ORM models
Base = declarative_base()

# Supabase clients
supabase: Optional[Client] = None
supabase_admin: Optional[Client] = None

# SQLAlchemy async engine and session factory
engine = None
AsyncSessionLocal = None


async def init_db():
    """
    Initialize database connections:
    - Supabase client for auth and real-time features
    - SQLAlchemy engine for complex queries
    """
    global supabase, supabase_admin, engine, AsyncSessionLocal
    
    try:
        # Initialize Supabase client (uses anon key, respects RLS)
        supabase = create_client(settings.supabase_url, settings.supabase_anon_key)
        logger.info("Supabase client initialized (anon key)")
        
        # Initialize Supabase admin client (bypasses RLS for server operations)
        supabase_admin = create_client(settings.supabase_url, settings.supabase_service_key)
        logger.info("Supabase admin client initialized (service key)")
        
        # Initialize SQLAlchemy engine for complex queries
        engine = create_async_engine(
            settings.database_url,
            echo=settings.debug,
            future=True,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        
        # Create async session factory
        AsyncSessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
        
        logger.info("SQLAlchemy async engine initialized for Supabase PostgreSQL")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


async def close_db():
    """Close database connections"""
    global engine
    
    try:
        if engine:
            await engine.dispose()
            logger.info("Database connections closed")
    except Exception as e:
        logger.error(f"Error closing database connections: {e}")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database session.
    Usage: db: AsyncSession = Depends(get_db)
    """
    if AsyncSessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_supabase() -> Client:
    """
    Dependency for getting Supabase client (uses anon key, respects RLS).
    Usage: supabase: Client = Depends(get_supabase)
    """
    if supabase is None:
        raise RuntimeError("Supabase not initialized. Call init_db() first.")
    return supabase


def get_supabase_admin() -> Client:
    """
    Dependency for getting Supabase admin client (bypasses RLS).
    Use only for server-side admin operations.
    Usage: supabase: Client = Depends(get_supabase_admin)
    """
    if supabase_admin is None:
        raise RuntimeError("Supabase admin not initialized. Call init_db() first.")
    return supabase_admin
