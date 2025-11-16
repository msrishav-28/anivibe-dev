import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { TrendingUp, Award, Heart } from 'lucide-react';

interface TasteProfileProps {
  profile: {
    favorite_genres: Array<{ name: string; count: number; percentage: number }>;
    preferred_types: Array<{ name: string; count: number }>;
    average_rating: number;
    total_ratings: number;
    viewing_patterns: {
      most_active_time: string;
      binge_watcher: boolean;
    };
    personality_insights: string[];
  };
}

export function TasteProfile({ profile }: TasteProfileProps) {
  return (
    <div className="grid gap-6 md:grid-cols-2">
      {/* Favorite Genres */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Heart className="h-5 w-5 text-primary-500" />
            Favorite Genres
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {profile.favorite_genres.slice(0, 5).map((genre) => (
            <div key={genre.name}>
              <div className="mb-2 flex justify-between text-sm">
                <span className="font-medium">{genre.name}</span>
                <span className="text-muted-foreground">
                  {genre.count} anime ({genre.percentage.toFixed(0)}%)
                </span>
              </div>
              <Progress value={genre.percentage} />
            </div>
          ))}
        </CardContent>
      </Card>

      {/* Viewing Stats */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-primary-500" />
            Viewing Stats
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Average Rating</span>
            <Badge className="bg-primary-500/10 text-primary-500 text-lg font-bold">
              {profile.average_rating.toFixed(1)} / 10
            </Badge>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Total Ratings</span>
            <span className="font-semibold">{profile.total_ratings}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Most Active</span>
            <span className="font-semibold">{profile.viewing_patterns.most_active_time}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-sm text-muted-foreground">Viewing Style</span>
            <Badge>
              {profile.viewing_patterns.binge_watcher ? 'Binge Watcher' : 'Casual Viewer'}
            </Badge>
          </div>
        </CardContent>
      </Card>

      {/* Personality Insights */}
      <Card className="md:col-span-2">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Award className="h-5 w-5 text-primary-500" />
            Your Anime Personality
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {profile.personality_insights.map((insight, idx) => (
              <Badge key={idx} variant="secondary" className="text-sm">
                {insight}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
