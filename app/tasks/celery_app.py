"""
Celery application configuration for background tasks
"""
from celery import Celery
from config import settings

# Create Celery app
celery_app = Celery(
    "anivibe",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=[
        "app.tasks.embedding_tasks",
        "app.tasks.recommendation_tasks",
        "app.tasks.data_tasks"
    ]
)

# Configure Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour
    task_soft_time_limit=3000,  # 50 minutes
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)

# Task routes
celery_app.conf.task_routes = {
    "app.tasks.embedding_tasks.*": {"queue": "embeddings"},
    "app.tasks.recommendation_tasks.*": {"queue": "recommendations"},
    "app.tasks.data_tasks.*": {"queue": "data"},
}
