import { Progress } from '@/components/ui/progress';
import { cn } from '@/lib/utils';

interface ConfidenceBarProps {
  confidence: number; // 0 to 1
  showLabel?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export function ConfidenceBar({ 
  confidence, 
  showLabel = true, 
  size = 'md' 
}: ConfidenceBarProps) {
  const percentage = Math.round(confidence * 100);
  
  const getColor = () => {
    if (percentage >= 80) return 'bg-green-500';
    if (percentage >= 60) return 'bg-blue-500';
    if (percentage >= 40) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  const getLabel = () => {
    if (percentage >= 80) return 'Excellent Match';
    if (percentage >= 60) return 'Good Match';
    if (percentage >= 40) return 'Fair Match';
    return 'Low Match';
  };

  const heightClasses = {
    sm: 'h-1',
    md: 'h-2',
    lg: 'h-3',
  };

  return (
    <div className="space-y-2">
      {showLabel && (
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium">{getLabel()}</span>
          <span className="text-muted-foreground">{percentage}%</span>
        </div>
      )}
      <div className={cn('relative w-full overflow-hidden rounded-full bg-muted', heightClasses[size])}>
        <div
          className={cn('h-full transition-all duration-500', getColor())}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
