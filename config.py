"""
Application configuration.

The production target is Neon Postgres + Clerk + Cloudflare R2 + Upstash Redis.
Legacy provider-specific settings were intentionally removed from runtime config.
"""
from typing import List, Optional
import os

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    # Application
    app_name: str = "AniVibe"
    app_version: str = "1.0.0"
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "true").lower() == "true")
    api_v1_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))

    # Security / Clerk
    secret_key: str = Field(
        default_factory=lambda: os.getenv("SECRET_KEY", "insecure-development-key-change-me-32"),
        min_length=32,
    )
    clerk_issuer: Optional[str] = Field(default_factory=lambda: os.getenv("CLERK_ISSUER"))
    clerk_jwks_url: Optional[str] = Field(default_factory=lambda: os.getenv("CLERK_JWKS_URL"))
    clerk_secret_key: Optional[str] = Field(default_factory=lambda: os.getenv("CLERK_SECRET_KEY"))
    auth_required: bool = Field(default_factory=lambda: os.getenv("AUTH_REQUIRED", "true").lower() == "true")
    dev_auth_header: str = Field(default_factory=lambda: os.getenv("DEV_AUTH_HEADER", "X-AniVibe-Dev-User"))
    dev_auth_default_user: str = Field(default_factory=lambda: os.getenv("DEV_AUTH_DEFAULT_USER", "local-user"))

    # Database / Neon Postgres
    database_url: Optional[str] = Field(default_factory=lambda: os.getenv("DATABASE_URL"))
    database_migration_url: Optional[str] = Field(default_factory=lambda: os.getenv("DATABASE_MIGRATION_URL"))
    database_echo: bool = Field(default_factory=lambda: os.getenv("DATABASE_ECHO", "false").lower() == "true")
    database_pool_size: int = Field(default_factory=lambda: int(os.getenv("DATABASE_POOL_SIZE", "5")))
    database_max_overflow: int = Field(default_factory=lambda: int(os.getenv("DATABASE_MAX_OVERFLOW", "10")))

    @property
    def database_url_sync(self) -> Optional[str]:
        """Synchronous Postgres URL for Alembic migrations."""
        url = self.database_migration_url or self.database_url
        if not url:
            return None
        return url.replace("+asyncpg", "")

    # Redis / Upstash
    redis_url_env: Optional[str] = Field(default_factory=lambda: os.getenv("REDIS_URL"), alias="REDIS_URL")
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0
    redis_required: bool = Field(default_factory=lambda: os.getenv("REDIS_REQUIRED", "false").lower() == "true")
    cache_ttl: int = 3600

    @property
    def redis_url(self) -> str:
        if self.redis_url_env:
            return self.redis_url_env
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    # Cloudflare R2
    r2_account_id: Optional[str] = Field(default_factory=lambda: os.getenv("R2_ACCOUNT_ID"))
    r2_access_key_id: Optional[str] = Field(default_factory=lambda: os.getenv("R2_ACCESS_KEY_ID"))
    r2_secret_access_key: Optional[str] = Field(default_factory=lambda: os.getenv("R2_SECRET_ACCESS_KEY"))
    r2_bucket: Optional[str] = Field(default_factory=lambda: os.getenv("R2_BUCKET"))
    r2_public_base_url: Optional[str] = Field(default_factory=lambda: os.getenv("R2_PUBLIC_BASE_URL"))
    max_upload_size: int = 10 * 1024 * 1024

    # External APIs
    jikan_api_url: str = "https://api.jikan.moe/v4"
    anilist_api_url: str = "https://graphql.anilist.co"
    gemini_api_key: Optional[str] = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY"))
    mal_client_id: Optional[str] = Field(default_factory=lambda: os.getenv("MAL_CLIENT_ID"))
    mal_client_secret: Optional[str] = Field(default_factory=lambda: os.getenv("MAL_CLIENT_SECRET"))
    anilist_client_id: Optional[str] = Field(default_factory=lambda: os.getenv("ANILIST_CLIENT_ID"))
    anilist_client_secret: Optional[str] = Field(default_factory=lambda: os.getenv("ANILIST_CLIENT_SECRET"))

    # ML service
    ml_service_url: Optional[str] = Field(default_factory=lambda: os.getenv("ML_SERVICE_URL"))
    ml_service_timeout: int = 30
    enable_recommendations: bool = True
    enable_image_search: bool = Field(default_factory=lambda: os.getenv("ENABLE_IMAGE_SEARCH", "false").lower() == "true")
    enable_gnn: bool = Field(default=False)
    enable_bert4rec: bool = Field(default=False)
    use_gpu: bool = Field(default=False)
    gpu_device: str = Field(default_factory=lambda: os.getenv("GPU_DEVICE", "cuda:0"))
    model_cache_dir: str = "./models/cache"
    sbert_model_name: str = "all-MiniLM-L6-v2"
    clip_model_name: str = "ViT-B-32"
    clip_pretrained: str = "openai"
    sentiment_model_name: str = "distilbert-base-uncased"

    @property
    def device(self) -> str:
        if not self.use_gpu:
            return "cpu"
        try:
            import torch

            return "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            return "cpu"

    # Rate limiting
    rate_limit_enabled: bool = Field(default_factory=lambda: os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true")
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 20

    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/anivibe.log"
    log_json: bool = Field(default_factory=lambda: os.getenv("LOG_JSON", "false").lower() == "true")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000", "https://anivibe.vercel.app"]
    )
    cors_allow_credentials: bool = True

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value):
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"


settings = Settings()
