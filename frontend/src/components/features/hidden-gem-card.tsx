import Link from 'next/link';
import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/badge';
import { RatingWidget } from '@/components/ui/rating-widget';
import { Gem, Users, TrendingUp } from 'lucide-react';
import type { Anime } from '@/types';
import Image from 'next/image';

interface HiddenGemCardProps {
  anime: Anime;
  reason?: string;
}

export function HiddenGemCard({ anime, reason }: HiddenGemCardProps) {
  const animeId = anime.anime_id ?? anime.id;
  const imageUrl = anime.image_url || '/placeholder-anime.svg';
  const score = anime.score ?? (typeof anime.rating === 'number' ? anime.rating : 0);

  return (
    <Link href={`/anime/${animeId}`}>
      <motion.div
        whileHover={{ y: -8, scale: 1.02 }}
        transition={{ duration: 0.3 }}
        className="group relative aspect-[2/3] overflow-hidden rounded-xl bg-card border border-primary-500/30 hover:shadow-neon-purple transition-colors"
      >
        <Image
          src={imageUrl}
          alt={anime.title}
          fill
          className="object-cover transition-transform duration-500 group-hover:scale-110"
          sizes="(max-width: 768px) 100vw, 33vw"
        />

        {/* Holographic Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black via-black/40 to-transparent opacity-90" />
        <div className="absolute inset-0 bg-[url('/noise.png')] opacity-10 mix-blend-overlay" />

        {/* Badge */}
        <div className="absolute top-3 right-3 z-10">
          <Badge className="bg-primary-500/80 backdrop-blur-md border border-primary-400 text-white gap-1.5 shadow-glow leading-none py-1.5">
            <Gem className="h-3.5 w-3.5 animate-pulse" />
            HIDDEN GEM
          </Badge>
        </div>

        {/* Content */}
        <div className="absolute bottom-0 left-0 right-0 p-5 z-20">
          <h3 className="mb-2 font-heading font-bold text-xl text-white leading-tight line-clamp-2 group-hover:text-primary-300 transition-colors">
            {anime.title}
          </h3>

          <div className="flex items-center justify-between mb-3 border-b border-white/10 pb-3">
            <div className="flex items-center gap-2">
              <RatingWidget value={score} readonly size="sm" showValue={false} />
              <span className="text-sm font-bold text-primary-300 shadow-glow">{score.toFixed(1)}</span>
            </div>
          </div>

          <div className="flex items-center gap-4 text-xs font-mono text-muted-foreground">
            <div className="flex items-center gap-1.5">
              <Users className="h-3.5 w-3.5" />
              <span>{anime.members?.toLocaleString() || 'N/A'}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <TrendingUp className="h-3.5 w-3.5" />
              <span>Rank #{anime.rank || 'N/A'}</span>
            </div>
          </div>

          {reason && (
            <div className="mt-4 p-3 rounded-lg bg-black/60 border-l-2 border-primary-500 backdrop-blur-sm">
              <p className="text-xs text-slate-300 italic line-clamp-3 leading-relaxed">
                "{reason}"
              </p>
            </div>
          )}
        </div>
      </motion.div>
    </Link>
  );
}
