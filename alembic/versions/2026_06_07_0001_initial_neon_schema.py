"""Initial Neon/Postgres schema

Revision ID: 2026_06_07_0001
Revises:
Create Date: 2026-06-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from pgvector.sqlalchemy import Vector

revision: str = "2026_06_07_0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


anime_type = postgresql.ENUM("TV", "MOVIE", "OVA", "ONA", "SPECIAL", "MUSIC", name="animetype")
anime_status = postgresql.ENUM("FINISHED", "AIRING", "NOT_YET", name="animestatus")
anime_season = postgresql.ENUM("WINTER", "SPRING", "SUMMER", "FALL", name="animeseason")


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    anime_type.create(op.get_bind(), checkfirst=True)
    anime_status.create(op.get_bind(), checkfirst=True)
    anime_season.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("external_auth_id", sa.String(255), nullable=True),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(100), nullable=True),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("mal_username", sa.String(100), nullable=True),
        sa.Column("mal_user_id", sa.Integer(), nullable=True),
        sa.Column("anilist_username", sa.String(100), nullable=True),
        sa.Column("anilist_user_id", sa.Integer(), nullable=True),
        sa.Column("preferred_language", sa.String(10), nullable=True, server_default="en"),
        sa.Column("show_nsfw", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("anime_watched", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("episodes_watched", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("watch_time_hours", sa.Float(), nullable=True, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("last_login", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_profiles_external_auth_id", "profiles", ["external_auth_id"], unique=True)
    op.create_index("ix_profiles_username", "profiles", ["username"], unique=True)
    op.create_index("ix_profiles_email", "profiles", ["email"])

    op.create_table(
        "anime",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("title_english", sa.String(500), nullable=True),
        sa.Column("title_japanese", sa.String(500), nullable=True),
        sa.Column("title_synonyms", sa.Text(), nullable=True),
        sa.Column("mal_id", sa.Integer(), nullable=True),
        sa.Column("anilist_id", sa.Integer(), nullable=True),
        sa.Column("synopsis", sa.Text(), nullable=True),
        sa.Column("background", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(500), nullable=True),
        sa.Column("trailer_url", sa.String(500), nullable=True),
        sa.Column("type", anime_type, nullable=True),
        sa.Column("status", anime_status, nullable=True),
        sa.Column("episodes", sa.Integer(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=True),
        sa.Column("aired_from", sa.DateTime(), nullable=True),
        sa.Column("aired_to", sa.DateTime(), nullable=True),
        sa.Column("season", anime_season, nullable=True),
        sa.Column("year", sa.Integer(), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("scored_by", sa.Integer(), nullable=True),
        sa.Column("rank", sa.Integer(), nullable=True),
        sa.Column("popularity", sa.Integer(), nullable=True),
        sa.Column("members", sa.Integer(), nullable=True),
        sa.Column("favorites", sa.Integer(), nullable=True),
        sa.Column("rating", sa.String(50), nullable=True),
        sa.Column("source", sa.String(100), nullable=True),
        sa.Column("is_nsfw", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("is_hidden_gem", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("popularity_score", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("last_synced", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_anime_title", "anime", ["title"])
    op.create_index("ix_anime_year", "anime", ["year"])
    op.create_index("ix_anime_score", "anime", ["score"])
    op.create_index("ix_anime_members", "anime", ["members"])
    op.create_index("ix_anime_popularity", "anime", ["popularity"])
    op.create_index("ix_anime_mal_id", "anime", ["mal_id"], unique=True)
    op.create_index("ix_anime_anilist_id", "anime", ["anilist_id"], unique=True)

    op.create_table(
        "genres",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("mal_id", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
    )
    op.create_index("ix_genres_name", "genres", ["name"], unique=True)
    op.create_index("ix_genres_mal_id", "genres", ["mal_id"], unique=True)

    op.create_table(
        "studios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("mal_id", sa.Integer(), nullable=True),
        sa.Column("established", sa.Integer(), nullable=True),
    )
    op.create_index("ix_studios_name", "studios", ["name"], unique=True)
    op.create_index("ix_studios_mal_id", "studios", ["mal_id"], unique=True)

    op.create_table(
        "tags",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("category", sa.String(50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("anilist_id", sa.Integer(), nullable=True),
    )
    op.create_index("ix_tags_name", "tags", ["name"], unique=True)
    op.create_index("ix_tags_anilist_id", "tags", ["anilist_id"], unique=True)

    op.create_table(
        "anime_genres",
        sa.Column("anime_id", sa.Integer(), sa.ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("genre_id", sa.Integer(), sa.ForeignKey("genres.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "anime_studios",
        sa.Column("anime_id", sa.Integer(), sa.ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("studio_id", sa.Integer(), sa.ForeignKey("studios.id", ondelete="CASCADE"), primary_key=True),
    )
    op.create_table(
        "anime_tags",
        sa.Column("anime_id", sa.Integer(), sa.ForeignKey("anime.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tag_id", sa.Integer(), sa.ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "anime_embeddings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("anime_id", sa.Integer(), sa.ForeignKey("anime.id", ondelete="CASCADE"), nullable=False),
        sa.Column("model_name", sa.String(100), nullable=False),
        sa.Column("model_version", sa.String(100), nullable=False),
        sa.Column("dimensions", sa.Integer(), nullable=False),
        sa.Column("embedding", Vector(), nullable=False),
        sa.Column("source_dataset_version", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("anime_id", "model_name", "model_version", name="uq_anime_embedding_version"),
    )
    op.create_index("ix_anime_embeddings_anime_id", "anime_embeddings", ["anime_id"])
    op.create_index("ix_anime_embeddings_model", "anime_embeddings", ["model_name", "model_version"])

    op.create_table(
        "ratings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("anime_id", sa.Integer(), sa.ForeignKey("anime.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("review", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "anime_id", name="unique_user_anime_rating"),
    )
    op.create_index("ix_ratings_user_id", "ratings", ["user_id"])
    op.create_index("ix_ratings_anime_id", "ratings", ["anime_id"])

    op.create_table(
        "watchlist_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("anime_id", sa.Integer(), sa.ForeignKey("anime.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="plan_to_watch"),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("user_id", "anime_id", name="unique_user_anime_watchlist"),
    )
    op.create_index("ix_watchlist_entries_user_id", "watchlist_entries", ["user_id"])
    op.create_index("ix_watchlist_entries_anime_id", "watchlist_entries", ["anime_id"])

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("anime_id", sa.Integer(), sa.ForeignKey("anime.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(200), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("sentiment", sa.String(20), nullable=True),
        sa.Column("helpful_count", sa.Integer(), nullable=True, server_default="0"),
        sa.Column("is_spoiler", sa.Boolean(), nullable=True, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
    )
    op.create_index("ix_reviews_user_id", "reviews", ["user_id"])
    op.create_index("ix_reviews_anime_id", "reviews", ["anime_id"])

    op.create_table(
        "review_votes",
        sa.Column("review_id", sa.Integer(), sa.ForeignKey("reviews.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("is_helpful", sa.Boolean(), nullable=True, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True, server_default=sa.func.now()),
    )

    op.create_table(
        "dataset_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("version", sa.String(100), nullable=False),
        sa.Column("source", sa.String(100), nullable=False),
        sa.Column("source_url", sa.Text(), nullable=True),
        sa.Column("record_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("validation_failures", postgresql.JSONB(), nullable=True),
        sa.Column("metadata_json", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_dataset_versions_name", "dataset_versions", ["name"])
    op.create_index("ix_dataset_versions_version", "dataset_versions", ["version"])

    op.create_table(
        "model_versions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("model_name", sa.String(100), nullable=False),
        sa.Column("model_version", sa.String(100), nullable=False),
        sa.Column("dataset_version", sa.String(100), nullable=True),
        sa.Column("metrics", postgresql.JSONB(), nullable=True),
        sa.Column("artifact_uri", sa.Text(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="candidate"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("promoted_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_model_versions_model_name", "model_versions", ["model_name"])
    op.create_index("ix_model_versions_model_version", "model_versions", ["model_version"])

    op.create_table(
        "recommendation_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True),
        sa.Column("request_params", postgresql.JSONB(), nullable=True),
        sa.Column("candidate_ids", postgresql.JSONB(), nullable=False),
        sa.Column("scores", postgresql.JSONB(), nullable=True),
        sa.Column("explanation_factors", postgresql.JSONB(), nullable=True),
        sa.Column("model_name", sa.String(100), nullable=False),
        sa.Column("model_version", sa.String(100), nullable=False),
        sa.Column("latency_ms", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_recommendation_events_user_id", "recommendation_events", ["user_id"])
    op.create_index("ix_recommendation_events_created_at", "recommendation_events", ["created_at"])

    op.create_table(
        "search_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("profiles.id", ondelete="SET NULL"), nullable=True),
        sa.Column("query", sa.Text(), nullable=False),
        sa.Column("search_type", sa.String(50), nullable=False),
        sa.Column("result_ids", postgresql.JSONB(), nullable=False),
        sa.Column("model_name", sa.String(100), nullable=True),
        sa.Column("model_version", sa.String(100), nullable=True),
        sa.Column("fallback_used", sa.String(50), nullable=True),
        sa.Column("latency_ms", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_search_events_user_id", "search_events", ["user_id"])
    op.create_index("ix_search_events_created_at", "search_events", ["created_at"])

    op.create_table(
        "inference_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("service_name", sa.String(100), nullable=False),
        sa.Column("model_name", sa.String(100), nullable=True),
        sa.Column("model_version", sa.String(100), nullable=True),
        sa.Column("input_summary", postgresql.JSONB(), nullable=True),
        sa.Column("output_summary", postgresql.JSONB(), nullable=True),
        sa.Column("fallback_used", sa.String(50), nullable=True),
        sa.Column("latency_ms", sa.Float(), nullable=True),
        sa.Column("error_code", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("ix_inference_logs_service_name", "inference_logs", ["service_name"])
    op.create_index("ix_inference_logs_created_at", "inference_logs", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_inference_logs_created_at", table_name="inference_logs")
    op.drop_index("ix_inference_logs_service_name", table_name="inference_logs")
    op.drop_table("inference_logs")
    op.drop_index("ix_search_events_created_at", table_name="search_events")
    op.drop_index("ix_search_events_user_id", table_name="search_events")
    op.drop_table("search_events")
    op.drop_index("ix_recommendation_events_created_at", table_name="recommendation_events")
    op.drop_index("ix_recommendation_events_user_id", table_name="recommendation_events")
    op.drop_table("recommendation_events")
    op.drop_index("ix_model_versions_model_version", table_name="model_versions")
    op.drop_index("ix_model_versions_model_name", table_name="model_versions")
    op.drop_table("model_versions")
    op.drop_index("ix_dataset_versions_version", table_name="dataset_versions")
    op.drop_index("ix_dataset_versions_name", table_name="dataset_versions")
    op.drop_table("dataset_versions")
    op.drop_table("review_votes")
    op.drop_index("ix_reviews_anime_id", table_name="reviews")
    op.drop_index("ix_reviews_user_id", table_name="reviews")
    op.drop_table("reviews")
    op.drop_index("ix_watchlist_entries_anime_id", table_name="watchlist_entries")
    op.drop_index("ix_watchlist_entries_user_id", table_name="watchlist_entries")
    op.drop_table("watchlist_entries")
    op.drop_index("ix_ratings_anime_id", table_name="ratings")
    op.drop_index("ix_ratings_user_id", table_name="ratings")
    op.drop_table("ratings")
    op.drop_index("ix_anime_embeddings_model", table_name="anime_embeddings")
    op.drop_index("ix_anime_embeddings_anime_id", table_name="anime_embeddings")
    op.drop_table("anime_embeddings")
    op.drop_table("anime_tags")
    op.drop_table("anime_studios")
    op.drop_table("anime_genres")
    op.drop_index("ix_tags_anilist_id", table_name="tags")
    op.drop_index("ix_tags_name", table_name="tags")
    op.drop_table("tags")
    op.drop_index("ix_studios_mal_id", table_name="studios")
    op.drop_index("ix_studios_name", table_name="studios")
    op.drop_table("studios")
    op.drop_index("ix_genres_mal_id", table_name="genres")
    op.drop_index("ix_genres_name", table_name="genres")
    op.drop_table("genres")
    op.drop_index("ix_anime_anilist_id", table_name="anime")
    op.drop_index("ix_anime_mal_id", table_name="anime")
    op.drop_index("ix_anime_popularity", table_name="anime")
    op.drop_index("ix_anime_members", table_name="anime")
    op.drop_index("ix_anime_score", table_name="anime")
    op.drop_index("ix_anime_year", table_name="anime")
    op.drop_index("ix_anime_title", table_name="anime")
    op.drop_table("anime")
    op.drop_index("ix_profiles_email", table_name="profiles")
    op.drop_index("ix_profiles_username", table_name="profiles")
    op.drop_index("ix_profiles_external_auth_id", table_name="profiles")
    op.drop_table("profiles")
    anime_season.drop(op.get_bind(), checkfirst=True)
    anime_status.drop(op.get_bind(), checkfirst=True)
    anime_type.drop(op.get_bind(), checkfirst=True)
