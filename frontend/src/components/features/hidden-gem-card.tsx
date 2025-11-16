import Image from 'next/image';
import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { RatingWidget } from '@/components/ui/rating-widget';
import { Gem, Users, TrendingUp } from 'lucide-react';
import type { Anime } from '@/types';

interface HiddenGemCardProps {
  anime: Anime;
  reason?: string;
}

export function HiddenGemCard({ anime, reason }: HiddenGemCardProps) {
  return (
    <Link href={`/anime/${anime.anime_id}`}>
      <Card className="group overflow-hidden transition-all hover:scale-105 hover:shadow-xl border-2 border-primary-500/20">
        <div className="relative aspect-[2/3] overflow-hidden">
          <Image
            src={anime.image_url}
            alt={anime.title}
            fill
            className="object-cover transition-transform group-hover:scale-110"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />
          
          {/* Hidden Gem Badge */}
          <div className="absolute top-2 right-2">
            <Badge className="bg-primary-500 gap-1">
              <Gem className="h-3 w-3" />
              Hidden Gem
            </Badge>
          </div>

          {/* Content Overlay */}
          <div className="absolute bottom-0 left-0 right-0 p-4">
            <h3 className="mb-2 font-bold text-white line-clamp-2">{anime.title}</h3>
            
            <div className="flex items-center justify-between mb-2">
              <RatingWidget value={anime.score} readonly size="sm" showValue={false} />
              <span className="text-sm font-semibold text-white">{anime.score.toFixed(1)}</span>
            </div>

            <div className="flex items-center gap-3 text-xs text-white/80">
              <div className="flex items-center gap-1">
                <Users className="h-3 w-3" />
                <span>{anime.members?.toLocaleString() || 'N/A'}</span>
              </div>
              <div className="flex items-center gap-1">
                <TrendingUp className="h-3 w-3" />
                <span>#{anime.popularity || 'N/A'}</span>
              </div>
            </div>
          </div>
        </div>

        <CardContent className="p-4">
          <div className="flex flex-wrap gap-1 mb-2">
            {anime.genres.slice(0, 3).map((genre) => (
              <Badge key={genre} variant="secondary" className="text-xs">
                {genre}
              </Badge>
            ))}
          </div>
          
          {reason && (
            <p className="text-xs text-muted-foreground italic">
              💡 {reason}
            </p>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
