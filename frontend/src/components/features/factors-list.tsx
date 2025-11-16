import { Badge } from '@/components/ui/badge';
import { CheckCircle2 } from 'lucide-react';

interface Factor {
  name: string;
  value: string | number;
  importance?: number;
}

interface FactorsListProps {
  factors: Factor[];
  title?: string;
}

export function FactorsList({ factors, title = 'Matching Factors' }: FactorsListProps) {
  return (
    <div className="space-y-3">
      {title && <h4 className="text-sm font-medium">{title}</h4>}
      
      <div className="space-y-2">
        {factors.map((factor, idx) => (
          <div
            key={idx}
            className="flex items-center justify-between rounded-lg border border-border bg-card p-3 transition-colors hover:bg-accent"
          >
            <div className="flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-primary-500" />
              <span className="text-sm font-medium">{factor.name}</span>
            </div>
            
            <div className="flex items-center gap-2">
              <Badge variant="secondary">{factor.value}</Badge>
              {factor.importance !== undefined && (
                <div className="flex gap-0.5">
                  {[...Array(5)].map((_, i) => (
                    <div
                      key={i}
                      className={`h-1 w-1 rounded-full ${
                        i < Math.round(factor.importance! * 5)
                          ? 'bg-primary-500'
                          : 'bg-muted'
                      }`}
                    />
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
