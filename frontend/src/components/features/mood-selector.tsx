'use client';

import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Smile, Heart, Zap, Brain, Sparkles, Coffee, Moon, Sun } from 'lucide-react';

interface Mood {
  id: string;
  name: string;
  icon: any;
  color: string;
  description: string;
}

const MOODS: Mood[] = [
  { id: 'happy', name: 'Happy', icon: Smile, color: 'bg-yellow-500', description: 'Cheerful and uplifting' },
  { id: 'romantic', name: 'Romantic', icon: Heart, color: 'bg-pink-500', description: 'Love and feelings' },
  { id: 'exciting', name: 'Exciting', icon: Zap, color: 'bg-orange-500', description: 'Action-packed thrills' },
  { id: 'thoughtful', name: 'Thoughtful', icon: Brain, color: 'bg-purple-500', description: 'Deep and philosophical' },
  { id: 'whimsical', name: 'Whimsical', icon: Sparkles, color: 'bg-blue-500', description: 'Magical and fantastical' },
  { id: 'relaxed', name: 'Relaxed', icon: Coffee, color: 'bg-green-500', description: 'Calm and peaceful' },
  { id: 'dark', name: 'Dark', icon: Moon, color: 'bg-gray-700', description: 'Serious and intense' },
  { id: 'optimistic', name: 'Optimistic', icon: Sun, color: 'bg-amber-500', description: 'Hopeful and bright' },
];

interface MoodSelectorProps {
  selectedMood?: string;
  onMoodChange: (mood: string) => void;
}

export function MoodSelector({ selectedMood, onMoodChange }: MoodSelectorProps) {
  return (
    <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
      {MOODS.map((mood) => {
        const Icon = mood.icon;
        const isSelected = selectedMood === mood.id;

        return (
          <Card
            key={mood.id}
            className={`cursor-pointer transition-all hover:scale-105 ${
              isSelected
                ? 'border-primary-500 bg-primary-500/10 ring-2 ring-primary-500'
                : 'hover:border-primary-500/50'
            }`}
            onClick={() => onMoodChange(mood.id)}
          >
            <CardContent className="flex flex-col items-center p-6 text-center">
              <div className={`mb-3 rounded-full ${mood.color} p-4`}>
                <Icon className="h-6 w-6 text-white" />
              </div>
              <h3 className="mb-1 font-semibold">{mood.name}</h3>
              <p className="text-xs text-muted-foreground">{mood.description}</p>
            </CardContent>
          </Card>
        );
      })}
    </div>
  );
}
