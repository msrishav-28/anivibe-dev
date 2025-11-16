"""
Redis cache management
"""
import json
import pickle
from typing import Any, Optional
import redis.asyncio as aioredis
import logging

from config import settings

logger = logging.getLogger(__name__)

# Redis client
redis_client: Optional[aioredis.Redis] = None


async def init_redis():
    """Initialize Redis connection"""
    global redis_client
    
    try:
        redis_client = await aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=False,  # We'll handle encoding manually
            max_connections=50
        )
        # Test connection
        await redis_client.ping()
        logger.info("Redis connection established")
        
    except Exception as e:
        logger.error(f"Redis initialization failed: {e}")
        raise


async def close_redis():
    """Close Redis connection"""
    global redis_client
    
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")


def get_redis() -> aioredis.Redis:
    """
    Dependency for getting Redis client
    Usage: redis = Depends(get_redis)
    """
    return redis_client


async def cache_get(key: str, use_pickle: bool = False) -> Optional[Any]:
    """
    Get value from cache
    
    Args:
        key: Cache key
        use_pickle: If True, unpickle the value (for complex objects)
    
    Returns:
        Cached value or None
    """
    try:
        value = await redis_client.get(key)
        if value is None:
            return None
        
        if use_pickle:
            return pickle.loads(value)
        else:
            return json.loads(value.decode('utf-8'))
            
    except Exception as e:
        logger.error(f"Cache get error for key {key}: {e}")
        return None


async def cache_set(
    key: str,
    value: Any,
    expire: int = 3600,
    use_pickle: bool = False
) -> bool:
    """
    Set value in cache
    
    Args:
        key: Cache key
        value: Value to cache
        expire: Expiration time in seconds (default 1 hour)
        use_pickle: If True, pickle the value (for complex objects)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        if use_pickle:
            serialized = pickle.dumps(value)
        else:
            serialized = json.dumps(value).encode('utf-8')
        
        await redis_client.set(key, serialized, ex=expire)
        return True
        
    except Exception as e:
        logger.error(f"Cache set error for key {key}: {e}")
        return False


async def cache_delete(key: str) -> bool:
    """
    Delete key from cache
    
    Args:
        key: Cache key
    
    Returns:
        True if successful, False otherwise
    """
    try:
        await redis_client.delete(key)
        return True
        
    except Exception as e:
        logger.error(f"Cache delete error for key {key}: {e}")
        return False


async def cache_exists(key: str) -> bool:
    """
    Check if key exists in cache
    
    Args:
        key: Cache key
    
    Returns:
        True if exists, False otherwise
    """
    try:
        return await redis_client.exists(key) > 0
    except Exception as e:
        logger.error(f"Cache exists error for key {key}: {e}")
        return False


async def cache_clear_pattern(pattern: str) -> int:
    """
    Delete all keys matching pattern
    
    Args:
        pattern: Pattern to match (e.g., "user:*")
    
    Returns:
        Number of keys deleted
    """
    try:
        keys = []
        async for key in redis_client.scan_iter(match=pattern):
            keys.append(key)
        
        if keys:
            return await redis_client.delete(*keys)
        return 0
        
    except Exception as e:
        logger.error(f"Cache clear pattern error for {pattern}: {e}")
        return 0


async def cache_increment(key: str, amount: int = 1) -> Optional[int]:
    """
    Increment a counter in cache
    
    Args:
        key: Cache key
        amount: Amount to increment by
    
    Returns:
        New value or None
    """
    try:
        return await redis_client.incrby(key, amount)
    except Exception as e:
        logger.error(f"Cache increment error for key {key}: {e}")
        return None


async def cache_set_many(mapping: dict, expire: int = 3600) -> bool:
    """
    Set multiple key-value pairs
    
    Args:
        mapping: Dictionary of key-value pairs
        expire: Expiration time in seconds
    
    Returns:
        True if successful, False otherwise
    """
    try:
        pipe = redis_client.pipeline()
        
        for key, value in mapping.items():
            serialized = json.dumps(value).encode('utf-8')
            pipe.set(key, serialized, ex=expire)
        
        await pipe.execute()
        return True
        
    except Exception as e:
        logger.error(f"Cache set many error: {e}")
        return False


async def cache_get_many(keys: list) -> dict:
    """
    Get multiple values from cache
    
    Args:
        keys: List of cache keys
    
    Returns:
        Dictionary of key-value pairs
    """
    try:
        values = await redis_client.mget(keys)
        result = {}
        
        for key, value in zip(keys, values):
            if value is not None:
                try:
                    result[key] = json.loads(value.decode('utf-8'))
                except:
                    result[key] = None
        
        return result
        
    except Exception as e:
        logger.error(f"Cache get many error: {e}")
        return {}
