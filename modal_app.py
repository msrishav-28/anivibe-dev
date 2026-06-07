"""
Modal ML service for AniVibe.

Deploy: modal deploy modal_app.py
Local test: modal run modal_app.py
"""
import os

import modal

app = modal.App("anivibe-ml")

image = (
    modal.Image.debian_slim(python_version="3.10")
    .pip_install(
        "torch",
        "torchvision",
        "transformers",
        "sentence-transformers",
        "open-clip-torch",
        "pillow",
        "numpy",
        "psycopg2-binary",
        "pgvector",
        "fastapi",
    )
)

secrets = [
    modal.Secret.from_name("anivibe-production"),  # DATABASE_URL
]


def _sync_database_url() -> str:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is not configured")
    return database_url.replace("postgresql+asyncpg://", "postgresql://")


def _query_pgvector(embedding: list[float], model_name: str, limit: int) -> list[dict]:
    import psycopg2
    import psycopg2.extras

    embedding_text = str(embedding)
    sql = """
        SELECT
            a.id AS anime_id,
            a.title,
            a.image_url,
            1 - (ae.embedding <=> %s::vector) AS similarity
        FROM anime_embeddings ae
        JOIN anime a ON a.id = ae.anime_id
        WHERE ae.model_name = %s
        ORDER BY ae.embedding <=> %s::vector
        LIMIT %s
    """

    with psycopg2.connect(_sync_database_url()) as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(sql, (embedding_text, model_name, embedding_text, limit))
            rows = cursor.fetchall()

    return [
        {
            "anime_id": row["anime_id"],
            "title": row["title"],
            "image_url": row["image_url"],
            "similarity": float(row["similarity"]),
        }
        for row in rows
    ]


@app.function(image=image, secrets=secrets, gpu="T4", timeout=300, container_idle_timeout=60)
@modal.web_endpoint(method="POST")
def clip_image_search(request: dict):
    """Search anime poster embeddings with a CLIP image embedding."""
    import base64
    from io import BytesIO

    import open_clip
    import torch
    from PIL import Image

    image_base64 = request.get("image_base64")
    if not image_base64:
        return {"results": [], "model_name": "ViT-B-32", "model_version": "openai", "fallback_used": "missing_image"}

    try:
        if "base64," in image_base64:
            image_base64 = image_base64.split("base64,", 1)[1]
        image = Image.open(BytesIO(base64.b64decode(image_base64))).convert("RGB")
    except Exception as exc:
        return {
            "results": [],
            "model_name": "ViT-B-32",
            "model_version": "openai",
            "fallback_used": "invalid_image",
            "error": str(exc),
        }

    model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
    model.eval()

    with torch.no_grad():
        image_tensor = preprocess(image).unsqueeze(0)
        image_embedding = model.encode_image(image_tensor)
        image_embedding = image_embedding / image_embedding.norm(dim=-1, keepdim=True)
        embedding = image_embedding.cpu().numpy()[0].tolist()

    try:
        results = _query_pgvector(embedding, "ViT-B-32", int(request.get("limit", 20)))
    except Exception as exc:
        return {
            "results": [],
            "model_name": "ViT-B-32",
            "model_version": "openai",
            "fallback_used": "database_unavailable",
            "error": str(exc),
        }

    return {
        "results": results,
        "model_name": "ViT-B-32",
        "model_version": "openai",
        "fallback_used": None,
    }


@app.function(image=image, secrets=secrets, cpu=2, timeout=120)
@modal.web_endpoint(method="POST")
def semantic_search(request: dict):
    """Search anime text embeddings with an SBERT query embedding."""
    from sentence_transformers import SentenceTransformer

    query = request.get("query")
    if not query:
        return {"results": [], "model_name": "all-MiniLM-L6-v2", "model_version": "baseline", "fallback_used": "missing_query"}

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embedding = model.encode(query, normalize_embeddings=True).tolist()

    try:
        results = _query_pgvector(embedding, "all-MiniLM-L6-v2", int(request.get("limit", 20)))
    except Exception as exc:
        return {
            "results": [],
            "model_name": "all-MiniLM-L6-v2",
            "model_version": "baseline",
            "fallback_used": "database_unavailable",
            "error": str(exc),
        }

    return {
        "results": results,
        "model_name": "all-MiniLM-L6-v2",
        "model_version": "baseline",
        "fallback_used": None,
    }


@app.function(image=image, secrets=secrets, gpu="T4", timeout=300)
@modal.web_endpoint(method="POST")
def gnn_recommendations(request: dict):
    """GNN recommendations are intentionally disabled until a trained model is promoted."""
    return {
        "recommendations": [],
        "model_name": "gnn",
        "model_version": "not_deployed",
        "fallback_used": "model_not_deployed",
    }


@app.function(image=image)
@modal.web_endpoint(method="GET")
def health():
    return {"status": "healthy", "service": "anivibe-ml"}


if __name__ == "__main__":
    with app.run():
        print(semantic_search.remote({"query": "action anime", "limit": 5}))
