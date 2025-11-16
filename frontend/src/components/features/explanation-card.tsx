import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Lightbulb, TrendingUp } from 'lucide-react';

interface ExplanationFactor {
  name: string;
  value: string | number;
  importance?: number;
}

interface ExplanationCardProps {
  explanation: {
    anime_id: number;
    method: string;
    natural_language: string;
    factors: ExplanationFactor[];
    confidence?: number;
  };
}

export function ExplanationCard({ explanation }: ExplanationCardProps) {
  return (
    <Card className="border-primary-500/20 bg-primary-500/5">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-primary-500" />
            Why Recommended
          </CardTitle>
          {explanation.confidence && (
            <Badge className="bg-primary-500/10 text-primary-500">
              {(explanation.confidence * 100).toFixed(0)}% Match
            </Badge>
          )}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm leading-relaxed text-muted-foreground">
          {explanation.natural_language}
        </p>

        {explanation.factors && explanation.factors.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium">Key Factors:</h4>
            <div className="grid gap-2">
              {explanation.factors.map((factor, idx) => (
                <div
                  key={idx}
                  className="flex items-center justify-between rounded-md bg-background/50 p-2 text-sm"
                >
                  <span className="font-medium">{factor.name}</span>
                  <span className="text-muted-foreground">{factor.value}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <TrendingUp className="h-3 w-3" />
          <span>Based on {explanation.method} analysis</span>
        </div>
      </CardContent>
    </Card>
  );
}
