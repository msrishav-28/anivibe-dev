// Progress removed
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

  // Gradient based on score - Cyberpunk palette
  const getGradient = () => {
    if (percentage >= 85) return 'bg-gradient-to-r from-green-400 to-emerald-600 shadow-[0_0_10px_rgba(34,197,94,0.5)]'; // High Match
    if (percentage >= 60) return 'bg-gradient-to-r from-primary-400 to-purple-600 shadow-[0_0_10px_rgba(139,92,246,0.5)]'; // Good Match
    if (percentage >= 40) return 'bg-gradient-to-r from-yellow-400 to-orange-500'; // Mid
    return 'bg-gradient-to-r from-red-500 to-red-700'; // Low
  };

  const getLabel = () => {
    if (percentage >= 85) return 'PERFECT SYNC';
    if (percentage >= 60) return 'HIGH SYNC';
    if (percentage >= 40) return 'PARTIAL SYNC';
    return 'LOW SYNC';
  };

  const heights = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4'
  };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="mb-1.5 flex justify-between text-xs uppercase tracking-wider font-bold">
          <span className={cn(
            percentage >= 85 ? "text-green-400" :
              percentage >= 60 ? "text-primary-400" :
                "text-muted-foreground"
          )}>
            {getLabel()}
          </span>
          <span className="text-white font-mono">{percentage}%</span>
        </div>
      )}

      <div className={cn("relative w-full overflow-hidden rounded-full bg-white/10 border border-white/5", heights[size])}>
        {/* Fill */}
        <div
          className={cn("h-full rounded-full transition-all duration-1000 ease-out", getGradient())}
          style={{ width: `${percentage}%` }}
        />

        {/* Scanline Effect */}
        <div className="absolute inset-0 bg-[linear-gradient(90deg,transparent,rgba(255,255,255,0.2),transparent)] w-1/2 h-full skew-x-12 animate-shimmer" />
      </div>
    </div>
  );
}
