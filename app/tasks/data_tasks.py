"""
Data synchronization job entrypoints.
"""
import asyncio

from scripts.fetch_mal_data import MALDataFetcher, import_to_database


def sync_mal_data_job(limit: int | None = None) -> int:
    async def _sync() -> int:
        async with MALDataFetcher(limit=limit) as fetcher:
            await fetcher.fetch_genres()
            await fetcher.fetch_all_anime()
            fetcher.save_final_data()
            await import_to_database(fetcher.anime_data)
            return len(fetcher.anime_data)

    return asyncio.run(_sync())
