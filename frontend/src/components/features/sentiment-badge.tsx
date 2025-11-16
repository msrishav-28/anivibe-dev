import { Badge } from '@/components/ui/badge';
import { Smile, Meh, Frown } from 'lucide-react';

interface SentimentBadgeProps {
  score: number; // -1 to 1
  showLabel?: boolean;
}

export function SentimentBadge({ score, showLabel = true }: SentimentBadgeProps) {
  const getSentiment = () => {
    if (score > 0.3) {
      return {
        label: 'Positive',
        color: 'bg-green-500/10 text-green-500 border-green-500/20',
        icon: Smile,
      };
    } else if (score < -0.3) {
      return {
        label: 'Negative',
        color: 'bg-red-500/10 text-red-500 border-red-500/20',
        icon: Frown,
      };
    } else {
      return {
        label: 'Neutral',
        color: 'bg-gray-500/10 text-gray-500 border-gray-500/20',
        icon: Meh,
      };
    }
  };

  const sentiment = getSentiment();
  const Icon = sentiment.icon;

  return (
    <Badge className={sentiment.color}>
      <Icon className="mr-1 h-3 w-3" />
      {showLabel && sentiment.label}
    </Badge>
  );
}
