// ==================== ANIME ====================
export interface Anime {
  id: number;
  anime_id?: number;
  mal_id?: number;
  anilist_id?: number;
  title: string;
  title_english?: string;
  title_japanese?: string;
  english_title?: string;
  japanese_title?: string;
  synopsis?: string;
  genres?: Array<string | { id?: number; name: string; description?: string }>;
  themes?: string[];
  tags?: Array<string | { id?: number; name: string; category?: string }>;
  demographics?: string[];
  rating?: number | string;
  score?: number;
  scored_by?: number;
  rank?: number;
  popularity?: number;
  members?: number;
  favorites?: number;
  episodes?: number;
  status?: string;
  type?: string;
  season?: string;
  year?: number;
  studio?: string;
  studios?: Array<string | { id?: number; name: string }>;
  image_url?: string;
  trailer_url?: string;
  created_at?: string;
  updated_at?: string;
}

// ==================== USER ====================
export interface User {
  id: string;
  user_id?: string;
  external_auth_id?: string;
  username: string;
  email: string;
  full_name?: string;
  display_name?: string;
  bio?: string;
  avatar_url?: string;
  favorite_genres?: string[];
  anime_watched?: number;
  episodes_watched?: number;
  watch_time_hours?: number;
  created_at?: string;
}

export interface UserStats {
  total_anime_watched: number;
  total_episodes: number;
  total_watch_time_hours: number;
  average_rating: number;
  favorite_genres: { genre: string; count: number }[];
  top_rated_anime: Anime[];
}

// ==================== RECOMMENDATIONS ====================
export interface Recommendation {
  anime: Anime;
  score: number;
  reason?: string;
  strategy?: string;
}

export interface SemanticSearchResult {
  anime: Anime;
  similarity_score: number;
  query_understanding?: {
    emotions: string[];
    genres: string[];
    themes: string[];
    visual_elements: string[];
  };
}

// ==================== RATINGS ====================
export interface Rating {
  id: number;
  user_id: string;
  anime_id: number;
  score: number;
  created_at: string;
  updated_at: string;
}

// ==================== REVIEWS ====================
export interface Review {
  id: number;
  user_id: string;
  anime_id: number;
  content: string;
  rating: number;
  likes: number;
  sentiment?: 'positive' | 'neutral' | 'negative';
  created_at: string;
  updated_at: string;
  user?: User;
}

// ==================== WATCHLIST ====================
export interface WatchlistEntry {
  id: number;
  entry_id?: number;
  user_id: string;
  anime_id: number;
  status: 'watching' | 'completed' | 'plan_to_watch' | 'dropped' | 'on_hold';
  progress: number;
  anime?: Anime;
  score?: number;
  episodes_watched?: number;
  created_at: string;
  updated_at: string;
}

// ==================== EXPLAINABILITY ====================
export interface Explanation {
  anime_id: number;
  method: 'shap' | 'lime';
  factors: {
    feature: string;
    importance: number;
    description: string;
  }[];
  similar_anime: Anime[];
  user_preference_match: {
    genre_match: number;
    theme_match: number;
    style_match: number;
  };
}

// ==================== API RESPONSES ====================
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  has_more: boolean;
}
