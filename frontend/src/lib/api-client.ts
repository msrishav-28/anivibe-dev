import axios, { AxiosError } from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';
type AuthTokenProvider = () => Promise<string | null> | string | null;
let authTokenProvider: AuthTokenProvider | null = null;

export function setAuthTokenProvider(provider: AuthTokenProvider | null) {
  authTokenProvider = provider;
}

async function fileToDataUrl(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result));
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

// Create axios instance
const client = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token
client.interceptors.request.use(
  async (config) => {
    const token = authTokenProvider ? await authTokenProvider() : null;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - Handle errors globally
client.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// API methods
export const api = {
  // ==================== AUTH ====================
  login: async (email: string, password: string) => {
    void email;
    void password;
    throw new Error('Login is handled by Clerk. Use the Clerk SignIn component.');
  },

  register: async (data: {
    username: string;
    email: string;
    password: string;
    display_name?: string;
  }) => {
    void data;
    throw new Error('Signup is handled by Clerk. Use the Clerk SignUp component.');
  },

  logout: async () => {
    throw new Error('Logout is handled by Clerk. Use the Clerk signOut action.');
  },

  getCurrentUser: async () => {
    const response = await client.get('/auth/me');
    return response.data;
  },

  // ==================== ANIME ====================
  getAnime: async (id: number) => {
    const response = await client.get(`/anime/${id}`);
    return response.data;
  },

  searchAnime: async (query: string, page = 1, limit = 20) => {
    const response = await client.get('/anime', {
      params: { query, page, limit },
    });
    return response.data;
  },

  getAnimeList: async (params?: Record<string, unknown>) => {
    const response = await client.get('/anime', { params });
    return response.data;
  },

  getTrendingAnime: async (limit = 20) => {
    const response = await client.get('/anime/trending', {
      params: { limit },
    });
    return response.data;
  },

  getPopularAnime: async (limit = 20) => {
    const response = await client.get('/anime/popular', {
      params: { limit },
    });
    return response.data;
  },

  // ==================== SEARCH ====================
  semanticSearch: async (query: string, limit = 20) => {
    const response = await client.post('/search/semantic', {
      query,
      top_k: limit,
    });
    return response.data;
  },

  imageSearch: async (imageFile: File, limit = 20) => {
    const imageUrl = await fileToDataUrl(imageFile);
    const response = await client.post('/search/visual', {
      image_url: imageUrl,
      top_k: limit,
    });
    return response.data;
  },

  // ==================== RECOMMENDATIONS ====================
  getRecommendations: async (params?: {
    user_id?: string;
    limit?: number;
    strategy?: 'hybrid' | 'collaborative' | 'content' | 'gnn' | 'bert4rec';
  }) => {
    const response = await client.post('/recommendations/personalized', {
      top_k: params?.limit ?? 20,
      method: params?.strategy ?? 'hybrid',
    });
    return response.data;
  },

  getSimilarAnime: async (animeId: number, limit = 12) => {
    const response = await client.post('/recommendations/similar', {
      anime_id: animeId,
      top_k: limit,
    });
    return response.data;
  },

  getPersonalized: async (limit = 20) => {
    // Backend expects POST with top_k
    const response = await client.post('/recommendations/personalized', {
      top_k: limit,
      method: 'hybrid'
    });
    return response.data;
  },

  getHiddenGems: async (
    input: number | { min_score?: number; max_popularity?: number; top_k?: number } = 20
  ) => {
    const body = typeof input === 'number' ? { top_k: input } : input;
    const response = await client.post('/recommendations/hidden-gems', body);
    return response.data.recommendations?.map((item: any) => item.anime ?? item) ?? response.data.items ?? [];
  },

  // ==================== EXPLAINABILITY ====================
  explainRecommendation: async (animeId: number, method?: string) => {
    const response = await client.get(`/explain/anime/${animeId}/why-recommended`, {
      params: { method },
    });
    return response.data;
  },

  // ==================== RATINGS ====================
  rateAnime: async (animeId: number, score: number) => {
    const response = await client.post('/ratings', {
      anime_id: animeId,
      score,
    });
    return response.data;
  },

  createRating: async (data: { anime_id: number; score: number; review_text?: string }) => {
    const response = await client.post('/ratings', {
      anime_id: data.anime_id,
      score: data.score,
      review: data.review_text,
    });
    return response.data;
  },

  updateRating: async (ratingId: number, data: { score?: number; review_text?: string }) => {
    const response = await client.put(`/ratings/${ratingId}`, {
      score: data.score,
      review: data.review_text,
    });
    return response.data;
  },

  getUserRating: async (animeId: number) => {
    const response = await client.get(`/ratings/anime/${animeId}`);
    return response.data;
  },

  deleteRating: async (animeId: number) => {
    const response = await client.delete(`/ratings/anime/${animeId}`);
    return response.data;
  },

  // ==================== REVIEWS ====================
  getAnimeReviews: async (animeId: number, page = 1, limit = 10) => {
    const response = await client.get(`/anime/${animeId}/reviews`, {
      params: { page, limit },
    });
    return response.data;
  },

  createReview: async (animeId: number, content: string, rating: number) => {
    const response = await client.post(`/anime/${animeId}/reviews`, {
      content,
      rating,
    });
    return response.data;
  },

  updateReview: async (reviewId: number, content: string, rating: number) => {
    const response = await client.patch(`/reviews/${reviewId}`, {
      content,
      rating,
    });
    return response.data;
  },

  deleteReview: async (reviewId: number) => {
    const response = await client.delete(`/reviews/${reviewId}`);
    return response.data;
  },

  likeReview: async (reviewId: number) => {
    const response = await client.post(`/reviews/${reviewId}/vote`, { helpful: true });
    return response.data;
  },

  // ==================== WATCHLIST ====================
  getWatchlist: async (status?: 'watching' | 'completed' | 'plan_to_watch' | 'dropped') => {
    const response = await client.get('/watchlist', {
      params: { status },
    });
    return response.data;
  },

  addToWatchlist: async (animeId: number, status: string) => {
    const response = await client.post('/watchlist', {
      anime_id: animeId,
      status,
    });
    return response.data;
  },

  updateWatchlistStatus: async (animeId: number, status: string, progress?: number) => {
    const response = await client.put(`/watchlist/${animeId}`, {
      status,
      progress,
    });
    return response.data;
  },

  removeFromWatchlist: async (animeId: number) => {
    const response = await client.delete(`/watchlist/${animeId}`);
    return response.data;
  },

  updateWatchlistEntry: async (entryId: number, data: Record<string, unknown>) => {
    const response = await client.put(`/watchlist/${entryId}`, data);
    return response.data;
  },

  // ==================== USER PROFILE ====================
  getUserProfile: async (userId?: string) => {
    const response = await client.get(`/users/${userId || 'me'}`);
    return response.data;
  },

  updateProfile: async (data: {
    display_name?: string;
    bio?: string;
    avatar_url?: string;
    favorite_genres?: string[];
  }) => {
    const response = await client.put('/users/me', data);
    return response.data;
  },

  getUserStats: async (userId?: string) => {
    const response = await client.get(`/users/${userId || 'me'}/stats`);
    return response.data;
  },

  getTasteProfile: async (userId?: string) => {
    void userId;
    const response = await client.get('/recommendations/taste-profile');
    return response.data;
  },

  // ==================== ANALYTICS ====================
  getUserAnalytics: async () => {
    const response = await client.get('/analytics/genres');
    return response.data;
  },

  getWatchTimeAnalytics: async () => {
    const response = await client.get('/analytics/heatmap');
    return response.data;
  },

  getGenreDistribution: async () => {
    const response = await client.get('/analytics/genres');
    return response.data;
  },

  searchAutocomplete: async (query: string, limit = 10) => {
    const response = await client.get('/search/autocomplete', {
      params: { query, limit },
    });
    return response.data;
  },

  // ==================== ATLAS ====================
  getAtlas: async () => {
    return { nodes: [], edges: [], feature_status: 'experimental' };
  },

  getAtlasData: async () => {
    return api.getAtlas();
  },
};

// Export client for custom requests
export { client };
