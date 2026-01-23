import { cn } from '@/lib/utils';

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn('shimmer rounded-md bg-white/5 animate-pulse', className)}
      {...props}
    />
  );
}

export { Skeleton };
