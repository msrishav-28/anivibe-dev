"""
Application configuration management using Pydantic Settings
"""
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow"
    )
    
    # Application
    app_name: str = "AniVibe"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    api_v1_prefix: str = "/api/v1"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    
    # Security
    secret_key: str = Field(..., min_length=32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # ===========================================
    # SUPABASE CONFIGURATION
    # ===========================================
    supabase_url: str = Field(..., description="Supabase project URL")
    supabase_anon_key: str = Field(..., description="Supabase anon/public key")
    supabase_service_key: str = Field(..., description="Supabase service role key (server-side only)")
    
    @property
    def database_url(self) -> str:
        """Construct Supabase PostgreSQL connection URL via pooler"""
        # Extract project ref from URL (e.g., "xxxxx" from "https://xxxxx.supabase.co")
        project_ref = self.supabase_url.replace("https://", "").split(".")[0]
        # Use transaction pooler for better connection management
        # Password is the service key for direct database access
        return (
            f"postgresql+asyncpg://postgres.{project_ref}:{self.supabase_service_key}"
            f"@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"
        )
    
    # ===========================================
    # REDIS CONFIGURATION
    # ===========================================
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: Optional[str] = None
    redis_db: int = 0
    
    @property
    def redis_url(self) -> str:
        """Construct Redis URL"""
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"redis://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # ===========================================
    # EXTERNAL APIS
    # ===========================================
    jikan_api_url: str = "https://api.jikan.moe/v4"
    anilist_api_url: str = "https://graphql.anilist.co"
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # OAuth (for MAL/AniList integration)
    mal_client_id: Optional[str] = None
    mal_client_secret: Optional[str] = None
    anilist_client_id: Optional[str] = None
    anilist_client_secret: Optional[str] = None
    anilist_redirect_uri: str = "http://localhost:8000/api/v1/auth/anilist/callback"
    
    # ===========================================
    # RATE LIMITING
    # ===========================================
    rate_limit_per_minute: int = 100
    rate_limit_burst: int = 20
    
    # ===========================================
    # ML MODELS CONFIGURATION
    # ===========================================
    model_cache_dir: str = "./models/cache"
    embeddings_dir: str = "./data/embeddings"
    
    # CLIP
    clip_model_name: str = "ViT-B-32"
    clip_pretrained: str = "openai"
    
    # BERT
    sbert_model_name: str = "all-mpnet-base-v2"
    
    # Sentiment
    sentiment_model_name: str = "distilbert-base-uncased"
    
    # FAISS
    faiss_index_path: str = "./data/faiss_indexes"
    faiss_nlist: int = 100
    
    # Recommendations
    top_k_recommendations: int = 10
    similarity_threshold: float = 0.5
    popularity_attenuation_factor: float = 0.3
    
    # MLflow
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_experiment_name: str = "anivibe-experiments"
    
    # ===========================================
    # LOGGING
    # ===========================================
    log_level: str = "INFO"
    log_file: str = "logs/anivibe.log"
    
    # ===========================================
    # CORS
    # ===========================================
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    
    # ===========================================
    # FILE UPLOAD
    # ===========================================
    max_upload_size: int = 10485760  # 10MB
    
    # ===========================================
    # BATCH PROCESSING
    # ===========================================
    batch_size: int = 32
    max_workers: int = 4
    
    # ===========================================
    # GPU
    # ===========================================
    use_gpu: bool = True
    gpu_device: str = "cuda:0"
    
    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment.lower() == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()
