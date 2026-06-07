"""
Deprecated.

AniVibe now uses Postgres/pgvector as the canonical vector index. Generate
embeddings with `scripts/generate_embeddings.py`; vector search queries the
`anime_embeddings` table directly.
"""


def main() -> None:
    print(
        "FAISS indexes are deprecated for production. "
        "Use scripts/generate_embeddings.py and Postgres/pgvector instead."
    )


if __name__ == "__main__":
    main()
