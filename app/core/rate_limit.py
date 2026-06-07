"""
Route-aware API rate limiting.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import logging
import time
from typing import Dict, Optional, Tuple

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.cache import get_redis
from config import settings

logger = logging.getLogger(__name__)

_memory_counters: Dict[str, Tuple[int, float]] = {}


@dataclass(frozen=True)
class RateLimitRule:
    name: str
    requests: int
    window_seconds: int = 60


NO_LIMIT_PATHS = (
    "/",
    "/health",
    "/docs",
    "/redoc",
    "/openapi.json",
)


def classify_rate_limit(path: str, method: str) -> Optional[RateLimitRule]:
    """Map an HTTP request to its route-level rate limit."""
    normalized_path = path.rstrip("/") or "/"
    method = method.upper()

    if normalized_path in NO_LIMIT_PATHS:
        return None

    if "/search/visual" in normalized_path or "/me/avatar" in normalized_path or "/uploads" in normalized_path:
        return RateLimitRule("visual_or_upload", 5)

    if "/search/semantic" in normalized_path:
        return RateLimitRule("semantic_search", 30)

    if "/recommendations" in normalized_path:
        return RateLimitRule("recommendations", 30)

    if method in {"POST", "PUT", "PATCH", "DELETE"} and any(
        segment in normalized_path for segment in ("/watchlist", "/ratings", "/reviews")
    ):
        return RateLimitRule("user_write", 60)

    if "/anime" in normalized_path or "/search/autocomplete" in normalized_path:
        return RateLimitRule("browse", 120)

    if "/auth" in normalized_path:
        return RateLimitRule("auth", 30)

    return RateLimitRule("default", settings.rate_limit_per_minute)


def _request_identity(request: Request) -> str:
    dev_user = request.headers.get(settings.dev_auth_header)
    if dev_user:
        return f"dev:{dev_user.lower()}"

    authorization = request.headers.get("authorization")
    if authorization:
        digest = hashlib.sha256(authorization.encode("utf-8")).hexdigest()[:24]
        return f"auth:{digest}"

    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        return f"ip:{forwarded_for.split(',')[0].strip()}"

    client_host = request.client.host if request.client else "unknown"
    return f"ip:{client_host}"


async def _redis_check(key: str, rule: RateLimitRule) -> tuple[bool, int, int]:
    redis = get_redis()
    if redis is None:
        raise RuntimeError("Redis is not initialized")

    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, rule.window_seconds)
    ttl = await redis.ttl(key)
    retry_after = ttl if ttl and ttl > 0 else rule.window_seconds
    remaining = max(rule.requests - count, 0)
    return count <= rule.requests, remaining, retry_after


def _memory_check(key: str, rule: RateLimitRule) -> tuple[bool, int, int]:
    now = time.time()
    count, expires_at = _memory_counters.get(key, (0, now + rule.window_seconds))
    if expires_at <= now:
        count = 0
        expires_at = now + rule.window_seconds
    count += 1
    _memory_counters[key] = (count, expires_at)
    retry_after = max(int(expires_at - now), 1)
    remaining = max(rule.requests - count, 0)
    return count <= rule.requests, remaining, retry_after


async def check_rate_limit(request: Request) -> Optional[JSONResponse]:
    """Return a 429 response when a request exceeds its route limit."""
    if not settings.rate_limit_enabled:
        return None

    rule = classify_rate_limit(request.url.path, request.method)
    if rule is None:
        return None

    identity = _request_identity(request)
    window = int(time.time() // rule.window_seconds)
    key = f"rate_limit:{rule.name}:{identity}:{window}"

    try:
        allowed, remaining, retry_after = await _redis_check(key, rule)
        source = "redis"
    except Exception as exc:
        allowed, remaining, retry_after = _memory_check(key, rule)
        source = "memory"
        logger.debug("Rate limit using memory fallback: %s", exc)

    request.state.rate_limit_source = source
    request.state.rate_limit_rule = rule.name

    if allowed:
        return None

    return JSONResponse(
        status_code=429,
        headers={
            "Retry-After": str(retry_after),
            "X-RateLimit-Limit": str(rule.requests),
            "X-RateLimit-Remaining": str(remaining),
            "X-RateLimit-Reset": str(retry_after),
        },
        content={
            "error": {
                "code": "rate_limit_exceeded",
                "message": "Too many requests. Please retry after the rate limit window resets.",
                "details": {
                    "limit": rule.requests,
                    "window_seconds": rule.window_seconds,
                    "retry_after": retry_after,
                    "scope": rule.name,
                },
            }
        },
    )
