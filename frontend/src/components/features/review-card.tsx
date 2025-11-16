import { Card, CardContent } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { RatingWidget } from '@/components/ui/rating-widget';
import { SentimentBadge } from './sentiment-badge';
import { formatDate } from '@/lib/utils';

interface ReviewCardProps {
  review: {
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
  };
}

export function ReviewCard({ review }: ReviewCardProps) {
  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex items-start gap-4">
          {/* Avatar */}
          <Avatar className="h-10 w-10">
            <AvatarImage src={review.user.avatar_url} />
            <AvatarFallback>
              {review.user.username.slice(0, 2).toUpperCase()}
            </AvatarFallback>
          </Avatar>

          {/* Content */}
          <div className="flex-1">
            <div className="mb-2 flex items-center justify-between">
              <div>
                <p className="font-semibold">{review.user.username}</p>
                <p className="text-sm text-muted-foreground">
                  {formatDate(review.created_at)}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <RatingWidget value={review.score} readonly size="sm" showValue={false} />
                <span className="font-bold text-lg">{review.score.toFixed(1)}</span>
              </div>
            </div>

            {review.review_text && (
              <p className="text-sm text-muted-foreground leading-relaxed mb-3">
                {review.review_text}
              </p>
            )}

            {review.review_sentiment !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-xs text-muted-foreground">Sentiment:</span>
                <SentimentBadge score={review.review_sentiment} />
              </div>
            )}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
