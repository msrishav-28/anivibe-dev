'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import { Star, Play, Plus, Check, Share2, Heart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { AnimeCard } from '@/components/features/anime-card';
import { api } from '@/lib/api-client';
import { useWatchlistStore } from '@/store/watchlist-store';
import { genreColors } from '@/config/tokens';
import type { Anime } from '@/types';

interface AnimeDetailPageProps {
  params: { id: string };
}

export default function AnimeDetailPage({ params }: AnimeDetailPageProps) {
  const [anime, setAnime] = useState<Anime | null>(null);
  const [similarAnime, setSimilarAnime] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const { entries, addToWatchlist } = useWatchlistStore();

  const isInWatchlist = entries.some((entry) => entry.anime_id === parseInt(params.id));

  useEffect(() => {
    loadAnimeDetails();
  }, [params.id]);

  const loadAnimeDetails = async () => {
    setIsLoading(true);
    try {
      const [animeData, similar] = await Promise.all([
        api.getAnime(parseInt(params.id)),
        api.getSimilarAnime(parseInt(params.id), 12),
      ]);
      setAnime(animeData);
      setSimilarAnime(similar);
    } catch (error) {
      console.error('Failed to load anime:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddToWatchlist = () => {
    if (anime) {
      addToWatchlist(anime.anime_id, 'plan_to_watch');
    }
  };

  if (isLoading || !anime) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent" />
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-[500px] overflow-hidden">
        {/* Background Image */}
        <div className="absolute inset-0">
          <Image
            src={anime.image_url}
            alt={anime.title}
            fill
            className="object-cover blur-3xl scale-110 opacity-30"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-background via-background/80 to-background/20" />
        </div>

        {/* Content */}
        <div className="container-custom relative h-full flex items-end pb-8">
          <div className="flex gap-8">
            {/* Poster */}
            <div className="relative h-80 w-56 flex-shrink-0 overflow-hidden rounded-lg shadow-2xl">
              <Image
                src={anime.image_url}
                alt={anime.title}
                fill
                className="object-cover"
              />
            </div>

            {/* Info */}
            <div className="flex flex-col justify-end flex-1">
              <div className="mb-4 flex flex-wrap gap-2">
                {anime.genres.map((genre) => (
                  <Badge
                    key={genre}
                    style={{
                      backgroundColor: genreColors[genre] + '40',
                      color: genreColors[genre],
                    }}
                  >
                    {genre}
                  </Badge>
                ))}
              </div>

              <h1 className="mb-2 text-4xl font-bold">{anime.title}</h1>
              
              <div className="mb-4 flex items-center gap-4 text-sm text-muted-foreground">
                <span>{anime.type}</span>
                <span>•</span>
                <span>{anime.year}</span>
                {anime.episodes && (
                  <>
                    <span>•</span>
                    <span>{anime.episodes} Episodes</span>
                  </>
                )}
                <span>•</span>
                <span>{anime.status}</span>
              </div>

              <div className="mb-6 flex items-center gap-2">
                <Star className="h-6 w-6 fill-yellow-400 text-yellow-400" />
                <span className="text-2xl font-bold">{anime.score.toFixed(1)}</span>
                <span className="text-sm text-muted-foreground">
                  ({anime.scored_by?.toLocaleString()} users)
                </span>
              </div>

              <div className="flex gap-3">
                {anime.trailer_url && (
                  <Button size="lg" variant="primary">
                    <Play className="mr-2 h-5 w-5 fill-white" />
                    Watch Trailer
                  </Button>
                )}
                <Button
                  size="lg"
                  variant={isInWatchlist ? 'secondary' : 'outline'}
                  onClick={handleAddToWatchlist}
                >
                  {isInWatchlist ? (
                    <>
                      <Check className="mr-2 h-5 w-5" />
                      In My List
                    </>
                  ) : (
                    <>
                      <Plus className="mr-2 h-5 w-5" />
                      Add to List
                    </>
                  )}
                </Button>
                <Button size="lg" variant="ghost">
                  <Heart className="h-5 w-5" />
                </Button>
                <Button size="lg" variant="ghost">
                  <Share2 className="h-5 w-5" />
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Details Tabs */}
      <div className="container-custom py-8">
        <Tabs defaultValue="synopsis">
          <TabsList>
            <TabsTrigger value="synopsis">Synopsis</TabsTrigger>
            <TabsTrigger value="characters">Characters</TabsTrigger>
            <TabsTrigger value="reviews">Reviews</TabsTrigger>
            <TabsTrigger value="stats">Stats</TabsTrigger>
            <TabsTrigger value="similar">Similar</TabsTrigger>
          </TabsList>

          <TabsContent value="synopsis" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Synopsis</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground leading-relaxed">
                  {anime.synopsis || 'No synopsis available.'}
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="characters" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Characters & Voice Actors</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Character information coming soon...
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reviews" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>User Reviews</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Reviews coming soon...
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="stats" className="mt-6">
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Statistics</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Score</span>
                    <span className="font-semibold">{anime.score.toFixed(2)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Ranked</span>
                    <span className="font-semibold">#{anime.rank || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Popularity</span>
                    <span className="font-semibold">#{anime.popularity || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Members</span>
                    <span className="font-semibold">
                      {anime.members?.toLocaleString() || 'N/A'}
                    </span>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Type</span>
                    <span className="font-semibold">{anime.type}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Episodes</span>
                    <span className="font-semibold">{anime.episodes || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Status</span>
                    <span className="font-semibold">{anime.status}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Aired</span>
                    <span className="font-semibold">{anime.year}</span>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="similar" className="mt-6">
            <h3 className="mb-4 text-xl font-semibold">Similar Anime</h3>
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
              {similarAnime.map((item) => (
                <AnimeCard key={item.anime_id} anime={item} variant="grid" />
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
