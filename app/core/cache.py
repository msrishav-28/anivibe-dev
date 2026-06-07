"""
Redis cache management.
"""
import json
from typing import Any, Optional
import logging

import redis.asyncio as aioredis

from config import settings

logger = logging.getLogger(__name__)

redis_client: Optional[aioredis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis if available."""
    global redis_client

    try:
        redis_client = await aioredis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=False,
            max_connections=50,
        )
        await redis_client.ping()
        logger.info("Redis connection established")
    except Exception as exc:
        redis_client = None
        message = f"Redis unavailable: {exc}"
        if settings.redis_required or settings.is_production:
            logger.error(message)
            raise
        logger.warning("%s; continuing without cache", message)


async def close_redis() -> None:
    """Close Redis connection."""
    global redis_client

    if redis_client:
        await redis_client.close()
        redis_client = None
        logger.info("Redis connection closed")


def get_redis() -> Optional[aioredis.Redis]:
    return redis_client


async def cache_get(key: str) -> Optional[Any]:
    if redis_client is None:
        return None
    try:
        value = await redis_client.get(key)
        if value is None:
            return None
        return json.loads(value.decode("utf-8"))
    except Exception as exc:
        logger.warning("Cache get failed for %s: %s", key, exc)
        return None


async def cache_set(key: str, value: Any, expire: int = 3600) -> bool:
    if redis_client is None:
        return False
    try:
        serialized = json.dumps(value, default=str).encode("utf-8")
        await redis_client.set(key, serialized, ex=expire)
        return True
    except Exception as exc:
        logger.warning("Cache set failed for %s: %s", key, exc)
        return False


async def cache_delete(key: str) -> bool:
    if redis_client is None:
        return False
    try:
        await redis_client.delete(key)
        return True
    except Exception as exc:
        logger.warning("Cache delete failed for %s: %s", key, exc)
        return False


async def cache_exists(key: str) -> bool:
    if redis_client is None:
        return False
    try:
        return await redis_client.exists(key) > 0
    except Exception as exc:
        logger.warning("Cache exists failed for %s: %s", key, exc)
        return False


async def cache_clear_pattern(pattern: str) -> int:
    if redis_client is None:
        return 0
    try:
        keys = [key async for key in redis_client.scan_iter(match=pattern)]
        if not keys:
            return 0
        return await redis_client.delete(*keys)
    except Exception as exc:
        logger.warning("Cache clear failed for %s: %s", pattern, exc)
        return 0


async def cache_increment(key: str, amount: int = 1) -> Optional[int]:
    if redis_client is None:
        return None
    try:
        return await redis_client.incrby(key, amount)
    except Exception as exc:
        logger.warning("Cache increment failed for %s: %s", key, exc)
        return None


async def cache_set_many(mapping: dict, expire: int = 3600) -> bool:
    if redis_client is None:
        return False
    try:
        pipe = redis_client.pipeline()
        for key, value in mapping.items():
            pipe.set(key, json.dumps(value, default=str).encode("utf-8"), ex=expire)
        await pipe.execute()
        return True
    except Exception as exc:
        logger.warning("Cache set many failed: %s", exc)
        return False


async def cache_get_many(keys: list) -> dict:
    if redis_client is None:
        return {}
    try:
        values = await redis_client.mget(keys)
        result = {}
        for key, value in zip(keys, values):
            if value is not None:
                result[key] = json.loads(value.decode("utf-8"))
        return result
    except Exception as exc:
        logger.warning("Cache get many failed: %s", exc)
        return {}
