'use client';

import { useEffect } from 'react';
import { useIntersectionObserver } from '@/hooks/use-intersection-observer';
import { AnimeCard } from './anime-card';
import { Skeleton } from '@/components/ui/skeleton';
import type { Anime } from '@/types';

interface AnimeGridProps {
  anime: Anime[];
  isLoading?: boolean;
  hasMore?: boolean;
  onLoadMore?: () => void;
  variant?: 'grid' | 'list';
  className?: string;
}

export function AnimeGrid({
  anime,
  isLoading = false,
  hasMore = false,
  onLoadMore,
  variant = 'grid',
  className = '',
}: AnimeGridProps) {
  const [ref, inView] = useIntersectionObserver({
    threshold: 0.5,
  });

  useEffect(() => {
    if (inView && hasMore && onLoadMore && !isLoading) {
      onLoadMore();
    }
  }, [inView, hasMore, onLoadMore, isLoading]);

  if (anime.length === 0 && !isLoading) {
    return (
      <div className="flex min-h-[400px] items-center justify-center">
        <div className="text-center">
          <p className="text-lg text-muted-foreground">No anime found</p>
          <p className="text-sm text-muted-foreground">Try adjusting your filters</p>
        </div>
      </div>
    );
  }

  return (
    <div className={className}>
      <div
        className={
          variant === 'grid'
            ? 'grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6'
            : 'flex flex-col gap-4'
        }
      >
        {anime.map((item) => (
          <AnimeCard key={item.anime_id} anime={item} variant={variant} />
        ))}
      </div>

      {/* Loading More Indicator */}
      {isLoading && (
        <div
          className={
            variant === 'grid'
              ? 'mt-8 grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6'
              : 'mt-4 flex flex-col gap-4'
          }
        >
          {Array.from({ length: variant === 'grid' ? 12 : 3 }).map((_, i) => (
            <Skeleton
              key={i}
              className={variant === 'grid' ? 'aspect-poster h-full' : 'h-32'}
            />
          ))}
        </div>
      )}

      {/* Infinite Scroll Trigger */}
      {hasMore && <div ref={ref} className="h-10" />}
    </div>
  );
}
