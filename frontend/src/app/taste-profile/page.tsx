'use client';

import { useState, useEffect } from 'react';
import { TasteProfile } from '@/components/features/taste-profile';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';
import { useAuthStore } from '@/store/auth-store';
import { api } from '@/lib/api-client';
import { GlitchText } from '@/components/ui/glitch-text';

export default function TasteProfilePage() {
  const { user } = useAuthStore();
  const [profile, setProfile] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (user) {
      loadProfile();
    }
  }, [user]);

  const loadProfile = async () => {
    setIsLoading(true);
    try {
      const tasteProfile = await api.getTasteProfile();
      setProfile(tasteProfile);
    } catch (error) {
      console.error('Failed to load taste profile:', error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Card>
          <CardContent className="p-8 text-center">
            <p className="text-lg text-muted-foreground">
              Please log in to view your taste profile
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <div className="container-custom py-12">
        {/* Header */}
        <div className="mb-10 flex items-center justify-between">
          <div>
            <GlitchText text="NEURAL SYNCHRONIZATION" as="h1" className="mb-2 text-4xl font-bold font-heading" />
            <p className="text-muted-foreground">
              Analysis of your anime preferences and viewing habits
            </p>
          </div>
          <Button variant="outline" onClick={loadProfile} disabled={isLoading}>
            <RefreshCw className={`mr-2 h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>

        {/* Profile */}
        {isLoading ? (
          <div className="text-center py-12">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent mx-auto" />
            <p className="mt-4 text-muted-foreground">Loading your taste profile...</p>
          </div>
        ) : profile ? (
          <TasteProfile profile={profile} />
        ) : (
          <Card>
            <CardContent className="py-12 text-center">
              <p className="text-lg text-muted-foreground mb-4">
                Not enough data to generate your taste profile yet
              </p>
              <p className="text-sm text-muted-foreground">
                Rate more anime to see personalized insights!
              </p>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
