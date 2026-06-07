import * as React from 'react';
import { cn } from '@/lib/utils';

export interface AlertProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'destructive';
}

export function Alert({ className, variant = 'default', ...props }: AlertProps) {
  return (
    <div
      role="alert"
      className={cn(
        'rounded-md border border-white/10 bg-black/40 p-4 text-sm',
        variant === 'destructive' && 'border-red-500/40 bg-red-500/10 text-red-100',
        className
      )}
      {...props}
    />
  );
}

export function AlertTitle({ className, ...props }: React.HTMLAttributes<HTMLHeadingElement>) {
  return <h5 className={cn('mb-1 font-medium leading-none', className)} {...props} />;
}

export function AlertDescription({ className, ...props }: React.HTMLAttributes<HTMLParagraphElement>) {
  return <div className={cn('text-muted-foreground', className)} {...props} />;
}
