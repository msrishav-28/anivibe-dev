'use client';

import { useState, useEffect } from 'react';
import { AnimeGrid } from '@/components/features/anime-grid';
import { api } from '@/lib/api-client';
import type { Anime } from '@/types';

export default function ExplorePage() {
  const [anime, setAnime] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  // Filters will be moved to a modal or Vibe Tuner later, keeping state but removing Sidebar UI
  const [filters] = useState<any>({});

  const loadAnime = async (pageNum: number, newFilters?: any) => {
    setIsLoading(true);
    try {
      const params = {
        page: pageNum,
        limit: 24,
        ...newFilters,
      };
      const results = await api.getAnimeList(params);

      if (pageNum === 1) {
        setAnime(results.items);
      } else {
        setAnime((prev) => [...prev, ...results.items]);
      }

      setHasMore(results.items.length === 24);
    } catch (error) {
      console.error('Failed to load anime:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnime(1, filters);
  }, [filters]);

  const handleLoadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    loadAnime(nextPage, filters);
  };

  return (
    <div className="flex min-h-screen">
      {/* Main Content */}
      <main className="flex-1">
        <div className="container-custom py-8">
          {/* Header */}
          <div className="mb-6 flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">Explore Anime</h1>
              <p className="text-muted-foreground">
                Discover from 26,000+ anime titles
              </p>
            </div>
          </div>

          {/* Results */}
          <AnimeGrid
            anime={anime}
            isLoading={isLoading}
            hasMore={hasMore}
            onLoadMore={handleLoadMore}
          />
        </div>
      </main>
    </div>
  );
}
