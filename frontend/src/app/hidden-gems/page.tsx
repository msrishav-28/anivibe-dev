'use client';

import { useState, useEffect } from 'react';
import { HiddenGemCard } from '@/components/features/hidden-gem-card';
import { Card, CardContent } from '@/components/ui/card';
import { Slider } from '@/components/ui/slider';
import { Button } from '@/components/ui/button';
import { Gem, Sparkles } from 'lucide-react';
import { api } from '@/lib/api-client';
import type { Anime } from '@/types';

export default function HiddenGemsPage() {
  const [gems, setGems] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [minScore, setMinScore] = useState([7.5]);
  const [maxPopularity, setMaxPopularity] = useState([10000]);

  useEffect(() => {
    loadHiddenGems();
  }, []);

  const loadHiddenGems = async () => {
    setIsLoading(true);
    try {
      const results = await api.getHiddenGems({
        min_score: minScore[0],
        max_popularity: maxPopularity[0],
        top_k: 24,
      });
      setGems(results);
    } catch (error) {
      console.error('Failed to load hidden gems:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFiltersApply = () => {
    loadHiddenGems();
  };

  return (
    <div className="min-h-screen">
      <div className="container-custom py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <div className="mb-4 flex items-center justify-center gap-3">
            <Gem className="h-10 w-10 text-primary-500" />
            <h1 className="text-4xl font-bold">Hidden Gems</h1>
            <Sparkles className="h-10 w-10 text-accent-pink" />
          </div>
          <p className="text-lg text-muted-foreground">
            Discover high-quality anime that flew under the radar
          </p>
        </div>

        {/* Filters */}
        <Card className="mb-8">
          <CardContent className="p-6">
            <div className="grid gap-6 md:grid-cols-2">
              <div>
                <label className="mb-4 block text-sm font-medium">
                  Minimum Score: {minScore[0].toFixed(1)}
                </label>
                <Slider
                  value={minScore}
                  onValueChange={setMinScore}
                  min={6}
                  max={9}
                  step={0.1}
                />
              </div>

              <div>
                <label className="mb-4 block text-sm font-medium">
                  Max Popularity Rank: {maxPopularity[0].toLocaleString()}
                </label>
                <Slider
                  value={maxPopularity}
                  onValueChange={setMaxPopularity}
                  min={1000}
                  max={20000}
                  step={1000}
                />
              </div>
            </div>

            <div className="mt-6 text-center">
              <Button onClick={handleFiltersApply}>
                Apply Filters
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Results */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent mx-auto" />
            <p className="mt-4 text-muted-foreground">Discovering hidden gems...</p>
          </div>
        ) : gems.length > 0 ? (
          <>
            <div className="mb-6">
              <h2 className="text-2xl font-bold">
                {gems.length} Hidden Gems Found
              </h2>
              <p className="text-muted-foreground">
                High-quality anime with less than {maxPopularity[0].toLocaleString()} members
              </p>
            </div>

            <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {gems.map((anime) => (
                <HiddenGemCard
                  key={anime.anime_id}
                  anime={anime}
                  reason="Underrated masterpiece with excellent storytelling"
                />
              ))}
            </div>
          </>
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-lg text-muted-foreground">
                No hidden gems found with these criteria. Try adjusting the filters!
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
