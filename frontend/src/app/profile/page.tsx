'use client';

import { useEffect, useState } from 'react';
import { User, Calendar, TrendingUp, Heart, Clock } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Progress } from '@/components/ui/progress';
import { AnimeGrid } from '@/components/features/anime-grid';
import { useAuthStore } from '@/store/auth-store';
import { useWatchlistStore } from '@/store/watchlist-store';
import { api } from '@/lib/api-client';

export default function ProfilePage() {
  const { user } = useAuthStore();
  const { entries } = useWatchlistStore();
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    if (user) {
      loadUserStats();
    }
  }, [user]);

  const loadUserStats = async () => {
    try {
      const userStats = await api.getUserStats(user!.user_id);
      setStats(userStats);
    } catch (error) {
      console.error('Failed to load stats:', error);
    }
  };

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-muted-foreground">Please log in to view your profile</p>
      </div>
    );
  }

  const watchingCount = entries.filter((e) => e.status === 'watching').length;
  const completedCount = entries.filter((e) => e.status === 'completed').length;
  const planToWatchCount = entries.filter((e) => e.status === 'plan_to_watch').length;

  return (
    <div className="min-h-screen">
      <div className="container-custom py-8">
        {/* Profile Header */}
        <Card className="mb-8">
          <CardContent className="p-8">
            <div className="flex items-start gap-6">
              <Avatar className="h-24 w-24">
                <AvatarImage src={user.avatar_url} />
                <AvatarFallback className="text-2xl">
                  {user.username.slice(0, 2).toUpperCase()}
                </AvatarFallback>
              </Avatar>

              <div className="flex-1">
                <h1 className="mb-2 text-3xl font-bold">{user.username}</h1>
                <p className="mb-4 text-muted-foreground">{user.email}</p>

                <div className="flex gap-8">
                  <div>
                    <p className="text-2xl font-bold">{entries.length}</p>
                    <p className="text-sm text-muted-foreground">Total Anime</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{completedCount}</p>
                    <p className="text-sm text-muted-foreground">Completed</p>
                  </div>
                  <div>
                    <p className="text-2xl font-bold">{stats?.total_watch_time || 0}</p>
                    <p className="text-sm text-muted-foreground">Hours Watched</p>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats Grid */}
        <div className="mb-8 grid gap-6 md:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Watching</CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{watchingCount}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Completed</CardTitle>
              <TrendingUp className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{completedCount}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Plan to Watch</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{planToWatchCount}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Favorites</CardTitle>
              <Heart className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats?.favorites_count || 0}</div>
            </CardContent>
          </Card>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="overview">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="watchlist">Watchlist</TabsTrigger>
            <TabsTrigger value="analytics">Analytics</TabsTrigger>
            <TabsTrigger value="recommendations">Recommendations</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="mt-6">
            <div className="grid gap-6 md:grid-cols-2">
              <Card>
                <CardHeader>
                  <CardTitle>Genre Distribution</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {stats?.genre_distribution?.map((genre: any) => (
                    <div key={genre.name}>
                      <div className="mb-2 flex justify-between text-sm">
                        <span>{genre.name}</span>
                        <span className="text-muted-foreground">{genre.count}</span>
                      </div>
                      <Progress value={(genre.count / entries.length) * 100} />
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground">
                    Activity tracking coming soon...
                  </p>
                </CardContent>
              </Card>
            </div>
          </TabsContent>

          <TabsContent value="watchlist" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Your Anime List</CardTitle>
              </CardHeader>
              <CardContent>
                {entries.length > 0 ? (
                  <p className="text-muted-foreground">
                    {entries.length} anime in your list
                  </p>
                ) : (
                  <p className="text-muted-foreground">
                    Your watchlist is empty. Start adding anime!
                  </p>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="analytics" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Viewing Analytics</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  Detailed analytics coming soon...
                </p>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="recommendations" className="mt-6">
            <Card>
              <CardHeader>
                <CardTitle>Personalized Recommendations</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">
                  AI recommendations coming soon...
                </p>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}
