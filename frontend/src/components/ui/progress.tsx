import * as React from 'react';
import { cn } from '@/lib/utils';

export interface ProgressProps extends React.HTMLAttributes<HTMLDivElement> {
  value?: number | null;
}

export const Progress = React.forwardRef<HTMLDivElement, ProgressProps>(
  ({ className, value = 0, ...props }, ref) => {
    const clamped = Math.max(0, Math.min(100, value ?? 0));
    return (
      <div
        ref={ref}
        className={cn('relative h-4 w-full overflow-hidden rounded-full border border-white/5 bg-white/10', className)}
        {...props}
      >
        <div
          className="h-full bg-primary-500 shadow-[0_0_10px_rgba(139,92,246,0.5)] transition-all"
          style={{ width: `${clamped}%` }}
        />
      </div>
    );
  }
);
Progress.displayName = 'Progress';
