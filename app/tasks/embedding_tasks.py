"""
Embedding job entrypoints.

These are intentionally not Celery tasks. Run the offline script directly or
wire these functions into a future worker service.
"""
import asyncio

from scripts.generate_embeddings import generate_sbert_embeddings


def generate_sbert_embeddings_job(limit: int | None = None, batch_size: int = 32) -> None:
    asyncio.run(generate_sbert_embeddings(limit=limit, batch_size=batch_size))
