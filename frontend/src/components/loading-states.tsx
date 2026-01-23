'use client';

import { Skeleton } from '@/components/ui/skeleton';
import { Card, CardContent, CardHeader } from '@/components/ui/card';

// Anime Card Loading
export function AnimeCardSkeleton() {
  return (
    <Card variant="holo" className="overflow-hidden border-white/5">
      <Skeleton className="aspect-[2/3] w-full rounded-none" />
      <CardContent className="p-4 space-y-3">
        <Skeleton className="h-5 w-3/4 bg-white/10" />
        <Skeleton className="h-3 w-1/2 bg-white/5" />
      </CardContent>
    </Card>
  );
}

// Anime Grid Loading
export function AnimeGridSkeleton({ count = 12 }: { count?: number }) {
  return (
    <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6">
      {Array.from({ length: count }).map((_, i) => (
        <AnimeCardSkeleton key={i} />
      ))}
    </div>
  );
}

// Anime Detail Loading
export function AnimeDetailSkeleton() {
  return (
    <div className="space-y-8 animate-pulse-slow">
      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <Skeleton className="aspect-[2/3] w-full rounded-xl border border-white/10 bg-white/5" />
        </div>
        <div className="lg:col-span-2 space-y-6">
          <Skeleton className="h-12 w-3/4 bg-white/10 rounded-lg" />
          <Skeleton className="h-6 w-1/2 bg-white/5" />
          <Skeleton className="h-32 w-full bg-white/5 border border-white/10 rounded-xl" />
          <div className="grid grid-cols-2 gap-4">
            <Skeleton className="h-24 bg-primary-500/5 border border-primary-500/20 rounded-xl" />
            <Skeleton className="h-24 bg-primary-500/5 border border-primary-500/20 rounded-xl" />
          </div>
        </div>
      </div>
    </div>
  );
}

// Review Card Loading
export function ReviewCardSkeleton() {
  return (
    <Card variant="holo" className="border-white/5">
      <CardHeader className="flex-row items-center gap-4 pb-2">
        <Skeleton className="h-10 w-10 rounded-full border border-white/10" />
        <div className="flex-1 space-y-2">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-3 w-24 bg-white/5" />
        </div>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-20 w-full" />
      </CardContent>
    </Card>
  );
}

// Profile Stats Loading
export function ProfileStatsSkeleton() {
  return (
    <div className="grid gap-4 md:grid-cols-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <Card key={i}>
          <CardContent className="p-6">
            <Skeleton className="h-4 w-20 mb-2" />
            <Skeleton className="h-8 w-16" />
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

// Full Page Loading
export function PageSkeleton() {
  return (
    <div className="container-custom py-8 space-y-8">
      <div>
        <Skeleton className="h-10 w-64 mb-2" />
        <Skeleton className="h-6 w-96" />
      </div>
      <AnimeGridSkeleton count={8} />
    </div>
  );
}
