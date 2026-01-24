import { useQuery } from '@tanstack/react-query';
import { api } from '@/lib/api-client';
import { Anime, User, UserStats } from '@/types';

// ==================== KEY CONFIG ====================
// Stale Time: 5 minutes (Data is considered fresh for 5 mins)
// Cache Time: 30 minutes (Unused data stays in memory)
const STALE_TIME = 1000 * 60 * 5;

export function useAnime(id: number) {
    return useQuery({
        queryKey: ['anime', id],
        queryFn: () => api.getAnime(id),
        staleTime: STALE_TIME,
        retry: 1, // Don't retry indefinitely if 404
    });
}

export function useSimilarAnime(id: number) {
    return useQuery({
        queryKey: ['anime', id, 'similar'],
        queryFn: async () => {
            const recommendations = await api.getSimilarAnime(id, 12);
            // Map recommendations to just the Anime object for the UI
            return recommendations.map(rec => rec.anime || rec);
        },
        staleTime: STALE_TIME,
    });
}

export function useUserStats(userId?: string) {
    return useQuery({
        queryKey: ['user', userId || 'me', 'stats'],
        queryFn: () => api.getUserStats(userId),
        staleTime: 1000 * 60 * 2, // Stats update slightly more often
        enabled: !!userId, // Only run if userId exists
    });
}

export function useAnimeReviews(animeId: number, page: number = 1) {
    return useQuery({
        queryKey: ['anime', animeId, 'reviews', page],
        queryFn: () => api.getAnimeReviews(animeId, page),
        staleTime: 1000 * 60, // Reviews update frequently
    });
}
