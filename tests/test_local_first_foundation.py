import pytest

from app.core.rate_limit import _memory_counters, classify_rate_limit
from app.core.security import is_dev_auth_bypass_enabled
from config import settings
from scripts.fetch_mal_data import validate_raw_anime_data


def test_dev_auth_bypass_is_development_only(monkeypatch):
    monkeypatch.setattr(settings, "environment", "development")
    monkeypatch.setattr(settings, "auth_required", False)
    assert is_dev_auth_bypass_enabled() is True

    monkeypatch.setattr(settings, "environment", "production")
    with pytest.raises(RuntimeError):
        is_dev_auth_bypass_enabled()


def test_route_rate_limit_classification():
    assert classify_rate_limit("/health", "GET") is None
    assert classify_rate_limit("/api/v1/search/visual", "POST").requests == 5
    assert classify_rate_limit("/api/v1/search/semantic", "POST").requests == 30
    assert classify_rate_limit("/api/v1/recommendations/personalized", "POST").requests == 30
    assert classify_rate_limit("/api/v1/watchlist", "POST").requests == 60
    assert classify_rate_limit("/api/v1/anime", "GET").requests == 120


def test_raw_anime_import_validation_reports_missing_and_duplicate_ids():
    validation = validate_raw_anime_data(
        [
            {
                "mal_id": 1,
                "title": "Cowboy Bebop",
                "synopsis": "Bounty hunters in space.",
                "score": 8.7,
                "members": 1000000,
                "images": {"jpg": {"large_image_url": "https://example.com/cowboy.jpg"}},
            },
            {
                "mal_id": 1,
                "title": "",
                "images": {"jpg": {}},
            },
        ]
    )

    assert validation["record_count"] == 2
    assert validation["unique_mal_ids"] == 1
    assert validation["failures"]["duplicate_mal_ids"] == [1]
    assert validation["failures"]["missing_required"]["title"] == 1
    assert validation["failures"]["missing_required"]["image_url"] == 1


@pytest.mark.asyncio
async def test_default_route_rate_limit_returns_429(client, monkeypatch):
    _memory_counters.clear()
    monkeypatch.setattr(settings, "rate_limit_enabled", True)
    monkeypatch.setattr(settings, "rate_limit_per_minute", 1)

    first = await client.get("/api/v1/unknown-local-rate-limit-test")
    second = await client.get("/api/v1/unknown-local-rate-limit-test")

    assert first.status_code == 404
    assert second.status_code == 429
    assert second.json()["error"]["code"] == "rate_limit_exceeded"
    _memory_counters.clear()
