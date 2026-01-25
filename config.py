"""
Pure Supabase configuration
"""
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings - Supabase only"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # ==========================================
    # APPLICATION
    # ==========================================
    app_name: str = "AniVibe"
    app_version: str = "1.0.0"
    environment: str = Field(default="development")
    debug: bool = Field(default=True)
    api_v1_prefix: str = "/api/v1"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # ==========================================
    # SECURITY
    # ==========================================
    secret_key: str = Field(..., min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # ==========================================
    # SUPABASE (Single Source of Truth)
    # ==========================================
    supabase_url: str = Field(..., description="https://xxxxx.supabase.co")
    supabase_anon_key: str = Field(..., description="Public anon key")
    supabase_service_key: str = Field(..., description="Service role key (server only)")
    
    @property
    def database_url(self) -> str:
        """
        Supabase PostgreSQL connection via Supavisor pooler.
        Uses session mode for better connection pooling.
        """
        project_ref = self.supabase_url.replace("https://", "").split(".")[0]
        
        # Session pooler (port 5432) for app connections
        return (
            f"postgresql+asyncpg://postgres.{project_ref}:"
            f"{self.supabase_service_key}@"
            f"aws-0-ap-south-1.pooler.supabase.com:5432/postgres"
        )
    
    @property 
    def database_url_sync(self) -> str:
        """Synchronous connection for Alembic migrations"""
        project_ref = self.supabase_url.replace("https://", "").split(".")[0]
        
        # Transaction pooler (port 6543) for migrations
        return (
            f"postgresql://postgres.{project_ref}:"
            f"{self.supabase_service_key}@"
            f"aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
        )
    
    # ==========================================
    # REDIS (Caching Only)
    # ==========================================
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0
    cache_ttl: int = 3600  # 1 hour default
    
    @property
    def redis_url(self) -> str:
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # ==========================================
    # EXTERNAL APIs
    # ==========================================
    jikan_api_url: str = "https://api.jikan.moe/v4"
    anilist_api_url: str = "https://graphql.anilist.co"
    gemini_api_key: Optional[str] = None
    
    # OAuth
    mal_client_id: Optional[str] = None
    mal_client_secret: Optional[str] = None
    anilist_client_id: Optional[str] = None
    anilist_client_secret: Optional[str] = None
    
    # ==========================================
    # ML SERVICE (Separate Microservice)
    # ==========================================
    ml_service_url: str = Field(
        default="http://localhost:8080",
        description="Modal/HuggingFace ML endpoint"
    )
    ml_service_timeout: int = 30
    
    # Feature Toggles (Enable progressively)
    enable_recommendations: bool = True
    enable_image_search: bool = Field(default=False)
    enable_gnn: bool = Field(default=False)
    enable_bert4rec: bool = Field(default=False)
    
    # ML Model Config
    use_gpu: bool = Field(default=False)
    model_cache_dir: str = "./models/cache"
    
    @property
    def device(self) -> str:
        """Auto-detect GPU availability"""
        if not self.use_gpu:
            return "cpu"
        
        try:
            import torch
            return "cuda" if torch.cuda.is_available() else "cpu"
        except ImportError:
            return "cpu"
    
    # Lightweight models (SBERT can run in main app)
    sbert_model_name: str = "all-MiniLM-L6-v2"  # 80MB only
    
    # Heavy models (CLIP, GNN) - offload to Modal
    clip_model_name: str = "ViT-B-32"
    
    # ==========================================
    # RATE LIMITING
    # ==========================================
    rate_limit_per_minute: int = 60
    rate_limit_burst: int = 20
    
    # ==========================================
    # LOGGING
    # ==========================================
    log_level: str = "INFO"
    log_file: str = "logs/anivibe.log"
    
    # ==========================================
    # CORS
    # ==========================================
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )
    cors_allow_credentials: bool = True
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # ==========================================
    # FILE STORAGE (Supabase Storage)
    # ==========================================
    supabase_storage_bucket: str = "anime-images"
    max_upload_size: int = 10485760  # 10MB
    
    # ==========================================
    # PROPERTIES
    # ==========================================
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
