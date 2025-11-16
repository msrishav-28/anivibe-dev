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
    
    # PostgreSQL Database
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "anivibe"
    postgres_password: str
    postgres_db: str = "anivibe_db"
    
    @property
    def database_url(self) -> str:
        """Construct async PostgreSQL database URL"""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    # MongoDB
    mongodb_host: str = "localhost"
    mongodb_port: int = 27017
    mongodb_user: str = "anivibe"
    mongodb_password: str
    mongodb_db: str = "anivibe_embeddings"
    
    @property
    def mongodb_url(self) -> str:
        """Construct MongoDB connection URL"""
        return (
            f"mongodb://{self.mongodb_user}:{self.mongodb_password}"
            f"@{self.mongodb_host}:{self.mongodb_port}/{self.mongodb_db}"
        )
    
    # Redis
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
    
    # External APIs
    jikan_api_url: str = "https://api.jikan.moe/v4"
    anilist_api_url: str = "https://graphql.anilist.co"
    gemini_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    
    # OAuth
    mal_client_id: Optional[str] = None
    mal_client_secret: Optional[str] = None
    anilist_client_id: Optional[str] = None
    anilist_client_secret: Optional[str] = None
    anilist_redirect_uri: str = "http://localhost:8000/api/v1/auth/anilist/callback"
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_burst: int = 20
    
    # ML Models
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
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/anivibe.log"
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    cors_allow_credentials: bool = True
    
    # File Upload
    max_upload_size: int = 10485760  # 10MB
    
    # Batch Processing
    batch_size: int = 32
    max_workers: int = 4
    
    # GPU
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
