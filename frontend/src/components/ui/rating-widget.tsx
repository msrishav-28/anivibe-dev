'use client';

import { useState } from 'react';
import { Star } from 'lucide-react';
import { cn } from '@/lib/utils';

interface RatingWidgetProps {
  value?: number;
  onChange?: (value: number) => void;
  readonly?: boolean;
  size?: 'sm' | 'md' | 'lg';
  showValue?: boolean;
}

export function RatingWidget({
  value = 0,
  onChange,
  readonly = false,
  size = 'md',
  showValue = true,
}: RatingWidgetProps) {
  const [hover, setHover] = useState<number | null>(null);

  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
  };

  const handleClick = (rating: number) => {
    if (!readonly && onChange) {
      onChange(rating);
    }
  };

  return (
    <div className="flex items-center gap-2">
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((rating) => {
          const isFilled = (hover ?? value) >= rating;
          return (
            <button
              key={rating}
              type="button"
              disabled={readonly}
              onClick={() => handleClick(rating)}
              onMouseEnter={() => !readonly && setHover(rating)}
              onMouseLeave={() => !readonly && setHover(null)}
              className={cn(
                'transition-all',
                !readonly && 'hover:scale-110 cursor-pointer',
                readonly && 'cursor-default'
              )}
            >
              <Star
                className={cn(
                  sizeClasses[size],
                  'transition-colors',
                  isFilled ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'
                )}
              />
            </button>
          );
        })}
      </div>
      {showValue && (
        <span className="text-sm font-medium text-muted-foreground">
          {(hover ?? value).toFixed(1)}
        </span>
      )}
    </div>
  );
}
