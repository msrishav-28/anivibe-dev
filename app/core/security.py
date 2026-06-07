"""
Authentication and authorization helpers for Clerk JWTs.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
import logging
import re

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from app.core.database import get_db
from app.models.user import Profile

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)
_jwks_cache: Optional[Dict[str, Any]] = None


def is_dev_auth_bypass_enabled() -> bool:
    """Return whether local dev auth is active, failing closed in production."""
    if not settings.auth_required and settings.is_production:
        raise RuntimeError("AUTH_REQUIRED=false is not allowed when ENVIRONMENT=production")
    return settings.is_development and not settings.auth_required


def _profile_to_user(profile: Profile) -> Dict[str, Any]:
    return {
        "id": str(profile.id),
        "user_id": str(profile.id),
        "external_auth_id": profile.external_auth_id,
        "email": profile.email,
        "username": profile.username,
        "full_name": profile.full_name,
        "avatar_url": profile.avatar_url,
        "is_verified": profile.is_verified,
        "created_at": profile.created_at,
    }


async def _fetch_jwks() -> Dict[str, Any]:
    global _jwks_cache
    if _jwks_cache:
        return _jwks_cache
    if not settings.clerk_jwks_url:
        raise RuntimeError("CLERK_JWKS_URL is not configured")

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(settings.clerk_jwks_url)
        response.raise_for_status()
        _jwks_cache = response.json()
        return _jwks_cache


async def _verify_clerk_token(token: str) -> Dict[str, Any]:
    try:
        jwks = await _fetch_jwks()
        headers = jwt.get_unverified_header(token)
        key = next((item for item in jwks.get("keys", []) if item.get("kid") == headers.get("kid")), None)
        if not key:
            global _jwks_cache
            _jwks_cache = None
            jwks = await _fetch_jwks()
            key = next((item for item in jwks.get("keys", []) if item.get("kid") == headers.get("kid")), None)
        if not key:
            raise JWTError("Signing key not found")

        options = {"verify_aud": False}
        return jwt.decode(
            token,
            key,
            algorithms=[headers.get("alg", "RS256")],
            issuer=settings.clerk_issuer,
            options=options,
        )
    except Exception as exc:
        logger.warning("Clerk token verification failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def _username_from_claims(claims: Dict[str, Any]) -> str:
    raw = (
        claims.get("username")
        or claims.get("preferred_username")
        or claims.get("name")
        or claims.get("email")
        or claims.get("sub", "user")
    )
    username = re.sub(r"[^a-zA-Z0-9_]+", "_", str(raw).split("@")[0]).strip("_").lower()
    return (username or "user")[:42]


def _dev_auth_claims(request: Request) -> Dict[str, Any]:
    raw_user = request.headers.get(settings.dev_auth_header, settings.dev_auth_default_user)
    username = _username_from_claims({"username": raw_user})
    external_auth_id = f"dev:{username}"
    return {
        "sub": external_auth_id,
        "username": f"dev_{username}"[:42],
        "email": f"{username}@dev.anivibe.local",
        "name": f"Local Dev User {username}",
        "email_verified": True,
    }


async def _get_or_create_profile(claims: Dict[str, Any], db: AsyncSession) -> Profile:
    external_auth_id = claims.get("sub")
    if not external_auth_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth subject")

    result = await db.execute(select(Profile).filter(Profile.external_auth_id == external_auth_id))
    profile = result.scalar_one_or_none()
    if profile:
        profile.last_login = datetime.utcnow()
        await db.commit()
        await db.refresh(profile)
        return profile

    email = claims.get("email") or claims.get("primary_email_address") or f"{external_auth_id}@clerk.local"
    username_base = _username_from_claims(claims)
    username = username_base
    suffix = 1
    while True:
        existing = await db.execute(select(Profile.id).filter(Profile.username == username))
        if existing.scalar_one_or_none() is None:
            break
        suffix += 1
        username = f"{username_base[:38]}_{suffix}"

    profile = Profile(
        external_auth_id=external_auth_id,
        email=email,
        username=username,
        full_name=claims.get("name"),
        avatar_url=claims.get("picture") or claims.get("image_url"),
        is_verified=bool(claims.get("email_verified", True)),
        last_login=datetime.utcnow(),
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


async def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Verify Clerk JWT and return the internal AniVibe user profile."""
    if not credentials:
        if is_dev_auth_bypass_enabled():
            profile = await _get_or_create_profile(_dev_auth_claims(request), db)
            return _profile_to_user(profile)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    claims = await _verify_clerk_token(credentials.credentials)
    profile = await _get_or_create_profile(claims, db)
    return _profile_to_user(profile)


async def get_current_user_optional(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> Optional[Dict[str, Any]]:
    if not credentials:
        if is_dev_auth_bypass_enabled():
            profile = await _get_or_create_profile(_dev_auth_claims(request), db)
            return _profile_to_user(profile)
        return None
    try:
        return await get_current_user(request, credentials, db)
    except HTTPException:
        return None


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    return current_user


async def get_current_verified_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    if not current_user.get("is_verified"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified",
        )
    return current_user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    raise NotImplementedError("Password authentication is handled by Clerk")


def get_password_hash(password: str) -> str:
    raise NotImplementedError("Password authentication is handled by Clerk")


def create_access_token(data: dict) -> str:
    raise NotImplementedError("Token creation is handled by Clerk")


def create_refresh_token(data: dict) -> str:
    raise NotImplementedError("Token creation is handled by Clerk")


def decode_token(token: str) -> dict:
    raise NotImplementedError("Token verification is handled by get_current_user")
