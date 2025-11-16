'use client';

import { useState, useEffect } from 'react';
import { ReviewCard } from './review-card';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';

interface Review {
  rating_id: number;
  user: {
    user_id: number;
    username: string;
    avatar_url?: string;
  };
  score: number;
  review_text?: string;
  review_sentiment?: number;
  created_at: string;
}

interface ReviewsListProps {
  animeId: number;
  reviews: Review[];
  isLoading?: boolean;
  onLoadMore?: () => void;
  hasMore?: boolean;
}

export function ReviewsList({ 
  animeId, 
  reviews, 
  isLoading = false, 
  onLoadMore,
  hasMore = false 
}: ReviewsListProps) {
  if (isLoading && reviews.length === 0) {
    return (
      <div className="space-y-4">
        {[1, 2, 3].map((i) => (
          <Skeleton key={i} className="h-32 w-full" />
        ))}
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No reviews yet. Be the first to review!</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {reviews.map((review) => (
        <ReviewCard key={review.rating_id} review={review} />
      ))}

      {hasMore && (
        <div className="text-center pt-4">
          <Button 
            variant="outline" 
            onClick={onLoadMore}
            loading={isLoading}
          >
            Load More Reviews
          </Button>
        </div>
      )}
    </div>
  );
}
