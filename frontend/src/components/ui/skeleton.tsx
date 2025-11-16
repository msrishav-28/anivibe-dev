import { cn } from '@/lib/utils';

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('shimmer rounded-md bg-muted animate-pulse', className)}
      {...props}
    />
  );
}

export { Skeleton };
