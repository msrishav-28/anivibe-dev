'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { RatingWidget } from '@/components/ui/rating-widget';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { api } from '@/lib/api-client';
import { useAuthStore } from '@/store/auth-store';

interface ReviewFormProps {
  animeId: number;
  onSuccess?: () => void;
  existingReview?: {
    rating_id: number;
    score: number;
    review_text?: string;
  };
}

export function ReviewForm({ animeId, onSuccess, existingReview }: ReviewFormProps) {
  const { user } = useAuthStore();
  const [score, setScore] = useState(existingReview?.score || 0);
  const [reviewText, setReviewText] = useState(existingReview?.review_text || '');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!user) {
      setError('Please log in to submit a review');
      return;
    }

    if (score === 0) {
      setError('Please select a rating');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      if (existingReview) {
        await api.updateRating(existingReview.rating_id, {
          score,
          review_text: reviewText || undefined,
        });
      } else {
        await api.createRating({
          anime_id: animeId,
          score,
          review_text: reviewText || undefined,
        });
      }
      
      onSuccess?.();
    } catch (err: any) {
      setError(err.message || 'Failed to submit review');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{existingReview ? 'Edit Your Review' : 'Write a Review'}</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="mb-2 block text-sm font-medium">Your Rating</label>
            <RatingWidget value={score} onChange={setScore} size="lg" />
          </div>

          <div>
            <label htmlFor="review" className="mb-2 block text-sm font-medium">
              Review (Optional)
            </label>
            <textarea
              id="review"
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              className="w-full rounded-md border border-input bg-background px-3 py-2 text-sm min-h-[120px]"
              placeholder="Share your thoughts about this anime..."
            />
          </div>

          {error && (
            <div className="rounded-md bg-red-500/10 border border-red-500/20 p-3 text-sm text-red-500">
              {error}
            </div>
          )}

          <Button type="submit" loading={isSubmitting} className="w-full">
            {existingReview ? 'Update Review' : 'Submit Review'}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
