'use client';

import { useEffect, useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { AnimeGrid } from '@/components/features/anime-grid';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Download } from 'lucide-react';
import { useWatchlistStore } from '@/store/watchlist-store';
import { useAuthStore } from '@/store/auth-store';
import { api } from '@/lib/api-client';
import type { Anime, WatchlistEntry } from '@/types';

export default function WatchlistPage() {
  const { user } = useAuthStore();
  const { entries, fetchWatchlist } = useWatchlistStore();
  const [sortBy, setSortBy] = useState('date_added');
  const [animeData, setAnimeData] = useState<Record<number, Anime>>({});
  const [isLoading, setIsLoading] = useState(true);

  // Effect 1: Fetch watchlist when user is available
  useEffect(() => {
    if (user) {
      fetchWatchlist();
    }
  }, [user, fetchWatchlist]);

  // Effect 2: Load anime details when entries change
  useEffect(() => {
    const loadAnimeDetails = async () => {
      if (entries.length === 0) {
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      try {
        // Optimization: Fetch in batches of 5 to avoid rate limiting/flooding
        const BATCH_SIZE = 5;
        const tempMap: Record<number, Anime> = { ...animeData };

        // Identify missing anime
        const missingIds = entries
          .map(e => e.anime_id)
          .filter(id => !tempMap[id]);

        if (missingIds.length === 0) {
          setIsLoading(false);
          return;
        }

        // Process batches
        for (let i = 0; i < missingIds.length; i += BATCH_SIZE) {
          const batch = missingIds.slice(i, i + BATCH_SIZE);
          const promises = batch.map(id => api.getAnime(id).catch(() => null));
          const results = await Promise.all(promises);

          results.forEach(anime => {
            if (anime) {
              tempMap[anime.anime_id] = anime;
            }
          });

          // Update state progressively
          setAnimeData({ ...tempMap });
          // Small delay to be nice to API
          await new Promise(resolve => setTimeout(resolve, 100));
        }

      } catch (error) {
        console.error('Failed to load anime details:', error);
      } finally {
        setIsLoading(false);
      }
    };

    loadAnimeDetails();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [entries]);

  const getEntriesByStatus = (status: string) => {
    return entries.filter((entry) => entry.status === status);
  };

  const getAnimeForEntries = (entries: WatchlistEntry[]) => {
    return entries
      .map((entry) => animeData[entry.anime_id])
      .filter((anime): anime is Anime => anime !== undefined);
  };

  const watchingEntries = getEntriesByStatus('watching');
  const completedEntries = getEntriesByStatus('completed');
  const planToWatchEntries = getEntriesByStatus('plan_to_watch');
  const onHoldEntries = getEntriesByStatus('on_hold');
  const droppedEntries = getEntriesByStatus('dropped');

  const totalEpisodes = completedEntries.reduce((sum, entry) => {
    const anime = animeData[entry.anime_id];
    return sum + (anime?.episodes || 0);
  }, 0);

  const averageScore = completedEntries.reduce((sum, entry) => {
    return sum + (entry.score || 0);
  }, 0) / (completedEntries.length || 1);

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card>
          <CardContent className="p-8 text-center">
            <p className="text-lg text-muted-foreground">
              Please log in to view your watchlist
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <div className="container-custom py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="mb-4 text-4xl font-bold">My Watchlist</h1>

          {/* Stats Cards */}
          <div className="grid gap-4 md:grid-cols-4">
            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Total Anime
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{entries.length}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Completed
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{completedEntries.length}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Episodes Watched
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{totalEpisodes}</div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Average Score
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{averageScore.toFixed(1)}</div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Controls */}
        <div className="mb-6 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="date_added">Date Added</SelectItem>
                <SelectItem value="title">Title</SelectItem>
                <SelectItem value="score">My Score</SelectItem>
                <SelectItem value="progress">Progress</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Download className="mr-2 h-4 w-4" />
              Export
            </Button>


          </div>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="all">
          <TabsList>
            <TabsTrigger value="all">
              All ({entries.length})
            </TabsTrigger>
            <TabsTrigger value="watching">
              Watching ({watchingEntries.length})
            </TabsTrigger>
            <TabsTrigger value="completed">
              Completed ({completedEntries.length})
            </TabsTrigger>
            <TabsTrigger value="plan_to_watch">
              Plan to Watch ({planToWatchEntries.length})
            </TabsTrigger>
            <TabsTrigger value="on_hold">
              On Hold ({onHoldEntries.length})
            </TabsTrigger>
            <TabsTrigger value="dropped">
              Dropped ({droppedEntries.length})
            </TabsTrigger>
          </TabsList>

          <TabsContent value="all" className="mt-6">
            {isLoading ? (
              <div className="text-center py-12">Loading...</div>
            ) : (
              <AnimeGrid
                anime={getAnimeForEntries(entries)}
              />
            )}
          </TabsContent>

          <TabsContent value="watching" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(watchingEntries)}
            />
          </TabsContent>

          <TabsContent value="completed" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(completedEntries)}
            />
          </TabsContent>

          <TabsContent value="plan_to_watch" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(planToWatchEntries)}
            />
          </TabsContent>

          <TabsContent value="on_hold" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(onHoldEntries)}
            />
          </TabsContent>

          <TabsContent value="dropped" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(droppedEntries)}
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
