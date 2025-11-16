// Core Anime Types
export interface Anime {
  anime_id: number;
  title: string;
  english_title?: string;
  japanese_title?: string;
  synopsis: string;
  genres: string[];
  themes: string[];
  demographics: string[];
  studios: string[];
  producers: string[];
  type: 'TV' | 'Movie' | 'OVA' | 'ONA' | 'Special';
  status: 'Finished Airing' | 'Currently Airing' | 'Not yet aired';
  episodes?: number;
  duration?: number;
  aired_from?: string;
  aired_to?: string;
  season?: string;
  year?: number;
  rating: string;
  score: number;
  scored_by: number;
  rank?: number;
  popularity?: number;
  members: number;
  favorites: number;
  image_url: string;
  trailer_url?: string;
  tags: string[];
  visual_tags?: string[];
  mood_tags?: string[];
}

// User Types
export interface User {
  user_id: number;
  username: string;
  email: string;
  display_name?: string;
  avatar_url?: string;
  cover_url?: string;
  bio?: string;
  location?: string;
  birthday?: string;
  pronouns?: string;
  social_links?: {
    twitter?: string;
    instagram?: string;
    youtube?: string;
    mal?: string;
    anilist?: string;
  };
  preferences: UserPreferences;
  stats: UserStats;
  created_at: string;
  last_active?: string;
}

export interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  language: string;
  notifications: NotificationPreferences;
  privacy: PrivacySettings;
  recommendations: RecommendationSettings;
}

export interface NotificationPreferences {
  email: boolean;
  push: boolean;
  in_app: boolean;
  new_releases: boolean;
  friend_activity: boolean;
  recommendations: boolean;
}

export interface PrivacySettings {
  profile_visibility: 'public' | 'private' | 'friends';
  show_statistics: boolean;
  show_ratings: boolean;
  show_reviews: boolean;
  allow_friend_requests: boolean;
  show_activity: boolean;
}

export interface RecommendationSettings {
  popularity_preference: number; // 0 (hidden gems) to 1 (mainstream)
  novelty_vs_familiarity: number; // 0 (similar) to 1 (surprise)
  rating_threshold: number; // Minimum rating (1-10)
  explicit_content: boolean;
  preferred_format: ('TV' | 'Movie' | 'OVA' | 'ONA')[];
}

export interface UserStats {
  total_anime: number;
  total_episodes: number;
  total_watch_time: number; // in minutes
  average_rating: number;
  completion_rate: number;
  genres_distribution: Record<string, number>;
  top_studios: Array<{ name: string; count: number }>;
}

// Watchlist Types
export interface WatchlistEntry {
  entry_id: number;
  user_id: number;
  anime_id: number;
  anime: Anime;
  status: 'watching' | 'completed' | 'on_hold' | 'dropped' | 'plan_to_watch';
  episodes_watched: number;
  score?: number;
  start_date?: string;
  finish_date?: string;
  notes?: string;
  rewatches: number;
  priority: number;
  tags: string[];
  created_at: string;
  updated_at: string;
}

// Recommendation Types
export interface Recommendation {
  anime: Anime;
  match_score: number; // 0-1
  explanation: RecommendationExplanation;
  confidence: number;
  novelty_score: number;
  algorithms_used: string[];
}

export interface RecommendationExplanation {
  genre_similarity: number;
  rating_match: number;
  user_affinity: number;
  similar_themes: string[];
  visual_similarity?: number;
  text_similarity?: number;
  feature_importance: Record<string, number>;
}

// Search Types
export interface SearchQuery {
  query: string;
  filters?: SearchFilters;
  sort?: SortOption;
  page?: number;
  limit?: number;
}

export interface SearchFilters {
  genres?: string[];
  themes?: string[];
  moods?: string[];
  visual_tags?: string[];
  year_range?: [number, number];
  rating_range?: [number, number];
  type?: ('TV' | 'Movie' | 'OVA' | 'ONA' | 'Special')[];
  status?: ('Finished Airing' | 'Currently Airing' | 'Not yet aired')[];
  studios?: string[];
  popularity?: 'mainstream' | 'balanced' | 'hidden_gems';
}

export type SortOption = 
  | 'relevance' 
  | 'rating_desc' 
  | 'rating_asc' 
  | 'popularity_desc' 
  | 'popularity_asc' 
  | 'year_desc' 
  | 'year_asc' 
  | 'title_asc' 
  | 'title_desc';

export interface SearchResult {
  anime: Anime;
  relevance_score: number;
  match_breakdown: {
    visual_match?: number;
    mood_match?: number;
    text_match?: number;
    overall_match: number;
  };
}

export interface SemanticSearchResult extends SearchResult {
  query_understanding: {
    visual_elements: string[];
    emotions: string[];
    genres: string[];
    themes: string[];
  };
}

// Review Types
export interface Review {
  review_id: number;
  user_id: number;
  user: {
    username: string;
    avatar_url?: string;
  };
  anime_id: number;
  title: string;
  content: string;
  rating: number;
  sentiment: 'positive' | 'neutral' | 'negative';
  helpful_count: number;
  spoiler: boolean;
  created_at: string;
  updated_at: string;
}

// Social Types
export interface Friend {
  user_id: number;
  username: string;
  display_name?: string;
  avatar_url?: string;
  taste_affinity: number;
  mutual_anime: number;
  status: 'pending' | 'accepted';
  created_at: string;
}

export interface Activity {
  activity_id: number;
  user_id: number;
  user: {
    username: string;
    avatar_url?: string;
  };
  type: 'completed' | 'watching' | 'rated' | 'reviewed' | 'added';
  anime_id: number;
  anime: Anime;
  metadata?: {
    rating?: number;
    episodes_watched?: number;
  };
  created_at: string;
}

// Analytics Types
export interface GenreDistribution {
  genre: string;
  count: number;
  percentage: number;
  color: string;
}

export interface WatchTimeHeatmap {
  date: string;
  episodes: number;
  hours: number;
}

export interface TasteProfile {
  preferences: {
    action: number;
    romance: number;
    comedy: number;
    drama: number;
    fantasy: number;
    scifi: number;
    thriller: number;
    slice_of_life: number;
  };
  mood_distribution: {
    emotional: number;
    dark: number;
    uplifting: number;
    intense: number;
    calm: number;
    comedic: number;
  };
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
  has_next: boolean;
  has_prev: boolean;
}

// Component Prop Types
export interface ComponentBaseProps {
  className?: string;
  children?: React.ReactNode;
}

export interface AnimeCardProps extends ComponentBaseProps {
  anime: Anime;
  variant?: 'grid' | 'list' | 'compact' | 'featured';
  showStats?: boolean;
  onHover?: 'expand' | 'glow' | 'lift';
  contextMenu?: string[];
  onClick?: () => void;
}

export interface ButtonProps extends ComponentBaseProps {
  variant?: 'primary' | 'secondary' | 'ghost' | 'outline' | 'danger' | 'success';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}

// Achievement & Gamification Types
export interface Achievement {
  achievement_id: number;
  name: string;
  description: string;
  category: 'milestone' | 'genre' | 'social' | 'discovery' | 'special';
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
  icon_url: string;
  points: number;
  unlocked: boolean;
  unlocked_at?: string;
  progress?: {
    current: number;
    required: number;
  };
}

export interface Badge {
  badge_id: number;
  name: string;
  icon_url: string;
  rarity: 'common' | 'rare' | 'epic' | 'legendary';
  animated: boolean;
}

// Chart Data Types
export interface ChartDataPoint {
  label: string;
  value: number;
  color?: string;
}

export interface TimeSeriesDataPoint {
  date: string;
  value: number;
}

// Atlas Visualization Types
export interface AtlasNode {
  anime_id: number;
  x: number;
  y: number;
  z?: number;
  title: string;
  image_url: string;
  genre: string;
  rating: number;
  popularity: number;
  color: string;
  size: number;
}

export interface AtlasCluster {
  cluster_id: number;
  label: string;
  center: [number, number, number?];
  nodes: AtlasNode[];
  color: string;
}

// Form Types
export interface LoginFormData {
  email: string;
  password: string;
  remember: boolean;
}

export interface SignupFormData {
  username: string;
  email: string;
  password: string;
  confirm_password: string;
  agree_terms: boolean;
}

export interface OnboardingData {
  favorite_genres: string[];
  ratings: Array<{ anime_id: number; rating: number }>;
  import_from?: 'mal' | 'anilist' | null;
  import_username?: string;
}
