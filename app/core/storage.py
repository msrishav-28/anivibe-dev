"""
Cloudflare R2 object storage helpers.
"""
from __future__ import annotations

import asyncio
import logging

from fastapi import HTTPException, UploadFile, status

from config import settings

logger = logging.getLogger(__name__)

ALLOWED_IMAGE_TYPES = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


def _r2_configured() -> bool:
    return all(
        [
            settings.r2_account_id,
            settings.r2_access_key_id,
            settings.r2_secret_access_key,
            settings.r2_bucket,
            settings.r2_public_base_url,
        ]
    )


def _build_client():
    import boto3

    return boto3.client(
        "s3",
        endpoint_url=f"https://{settings.r2_account_id}.r2.cloudflarestorage.com",
        aws_access_key_id=settings.r2_access_key_id,
        aws_secret_access_key=settings.r2_secret_access_key,
        region_name="auto",
    )


async def upload_avatar(user_id: str, avatar: UploadFile) -> str:
    """Validate and upload a user avatar to R2, returning the public URL."""
    if not _r2_configured():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="R2 storage is not configured",
        )

    content_type = avatar.content_type or ""
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar must be a JPEG, PNG, or WebP image",
        )

    content = await avatar.read()
    if len(content) > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Avatar exceeds maximum upload size",
        )

    ext = ALLOWED_IMAGE_TYPES[content_type]
    object_key = f"avatars/{user_id}/avatar.{ext}"
    client = _build_client()

    try:
        await asyncio.to_thread(
            client.put_object,
            Bucket=settings.r2_bucket,
            Key=object_key,
            Body=content,
            ContentType=content_type,
        )
    except Exception as exc:
        logger.error("R2 avatar upload failed: %s", exc)
        raise HTTPException(status_code=500, detail="Avatar upload failed") from exc

    return f"{settings.r2_public_base_url.rstrip('/')}/{object_key}"
