"""
Authentication endpoints.

Clerk owns signup, login, refresh, logout, and password reset UI/session flows.
The backend only verifies Clerk JWTs and exposes the internal AniVibe profile.
"""
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_active_user

router = APIRouter()


@router.get("/me")
async def me(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """Return the authenticated user's internal AniVibe profile."""
    return current_user


def _clerk_owned() -> None:
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail="This auth flow is handled by Clerk on the frontend. Send Clerk JWTs to backend APIs.",
    )


@router.post("/register", status_code=status.HTTP_410_GONE)
async def register():
    _clerk_owned()


@router.post("/login", status_code=status.HTTP_410_GONE)
async def login():
    _clerk_owned()


@router.post("/refresh", status_code=status.HTTP_410_GONE)
async def refresh_token():
    _clerk_owned()


@router.post("/logout", status_code=status.HTTP_410_GONE)
async def logout():
    _clerk_owned()


@router.post("/password-reset", status_code=status.HTTP_410_GONE)
async def request_password_reset():
    _clerk_owned()


@router.post("/password-update", status_code=status.HTTP_410_GONE)
async def update_password():
    _clerk_owned()
