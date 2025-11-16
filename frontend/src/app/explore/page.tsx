'use client';

import { useState, useEffect } from 'react';
import { FilterSidebar } from '@/components/features/filter-sidebar';
import { AnimeGrid } from '@/components/features/anime-grid';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Grid, List, SlidersHorizontal } from 'lucide-react';
import { api } from '@/lib/api-client';
import type { Anime } from '@/types';

export default function ExplorePage() {
  const [anime, setAnime] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [showFilters, setShowFilters] = useState(true);
  const [filters, setFilters] = useState<any>({});

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
        setAnime(results);
      } else {
        setAnime((prev) => [...prev, ...results]);
      }
      
      setHasMore(results.length === 24);
    } catch (error) {
      console.error('Failed to load anime:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadAnime(1, filters);
  }, [filters]);

  const handleFiltersChange = (newFilters: any) => {
    setFilters(newFilters);
    setPage(1);
  };

  const handleLoadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    loadAnime(nextPage, filters);
  };

  return (
    <div className="flex min-h-screen">
      {/* Filters Sidebar */}
      {showFilters && (
        <aside className="sticky top-16 hidden h-[calc(100vh-4rem)] w-80 flex-shrink-0 border-r border-border lg:block">
          <FilterSidebar
            onFiltersChange={handleFiltersChange}
            initialFilters={filters}
          />
        </aside>
      )}

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

            <div className="flex items-center gap-2">
              {/* View Toggle */}
              <div className="flex items-center gap-1 rounded-lg border border-border p-1">
                <Button
                  variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('grid')}
                >
                  <Grid className="h-4 w-4" />
                </Button>
                <Button
                  variant={viewMode === 'list' ? 'secondary' : 'ghost'}
                  size="sm"
                  onClick={() => setViewMode('list')}
                >
                  <List className="h-4 w-4" />
                </Button>
              </div>

              {/* Filter Toggle (Mobile) */}
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilters(!showFilters)}
                className="lg:hidden"
              >
                <SlidersHorizontal className="h-4 w-4" />
              </Button>
            </div>
          </div>

          {/* Results */}
          <AnimeGrid
            anime={anime}
            isLoading={isLoading}
            hasMore={hasMore}
            onLoadMore={handleLoadMore}
            variant={viewMode}
          />
        </div>
      </main>
    </div>
  );
}
