'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Progress } from '@/components/ui/progress';
import { ChevronRight, ChevronLeft } from 'lucide-react';

const GENRES = [
  'Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror',
  'Mystery', 'Psychological', 'Romance', 'Sci-Fi', 'Slice of Life',
  'Sports', 'Supernatural', 'Thriller', 'Mecha', 'Music'
];

interface OnboardingFlowProps {
  onComplete: (preferences: any) => void;
}

export function OnboardingFlow({ onComplete }: OnboardingFlowProps) {
  const [step, setStep] = useState(1);
  const [selectedGenres, setSelectedGenres] = useState<string[]>([]);
  const [experienceLevel, setExperienceLevel] = useState<string>('');

  const totalSteps = 3;
  const progress = (step / totalSteps) * 100;

  const handleGenreToggle = (genre: string) => {
    setSelectedGenres((prev) =>
      prev.includes(genre)
        ? prev.filter((g) => g !== genre)
        : [...prev, genre]
    );
  };

  const handleNext = () => {
    if (step < totalSteps) {
      setStep(step + 1);
    } else {
      onComplete({
        genres: selectedGenres,
        experience: experienceLevel,
      });
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const canProceed = () => {
    if (step === 1) return experienceLevel !== '';
    if (step === 2) return selectedGenres.length >= 3;
    return true;
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <div className="mb-8">
        <Progress value={progress} className="h-2" />
        <p className="mt-2 text-sm text-muted-foreground text-center">
          Step {step} of {totalSteps}
        </p>
      </div>

      {step === 1 && (
        <Card>
          <CardHeader>
            <CardTitle>Welcome to AniVibe! 👋</CardTitle>
            <CardDescription>
              Let's personalize your anime experience. How familiar are you with anime?
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { id: 'beginner', label: 'New to Anime', desc: 'Just getting started' },
              { id: 'intermediate', label: 'Some Experience', desc: 'Watched a few series' },
              { id: 'advanced', label: 'Anime Veteran', desc: 'Seen many anime' },
              { id: 'expert', label: 'Anime Expert', desc: 'Deep knowledge and passion' },
            ].map((level) => (
              <Card
                key={level.id}
                className={`cursor-pointer transition-all hover:scale-105 ${
                  experienceLevel === level.id
                    ? 'border-primary-500 bg-primary-500/10 ring-2 ring-primary-500'
                    : 'hover:border-primary-500/50'
                }`}
                onClick={() => setExperienceLevel(level.id)}
              >
                <CardContent className="flex items-center justify-between p-4">
                  <div>
                    <p className="font-semibold">{level.label}</p>
                    <p className="text-sm text-muted-foreground">{level.desc}</p>
                  </div>
                  <div className={`h-4 w-4 rounded-full border-2 ${
                    experienceLevel === level.id ? 'bg-primary-500 border-primary-500' : 'border-muted'
                  }`} />
                </CardContent>
              </Card>
            ))}
          </CardContent>
        </Card>
      )}

      {step === 2 && (
        <Card>
          <CardHeader>
            <CardTitle>What genres interest you? 🎭</CardTitle>
            <CardDescription>
              Select at least 3 genres you enjoy (you can change these later)
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {GENRES.map((genre) => (
                <div
                  key={genre}
                  onClick={() => handleGenreToggle(genre)}
                  className={`cursor-pointer rounded-lg border-2 p-3 text-center transition-all hover:scale-105 ${
                    selectedGenres.includes(genre)
                      ? 'border-primary-500 bg-primary-500/10'
                      : 'border-border hover:border-primary-500/50'
                  }`}
                >
                  <Checkbox
                    checked={selectedGenres.includes(genre)}
                    className="mb-2"
                  />
                  <p className="text-sm font-medium">{genre}</p>
                </div>
              ))}
            </div>
            <p className="mt-4 text-sm text-muted-foreground text-center">
              {selectedGenres.length} selected (minimum 3)
            </p>
          </CardContent>
        </Card>
      )}

      {step === 3 && (
        <Card>
          <CardHeader>
            <CardTitle>You're all set! 🎉</CardTitle>
            <CardDescription>
              We'll use your preferences to recommend amazing anime tailored just for you
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm font-medium mb-2">Your Experience Level:</p>
              <p className="text-muted-foreground capitalize">{experienceLevel}</p>
            </div>
            <div>
              <p className="text-sm font-medium mb-2">Selected Genres ({selectedGenres.length}):</p>
              <div className="flex flex-wrap gap-2">
                {selectedGenres.map((genre) => (
                  <span key={genre} className="px-3 py-1 rounded-full bg-primary-500/10 text-sm">
                    {genre}
                  </span>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="mt-6 flex justify-between">
        <Button
          variant="outline"
          onClick={handleBack}
          disabled={step === 1}
        >
          <ChevronLeft className="mr-2 h-4 w-4" />
          Back
        </Button>
        <Button
          onClick={handleNext}
          disabled={!canProceed()}
        >
          {step === totalSteps ? 'Get Started' : 'Next'}
          {step < totalSteps && <ChevronRight className="ml-2 h-4 w-4" />}
        </Button>
      </div>
    </div>
  );
}
