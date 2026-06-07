"""
Generate and evaluate local CLIP poster embeddings for visual search.

This is an offline development script. Keep ENABLE_IMAGE_SEARCH=false until the
report generated here meets the product gate.
"""
from __future__ import annotations

import argparse
import asyncio
from dataclasses import dataclass
import io
import json
import logging
from pathlib import Path
import statistics
import sys
import time
from typing import Dict, Iterable, List

import httpx
from sqlalchemy import select, text
from sqlalchemy.orm import selectinload

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.core import database
from app.models.anime import Anime, AnimeEmbedding
from app.models.ops import DatasetVersion
from config import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@dataclass(frozen=True)
class PosterItem:
    anime: Anime
    path: Path


def clip_model_key() -> str:
    return f"clip-{settings.clip_model_name}-{settings.clip_pretrained}"


def poster_path(cache_dir: Path, anime: Anime) -> Path:
    external_id = anime.mal_id or anime.id
    return cache_dir / f"{anime.id}-{external_id}.jpg"


async def latest_dataset_version(session) -> str | None:
    result = await session.execute(
        select(DatasetVersion.version).order_by(DatasetVersion.created_at.desc()).limit(1)
    )
    return result.scalar_one_or_none()


async def fetch_anime_with_posters(session, limit: int) -> List[Anime]:
    result = await session.execute(
        select(Anime)
        .options(selectinload(Anime.genres))
        .where(Anime.image_url.is_not(None))
        .order_by(Anime.id)
        .limit(limit)
    )
    return list(result.scalars().all())


async def download_posters(anime_list: Iterable[Anime], cache_dir: Path) -> List[PosterItem]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    items: List[PosterItem] = []
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
        for anime in anime_list:
            path = poster_path(cache_dir, anime)
            if path.exists() and path.stat().st_size > 0:
                items.append(PosterItem(anime=anime, path=path))
                continue
            try:
                response = await client.get(anime.image_url)
                response.raise_for_status()
                path.write_bytes(response.content)
                items.append(PosterItem(anime=anime, path=path))
            except Exception as exc:
                logger.warning("Poster download failed for %s: %s", anime.id, exc)
    return items


def load_clip():
    import open_clip
    import torch

    device = settings.device
    model, _, preprocess = open_clip.create_model_and_transforms(
        settings.clip_model_name,
        pretrained=settings.clip_pretrained,
        device=device,
    )
    model.eval()
    return model, preprocess, torch, device


def iter_batches(items: List[PosterItem], batch_size: int):
    for start in range(0, len(items), batch_size):
        yield items[start : start + batch_size]


async def upsert_embedding(
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
        return

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


async def generate_clip_embeddings(limit: int, batch_size: int, cache_dir: Path, model_version: str) -> int:
    await database.init_db()
    if database.AsyncSessionLocal is None:
        raise RuntimeError("Database is not initialized")

    model_name = clip_model_key()
    model, preprocess, torch, device = load_clip()
    generated = 0

    async with database.AsyncSessionLocal() as session:
        dataset_version = await latest_dataset_version(session)
        anime_list = await fetch_anime_with_posters(session, limit)
        poster_items = await download_posters(anime_list, cache_dir)
        logger.info("Generating %s poster embeddings with %s on %s", len(poster_items), model_name, device)

        from PIL import Image

        for batch in iter_batches(poster_items, batch_size):
            images = []
            valid_items = []
            for item in batch:
                try:
                    with Image.open(item.path) as image:
                        images.append(preprocess(image.convert("RGB")))
                    valid_items.append(item)
                except Exception as exc:
                    logger.warning("Poster decode failed for %s: %s", item.anime.id, exc)

            if not images:
                continue

            with torch.no_grad():
                tensor = torch.stack(images).to(device)
                embeddings = model.encode_image(tensor)
                embeddings = embeddings / embeddings.norm(dim=-1, keepdim=True)

            for item, embedding in zip(valid_items, embeddings.cpu().tolist()):
                await upsert_embedding(
                    session,
                    item.anime.id,
                    embedding,
                    model_name,
                    model_version,
                    dataset_version,
                )
                generated += 1
            await session.commit()
            logger.info("Generated %s/%s CLIP poster embeddings", generated, len(poster_items))

    await database.close_db()
    return generated


def make_variant_bytes(path: Path, variant: str) -> bytes:
    from PIL import Image

    with Image.open(path) as image:
        image = image.convert("RGB")
        if variant == "cropped":
            width, height = image.size
            margin_x = int(width * 0.08)
            margin_y = int(height * 0.08)
            image = image.crop((margin_x, margin_y, width - margin_x, height - margin_y))
        elif variant == "compressed":
            image = image.resize((max(image.width // 2, 64), max(image.height // 2, 64)))

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=60 if variant == "compressed" else 90)
        return buffer.getvalue()


def encode_image_bytes(image_bytes: bytes, model, preprocess, torch, device) -> list[float]:
    from PIL import Image

    with Image.open(io.BytesIO(image_bytes)) as image:
        tensor = preprocess(image.convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(tensor)
        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
    return embedding.cpu().tolist()[0]


async def query_visual_neighbors(session, embedding: list[float], model_name: str, model_version: str, limit: int) -> list[int]:
    result = await session.execute(
        text(
            """
            SELECT anime_id
            FROM anime_embeddings
            WHERE model_name = :model_name
              AND model_version = :model_version
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
            """
        ),
        {
            "model_name": model_name,
            "model_version": model_version,
            "embedding": str(embedding),
            "limit": limit,
        },
    )
    return [row[0] for row in result.fetchall()]


def empty_variant_metrics() -> Dict[str, object]:
    return {
        "queries": 0,
        "recall_at_1": 0.0,
        "recall_at_5": 0.0,
        "recall_at_10": 0.0,
        "median_latency_ms": 0.0,
        "p95_latency_ms": 0.0,
        "failure_examples": [],
    }


async def evaluate_visual_search(limit: int, cache_dir: Path, model_version: str, report_file: Path) -> Dict[str, object]:
    await database.init_db()
    if database.AsyncSessionLocal is None:
        raise RuntimeError("Database is not initialized")

    model_name = clip_model_key()
    model, preprocess, torch, device = load_clip()
    variants = ("exact", "cropped", "compressed")
    totals = {
        variant: {"queries": 0, "r1": 0, "r5": 0, "r10": 0, "latencies": [], "failures": []}
        for variant in variants
    }

    async with database.AsyncSessionLocal() as session:
        anime_list = await fetch_anime_with_posters(session, limit)
        poster_items = [PosterItem(anime=anime, path=poster_path(cache_dir, anime)) for anime in anime_list]
        poster_items = [item for item in poster_items if item.path.exists()]

        for item in poster_items:
            for variant in variants:
                try:
                    image_bytes = item.path.read_bytes() if variant == "exact" else make_variant_bytes(item.path, variant)
                    embedding = encode_image_bytes(image_bytes, model, preprocess, torch, device)
                    start = time.perf_counter()
                    neighbors = await query_visual_neighbors(session, embedding, model_name, model_version, 10)
                    latency_ms = (time.perf_counter() - start) * 1000
                except Exception as exc:
                    logger.warning("Visual query failed for %s/%s: %s", item.anime.id, variant, exc)
                    continue

                bucket = totals[variant]
                bucket["queries"] += 1
                bucket["latencies"].append(latency_ms)
                if neighbors[:1] == [item.anime.id]:
                    bucket["r1"] += 1
                if item.anime.id in neighbors[:5]:
                    bucket["r5"] += 1
                if item.anime.id in neighbors[:10]:
                    bucket["r10"] += 1
                if item.anime.id not in neighbors[:5] and len(bucket["failures"]) < 10:
                    bucket["failures"].append(
                        {
                            "anime_id": item.anime.id,
                            "title": item.anime.title,
                            "variant": variant,
                            "retrieved_ids": neighbors[:5],
                        }
                    )

    report_variants: Dict[str, object] = {}
    for variant, bucket in totals.items():
        queries = bucket["queries"]
        if not queries:
            report_variants[variant] = empty_variant_metrics()
            continue
        latencies = bucket["latencies"]
        p95_index = max(int(len(latencies) * 0.95) - 1, 0)
        report_variants[variant] = {
            "queries": queries,
            "recall_at_1": bucket["r1"] / queries,
            "recall_at_5": bucket["r5"] / queries,
            "recall_at_10": bucket["r10"] / queries,
            "median_latency_ms": statistics.median(latencies),
            "p95_latency_ms": sorted(latencies)[p95_index],
            "failure_examples": bucket["failures"],
        }

    exact_r1 = report_variants["exact"]["recall_at_1"]
    augmented_r5 = min(
        report_variants["cropped"]["recall_at_5"],
        report_variants["compressed"]["recall_at_5"],
    )
    report = {
        "model_name": model_name,
        "model_version": model_version,
        "device": device,
        "limit": limit,
        "feature_flag_should_enable": bool(exact_r1 >= 0.98 and augmented_r5 >= 0.90),
        "gate": {
            "exact_recall_at_1_min": 0.98,
            "augmented_recall_at_5_min": 0.90,
            "exact_recall_at_1": exact_r1,
            "augmented_recall_at_5": augmented_r5,
        },
        "variants": report_variants,
    }
    report_file.parent.mkdir(parents=True, exist_ok=True)
    report_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    await database.close_db()
    return report


async def main() -> None:
    parser = argparse.ArgumentParser(description="Generate/evaluate local CLIP poster visual search")
    parser.add_argument("--limit", type=int, default=250, help="Number of poster-backed anime to use")
    parser.add_argument("--batch-size", type=int, default=8, help="CLIP image embedding batch size")
    parser.add_argument("--cache-dir", type=Path, default=Path("data/posters"), help="Poster cache directory")
    parser.add_argument("--model-version", default="poster-baseline", help="CLIP poster model version label")
    parser.add_argument("--report-file", type=Path, default=Path("reports/visual_search_eval.json"))
    parser.add_argument("--generate", action="store_true", help="Download posters and generate CLIP embeddings")
    parser.add_argument("--evaluate", action="store_true", help="Run poster retrieval evaluation")
    args = parser.parse_args()

    if not args.generate and not args.evaluate:
        args.generate = True
        args.evaluate = True

    if args.generate:
        generated = await generate_clip_embeddings(args.limit, args.batch_size, args.cache_dir, args.model_version)
        logger.info("Generated or updated %s CLIP poster embeddings", generated)

    if args.evaluate:
        report = await evaluate_visual_search(args.limit, args.cache_dir, args.model_version, args.report_file)
        logger.info("Visual search report written to %s", args.report_file)
        logger.info("Feature flag should enable: %s", report["feature_flag_should_enable"])


if __name__ == "__main__":
    asyncio.run(main())
