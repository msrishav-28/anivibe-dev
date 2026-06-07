"""
Run a local product smoke check against a running AniVibe API.

Expected setup:
  1. docker compose up -d postgres redis
  2. alembic upgrade head
  3. python scripts/fetch_mal_data.py --limit 250 --import-db
  4. python scripts/generate_embeddings.py --batch-size 16
  5. AUTH_REQUIRED=false uvicorn app.main:app --reload
"""
from __future__ import annotations

import argparse
import json
import sys

import httpx


def assert_status(response: httpx.Response, expected: set[int], label: str) -> None:
    if response.status_code not in expected:
        print(f"[FAIL] {label}: HTTP {response.status_code}", file=sys.stderr)
        print(response.text, file=sys.stderr)
        raise SystemExit(1)
    print(f"[OK] {label}: HTTP {response.status_code}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local AniVibe product smoke checks")
    parser.add_argument("--base-url", default="http://localhost:8000")
    parser.add_argument("--dev-user", default="local-user")
    parser.add_argument("--timeout", type=float, default=30.0)
    args = parser.parse_args()

    headers = {"X-AniVibe-Dev-User": args.dev_user}
    summary: dict[str, object] = {}

    with httpx.Client(base_url=args.base_url, headers=headers, timeout=args.timeout) as client:
        response = client.get("/health")
        assert_status(response, {200}, "health")

        response = client.get("/api/v1/anime/", params={"limit": 5})
        assert_status(response, {200}, "anime list")
        anime_items = response.json().get("items", [])
        if not anime_items:
            print("[FAIL] anime list returned no items; import the smoke dataset first", file=sys.stderr)
            raise SystemExit(1)
        anime_id = anime_items[0]["id"]
        summary["anime_id"] = anime_id

        response = client.get(f"/api/v1/anime/{anime_id}")
        assert_status(response, {200}, "anime detail")

        response = client.post(
            "/api/v1/search/semantic",
            json={"query": "melancholic sci-fi with strong atmosphere", "top_k": 5, "use_clip": False},
        )
        assert_status(response, {200}, "semantic search")
        summary["semantic_total"] = response.json().get("total")

        response = client.post("/api/v1/recommendations/similar", json={"anime_id": anime_id, "top_k": 5})
        assert_status(response, {200}, "similar recommendations")

        response = client.post("/api/v1/watchlist/", json={"anime_id": anime_id, "status": "plan_to_watch"})
        assert_status(response, {201, 400}, "watchlist add")

        response = client.get("/api/v1/watchlist/")
        assert_status(response, {200}, "watchlist list")
        summary["watchlist_count"] = len(response.json())

        response = client.post("/api/v1/ratings/", json={"anime_id": anime_id, "score": 8})
        assert_status(response, {201, 400}, "rating create")

        response = client.post("/api/v1/recommendations/personalized", json={"top_k": 5, "method": "content"})
        assert_status(response, {200}, "personalized recommendations")
        summary["personalized_total"] = response.json().get("total")

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
