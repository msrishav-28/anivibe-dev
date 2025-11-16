/**
 * Design Token System
 * Centralized design constants for consistency across the application
 */

export const tokens = {
  // Color Palette
  colors: {
    primary: {
      50: '#faf5ff',
      100: '#f3e8ff',
      200: '#e9d5ff',
      300: '#d8b4fe',
      400: '#c084fc',
      500: '#8b5cf6',
      600: '#7c3aed',
      700: '#6d28d9',
      800: '#5b21b6',
      900: '#4c1d95',
      950: '#2e1065',
    },
    accent: {
      pink: '#ec4899',
      blue: '#3b82f6',
      cyan: '#06b6d4',
    },
    semantic: {
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444',
      info: '#3b82f6',
    },
    anime: {
      action: '#ef4444',
      romance: '#ec4899',
      fantasy: '#8b5cf6',
      scifi: '#3b82f6',
      thriller: '#6366f1',
      comedy: '#f59e0b',
      drama: '#8b5cf6',
      sliceoflife: '#10b981',
      mystery: '#6366f1',
      horror: '#dc2626',
    },
    neutral: {
      50: '#f8fafc',
      100: '#f1f5f9',
      200: '#e2e8f0',
      300: '#cbd5e1',
      400: '#94a3b8',
      500: '#64748b',
      600: '#475569',
      700: '#334155',
      800: '#1e293b',
      900: '#0f172a',
      950: '#020617',
    },
  },

  // Spacing Scale
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
    '3xl': '64px',
    '4xl': '96px',
  },

  // Border Radius
  radius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    '2xl': '24px',
    full: '9999px',
  },

  // Shadows
  shadows: {
    glow: '0 0 20px rgba(139, 92, 246, 0.3)',
    'glow-lg': '0 0 40px rgba(139, 92, 246, 0.4)',
    card: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    float: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
    'float-lg': '0 30px 40px -10px rgb(0 0 0 / 0.15)',
  },

  // Animation Durations
  animation: {
    durations: {
      instant: '150ms',
      fast: '300ms',
      normal: '500ms',
      slow: '800ms',
    },
    easings: {
      standard: 'cubic-bezier(0.4, 0.0, 0.2, 1)',
      decelerate: 'cubic-bezier(0.0, 0.0, 0.2, 1)',
      accelerate: 'cubic-bezier(0.4, 0.0, 1, 1)',
      bounce: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    },
  },

  // Typography
  typography: {
    fontSizes: {
      xs: '0.75rem',    // 12px
      sm: '0.875rem',   // 14px
      base: '1rem',     // 16px
      lg: '1.125rem',   // 18px
      xl: '1.25rem',    // 20px
      '2xl': '1.5rem',  // 24px
      '3xl': '1.875rem', // 30px
      '4xl': '2.25rem', // 36px
      '5xl': '3rem',    // 48px
      '6xl': '3.75rem', // 60px
      '7xl': '4.5rem',  // 72px
    },
    fontWeights: {
      thin: 100,
      extralight: 200,
      light: 300,
      normal: 400,
      medium: 500,
      semibold: 600,
      bold: 700,
      extrabold: 800,
      black: 900,
    },
    lineHeights: {
      tight: 1.25,
      snug: 1.375,
      normal: 1.5,
      relaxed: 1.625,
      loose: 2,
    },
    letterSpacings: {
      tighter: '-0.05em',
      tight: '-0.025em',
      normal: '0em',
      wide: '0.025em',
      wider: '0.05em',
      widest: '0.1em',
    },
  },

  // Breakpoints
  breakpoints: {
    xs: '320px',
    sm: '480px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },

  // Z-Index Scale
  zIndex: {
    base: 0,
    dropdown: 1000,
    sticky: 1100,
    fixed: 1200,
    modalBackdrop: 1300,
    modal: 1400,
    popover: 1500,
    tooltip: 1600,
    toast: 1700,
  },

  // Component Sizes
  components: {
    animeCard: {
      grid: {
        desktop: { width: '280px', height: '420px' },
        mobile: { width: '160px', height: '240px' },
      },
      list: {
        desktop: { width: '100%', height: '140px' },
        mobile: { width: '100%', height: '120px' },
      },
      featured: {
        desktop: { width: '350px', height: '500px' },
        mobile: { width: '200px', height: '300px' },
      },
    },
    button: {
      sm: { height: '32px', padding: '0 12px', fontSize: '0.875rem' },
      md: { height: '40px', padding: '0 16px', fontSize: '1rem' },
      lg: { height: '48px', padding: '0 24px', fontSize: '1.125rem' },
    },
    input: {
      sm: { height: '32px', padding: '0 12px', fontSize: '0.875rem' },
      md: { height: '40px', padding: '0 16px', fontSize: '1rem' },
      lg: { height: '48px', padding: '0 20px', fontSize: '1.125rem' },
    },
  },
};

// Genre color mapping
export const genreColors: Record<string, string> = {
  Action: tokens.colors.anime.action,
  Adventure: '#f59e0b',
  Comedy: tokens.colors.anime.comedy,
  Drama: tokens.colors.anime.drama,
  Fantasy: tokens.colors.anime.fantasy,
  Horror: tokens.colors.anime.horror,
  Mystery: tokens.colors.anime.mystery,
  Psychological: '#6366f1',
  Romance: tokens.colors.anime.romance,
  'Sci-Fi': tokens.colors.anime.scifi,
  'Slice of Life': tokens.colors.anime.sliceoflife,
  Supernatural: '#8b5cf6',
  Thriller: tokens.colors.anime.thriller,
  Sports: '#10b981',
  Music: '#ec4899',
  Mecha: '#3b82f6',
};

// Mood tag colors
export const moodColors: Record<string, string> = {
  emotional: '#ec4899',
  dark: '#1e293b',
  uplifting: '#10b981',
  intense: '#ef4444',
  calm: '#06b6d4',
  comedic: '#f59e0b',
  melancholic: '#6366f1',
  inspiring: '#8b5cf6',
};

// Rarity colors for achievements/badges
export const rarityColors = {
  common: '#94a3b8',
  rare: '#3b82f6',
  epic: '#8b5cf6',
  legendary: '#f59e0b',
};

// Status colors
export const statusColors = {
  watching: '#3b82f6',
  completed: '#10b981',
  on_hold: '#f59e0b',
  dropped: '#ef4444',
  plan_to_watch: '#94a3b8',
};

// Sentiment colors
export const sentimentColors = {
  positive: '#10b981',
  neutral: '#94a3b8',
  negative: '#ef4444',
};

export type ColorToken = keyof typeof tokens.colors;
export type SpacingToken = keyof typeof tokens.spacing;
export type RadiusToken = keyof typeof tokens.radius;
export type AnimationDuration = keyof typeof tokens.animation.durations;
export type AnimationEasing = keyof typeof tokens.animation.easings;
