'use client';

import { useState, useEffect } from 'react';
import { MoodSelector } from '@/components/features/mood-selector';
import { AnimeGrid } from '@/components/features/anime-grid';
import { Card, CardContent } from '@/components/ui/card';
import { api } from '@/lib/api-client';
import type { Anime } from '@/types';

export default function MoodPage() {
  const [selectedMood, setSelectedMood] = useState<string>('');
  const [recommendations, setRecommendations] = useState<Anime[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleMoodChange = (mood: string) => {
    setSelectedMood(mood);
  };

  const loadRecommendations = async () => {
    if (!selectedMood) return;
    
    setIsLoading(true);
    try {
      const results = await api.getMoodBasedRecommendations(selectedMood);
      setRecommendations(results);
    } catch (error) {
      console.error('Failed to load mood recommendations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (selectedMood) {
      loadRecommendations();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedMood]);

  return (
    <div className="min-h-screen">
      <div className="container-custom py-8">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="mb-4 text-4xl font-bold">Find Anime by Mood</h1>
          <p className="text-lg text-muted-foreground">
            Select your current mood and discover anime that matches your vibe
          </p>
        </div>

        {/* Mood Selector */}
        <div className="mb-12">
          <MoodSelector
            selectedMood={selectedMood}
            onMoodChange={handleMoodChange}
          />
        </div>

        {/* Results */}
        {selectedMood && (
          <div>
            <h2 className="mb-6 text-2xl font-bold">
              Recommendations for {selectedMood} mood
            </h2>

            {isLoading ? (
              <div className="text-center py-12">
                <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent mx-auto" />
                <p className="mt-4 text-muted-foreground">Finding perfect matches...</p>
              </div>
            ) : recommendations.length > 0 ? (
              <AnimeGrid anime={recommendations} variant="grid" />
            ) : (
              <Card>
                <CardContent className="py-12 text-center">
                  <p className="text-muted-foreground">
                    No recommendations found for this mood. Try another one!
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        )}

        {!selectedMood && (
          <Card className="border-dashed">
            <CardContent className="py-12 text-center">
              <p className="text-lg text-muted-foreground">
                Select a mood above to get personalized recommendations
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
