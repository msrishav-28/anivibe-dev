'use client';

import { useEffect, useState } from 'react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { AnimeGrid } from '@/components/features/anime-grid';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Grid, List, Download } from 'lucide-react';
import { useWatchlistStore } from '@/store/watchlist-store';
import { useAuthStore } from '@/store/auth-store';
import { api } from '@/lib/api-client';
import type { Anime, WatchlistEntry } from '@/types';

export default function WatchlistPage() {
  const { user } = useAuthStore();
  const { entries, fetchWatchlist } = useWatchlistStore();
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
  const [sortBy, setSortBy] = useState('date_added');
  const [animeData, setAnimeData] = useState<Record<number, Anime>>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user) {
      loadWatchlist();
    }
  }, [user]);

  const loadWatchlist = async () => {
    setIsLoading(true);
    try {
      await fetchWatchlist();
      
      // Fetch anime details for all entries
      const animePromises = entries.map((entry) => 
        api.getAnime(entry.anime_id).catch(() => null)
      );
      const animeResults = await Promise.all(animePromises);
      
      const animeMap: Record<number, Anime> = {};
      animeResults.forEach((anime) => {
        if (anime) {
          animeMap[anime.anime_id] = anime;
        }
      });
      setAnimeData(animeMap);
    } catch (error) {
      console.error('Failed to load watchlist:', error);
    } finally {
      setIsLoading(false);
    }
  };

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
            
            <div className="flex items-center gap-1 rounded-lg border border-border p-1">
              <Button
                variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('grid')}
              >
                <Grid className="h-4 w-4" />
              </Button>
              <Button
                variant={viewMode === 'list' ? 'secondary' : 'ghost'}
                size="sm"
                onClick={() => setViewMode('list')}
              >
                <List className="h-4 w-4" />
              </Button>
            </div>
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
                variant={viewMode}
              />
            )}
          </TabsContent>

          <TabsContent value="watching" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(watchingEntries)}
              variant={viewMode}
            />
          </TabsContent>

          <TabsContent value="completed" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(completedEntries)}
              variant={viewMode}
            />
          </TabsContent>

          <TabsContent value="plan_to_watch" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(planToWatchEntries)}
              variant={viewMode}
            />
          </TabsContent>

          <TabsContent value="on_hold" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(onHoldEntries)}
              variant={viewMode}
            />
          </TabsContent>

          <TabsContent value="dropped" className="mt-6">
            <AnimeGrid
              anime={getAnimeForEntries(droppedEntries)}
              variant={viewMode}
            />
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
