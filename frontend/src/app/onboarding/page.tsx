'use client';

import { useRouter } from 'next/navigation';
import { OnboardingFlow } from '@/components/features/onboarding-flow';
import { useUIStore } from '@/store/ui-store';

export default function OnboardingPage() {
  const router = useRouter();
  // const { user } = useAuthStore(); // Unused
  const { addToast } = useUIStore();

  const handleComplete = async (preferences: any) => {
    try {
      // Save user preferences (would call API here)
      console.log('User preferences:', preferences);

      addToast({
        title: 'Welcome to AniVibe!',
        description: 'Your preferences have been saved. Enjoy personalized recommendations!',
        type: 'success',
      });

      // Redirect to explore page
      router.push('/explore');
    } catch (error) {
      addToast({
        title: 'Error',
        description: 'Failed to save preferences',
        type: 'error',
      });
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-primary-500/5 to-accent-pink/5 py-12">
      <OnboardingFlow onComplete={handleComplete} />
    </div>
  );
}
