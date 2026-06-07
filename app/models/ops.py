"""
Operational, data lineage, and MLOps models.
"""
from datetime import datetime
import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.core.database import Base


class DatasetVersion(Base):
    __tablename__ = "dataset_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    version = Column(String(100), nullable=False, index=True)
    source = Column(String(100), nullable=False)
    source_url = Column(Text, nullable=True)
    record_count = Column(Integer, default=0, nullable=False)
    validation_failures = Column(JSONB, nullable=True)
    metadata_json = Column(JSONB, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class ModelVersion(Base):
    __tablename__ = "model_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_name = Column(String(100), nullable=False, index=True)
    model_version = Column(String(100), nullable=False, index=True)
    dataset_version = Column(String(100), nullable=True)
    metrics = Column(JSONB, nullable=True)
    artifact_uri = Column(Text, nullable=True)
    status = Column(String(30), default="candidate", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    promoted_at = Column(DateTime, nullable=True)


class RecommendationEvent(Base):
    __tablename__ = "recommendation_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    request_params = Column(JSONB, nullable=True)
    candidate_ids = Column(JSONB, nullable=False)
    scores = Column(JSONB, nullable=True)
    explanation_factors = Column(JSONB, nullable=True)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(100), nullable=False)
    latency_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class SearchEvent(Base):
    __tablename__ = "search_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True, index=True)
    query = Column(Text, nullable=False)
    search_type = Column(String(50), nullable=False)
    result_ids = Column(JSONB, nullable=False)
    model_name = Column(String(100), nullable=True)
    model_version = Column(String(100), nullable=True)
    fallback_used = Column(String(50), nullable=True)
    latency_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)


class InferenceLog(Base):
    __tablename__ = "inference_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    service_name = Column(String(100), nullable=False, index=True)
    model_name = Column(String(100), nullable=True)
    model_version = Column(String(100), nullable=True)
    input_summary = Column(JSONB, nullable=True)
    output_summary = Column(JSONB, nullable=True)
    fallback_used = Column(String(50), nullable=True)
    latency_ms = Column(Float, nullable=True)
    error_code = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
