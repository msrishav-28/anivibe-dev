"""
Generate anime text embeddings and store them in Postgres/pgvector.

This script is intended for offline jobs. Install `requirements-api.txt` and
`requirements-ml.txt`, set DATABASE_URL, then run:

    python scripts/generate_embeddings.py --limit 100
"""
import argparse
import asyncio
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parents[1]))

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core import database
from app.core.ml_models import check_ml_availability
from app.models.anime import Anime, AnimeEmbedding
from app.models.ops import DatasetVersion
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _anime_text(anime: Anime) -> str:
    parts = [anime.title]
    if anime.title_english:
        parts.append(anime.title_english)
    if anime.synopsis:
        parts.append(anime.synopsis)
    if anime.genres:
        parts.append("Genres: " + ", ".join(genre.name for genre in anime.genres))
    if anime.tags:
        parts.append("Tags: " + ", ".join(tag.name for tag in anime.tags[:20]))
    return ". ".join(part for part in parts if part)


async def _latest_dataset_version(session) -> str | None:
    result = await session.execute(
        select(DatasetVersion.version).order_by(DatasetVersion.created_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def _upsert_embedding(
    session,
    anime_id: int,
    embedding: list[float],
    model_name: str,
    model_version: str,
    dataset_version: str | None,
) -> None:
    result = await session.execute(
        select(AnimeEmbedding).filter(
            AnimeEmbedding.anime_id == anime_id,
            AnimeEmbedding.model_name == model_name,
            AnimeEmbedding.model_version == model_version,
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        existing.embedding = embedding
        existing.dimensions = len(embedding)
        existing.source_dataset_version = dataset_version
    else:
        session.add(
            AnimeEmbedding(
                anime_id=anime_id,
                model_name=model_name,
                model_version=model_version,
                dimensions=len(embedding),
                embedding=embedding,
                source_dataset_version=dataset_version,
            )
        )


async def generate_sbert_embeddings(
    limit: int | None,
    batch_size: int,
    model_version: str = "baseline",
    dataset_version: str | None = None,
) -> None:
    if not check_ml_availability():
        raise RuntimeError("ML dependencies are not installed. Install requirements-ml.txt first.")

    from sentence_transformers import SentenceTransformer

    await database.init_db()
    if database.AsyncSessionLocal is None:
        raise RuntimeError("Database is not initialized")

    model_name = settings.sbert_model_name
    model = SentenceTransformer(model_name, device=settings.device)

    async with database.AsyncSessionLocal() as session:
        query = (
            select(Anime)
            .options(selectinload(Anime.genres), selectinload(Anime.tags))
            .order_by(Anime.id)
        )
        if limit:
            query = query.limit(limit)

        anime_list = (await session.execute(query)).scalars().all()
        resolved_dataset_version = dataset_version or await _latest_dataset_version(session)
        logger.info("Generating SBERT embeddings for %s anime", len(anime_list))
        logger.info("Model: %s (%s), device: %s", model_name, model_version, settings.device)
        logger.info("Dataset version: %s", resolved_dataset_version or "unversioned")

        for start in range(0, len(anime_list), batch_size):
            batch = anime_list[start : start + batch_size]
            texts = [_anime_text(anime) for anime in batch]
            embeddings = model.encode(texts, normalize_embeddings=True).tolist()

            for anime, embedding in zip(batch, embeddings):
                await _upsert_embedding(
                    session,
                    anime.id,
                    embedding,
                    model_name,
                    model_version,
                    resolved_dataset_version,
                )

            await session.commit()
            logger.info("Processed %s/%s anime", min(start + batch_size, len(anime_list)), len(anime_list))

        embedding_count = (
            await session.execute(
                select(AnimeEmbedding)
                .filter(
                    AnimeEmbedding.model_name == model_name,
                    AnimeEmbedding.model_version == model_version,
                )
            )
        ).scalars().all()
        logger.info("Stored %s embeddings for %s/%s", len(embedding_count), model_name, model_version)

    await database.close_db()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate and store anime embeddings")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of anime to process")
    parser.add_argument("--batch-size", type=int, default=16, help="Embedding batch size")
    parser.add_argument("--model-version", default="baseline", help="Embedding model version label")
    parser.add_argument("--dataset-version", default=None, help="Dataset version label to attach to embeddings")
    args = parser.parse_args()

    asyncio.run(
        generate_sbert_embeddings(
            limit=args.limit,
            batch_size=args.batch_size,
            model_version=args.model_version,
            dataset_version=args.dataset_version,
        )
    )


if __name__ == "__main__":
    main()
