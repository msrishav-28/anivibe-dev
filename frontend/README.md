# AniVibe Frontend

A modern, AI-powered anime discovery platform built with Next.js 14, TypeScript, and Tailwind CSS.

## 🚀 Features

- **Semantic Search**: Natural language search powered by BERT and CLIP
- **AI Recommendations**: Multi-algorithm ensemble recommendations with explainability
- **Interactive Atlas**: 3D visualization of 26,000+ anime
- **User Profiles**: Comprehensive analytics and personalization
- **Social Features**: Friends, reviews, discussions
- **Responsive Design**: Mobile-first approach with beautiful UI
- **Dark Mode**: Default dark theme with light mode support
- **Accessibility**: WCAG 2.1 AA compliant
- **Performance Optimized**: Code splitting, lazy loading, image optimization

## 📋 Prerequisites

- Node.js 18.17.0 or higher
- npm 9.0.0 or higher
- Backend API running on http://localhost:8000 (or configured URL)

## 🛠️ Installation

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.local.example .env.local
   ```
   
   Edit `.env.local` with your configuration:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXT_PUBLIC_APP_URL=http://localhost:3000
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```

5. **Open your browser**:
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📦 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint errors
- `npm run format` - Format code with Prettier
- `npm run type-check` - Run TypeScript type checking
- `npm test` - Run Jest tests
- `npm run e2e` - Run Playwright E2E tests
- `npm run storybook` - Start Storybook development server
- `npm run analyze` - Analyze bundle size

## 🏗️ Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js 14 App Router pages
│   │   ├── (auth)/            # Auth routes group
│   │   ├── (main)/            # Main app routes
│   │   ├── layout.tsx         # Root layout
│   │   └── page.tsx           # Home page
│   ├── components/            # React components
│   │   ├── ui/               # Base UI components
│   │   ├── features/         # Feature-specific components
│   │   ├── layout/           # Layout components
│   │   └── shared/           # Shared components
│   ├── hooks/                # Custom React hooks
│   ├── lib/                  # Utility libraries
│   │   ├── api-client.ts    # API client
│   │   └── utils.ts          # Utility functions
│   ├── store/                # Zustand stores
│   │   ├── auth-store.ts    # Authentication state
│   │   ├── watchlist-store.ts # Watchlist state
│   │   └── ui-store.ts       # UI state
│   ├── styles/               # Global styles
│   │   └── globals.css       # Global CSS
│   ├── types/                # TypeScript types
│   │   └── index.ts          # Type definitions
│   └── config/               # Configuration
│       └── tokens.ts         # Design tokens
├── public/                   # Static files
├── tests/                    # Test files
├── .storybook/              # Storybook configuration
├── next.config.mjs          # Next.js configuration
├── tailwind.config.ts       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies
```

## 🎨 Design System

The project uses a comprehensive design token system defined in `src/config/tokens.ts`:

- **Colors**: Primary (purple), accent (pink, blue), semantic colors, anime genre colors
- **Typography**: Outfit (headings), Inter (body), JetBrains Mono (code)
- **Spacing**: 8px base unit system
- **Animation**: Standardized durations and easing functions
- **Components**: Consistent sizing for buttons, inputs, cards

## 🧩 Key Components

### Base Components (23 core components)

1. **Button** - 8 variants with loading states
2. **Input** - Text, search, tags, range sliders
3. **Card** - Anime cards with hover animations
4. **Modal** - Dialogs and full-screen views
5. **Toast** - Notifications with auto-dismiss
6. **Skeleton** - Loading placeholders
7. **Badge** - Genre tags and status indicators
8. **Dropdown** - Menus and select components
9. **Progress** - Loading and progress indicators
10. **Tooltip** - Contextual help

...and 13 more components

## 📱 Pages

### Core Pages (12 pages)

1. **Landing** (`/`) - Hero section with semantic search
2. **Explore** (`/explore`) - Filterable anime grid
3. **Anime Detail** (`/anime/[id]`) - Full anime information
4. **Search** (`/search`) - Advanced semantic search
5. **Atlas** (`/atlas`) - Interactive 3D visualization
6. **Profile** (`/profile`) - User dashboard and analytics
7. **Watchlist** (`/watchlist`) - User's anime list
8. **Reviews** (`/reviews`) - Community reviews
9. **Social** (`/social`) - Friends and activity feed
10. **Login/Signup** (`/login`, `/signup`) - Authentication
11. **Settings** (`/settings`) - User preferences
12. **404** - Error page

## 🔐 Authentication

The app uses JWT-based authentication:

- Tokens stored in localStorage
- Automatic token refresh
- Protected routes with middleware
- OAuth support (Google, GitHub, Discord)

## 📊 State Management

Using Zustand for global state:

- **Auth Store**: User authentication and profile
- **Watchlist Store**: User's anime list
- **UI Store**: Theme, modals, toasts, loading states

## 🎯 API Integration

The `api-client.ts` provides type-safe API methods:

```typescript
import { api } from '@/lib/api-client';

// Search anime
const results = await api.semanticSearch('emotional romance');

// Get recommendations
const recommendations = await api.getRecommendations();

// Add to watchlist
await api.addToWatchlist(animeId, 'watching');
```

## 🧪 Testing

### Unit Tests (Jest)
```bash
npm test
npm run test:watch
npm run test:coverage
```

### E2E Tests (Playwright)
```bash
npm run e2e
npm run e2e:ui
```

## 📖 Storybook

Component documentation and visual testing:

```bash
npm run storybook
```

Visit [http://localhost:6006](http://localhost:6006)

## 🎨 Styling

### Tailwind CSS

The project uses Tailwind CSS with custom design tokens:

```tsx
// Using design tokens
<div className="bg-primary-500 text-white rounded-lg p-lg">
  Content
</div>

// Using utility classes
<div className="glassmorphism gradient-text">
  Glass effect with gradient text
</div>
```

### Framer Motion

Animations with Framer Motion:

```tsx
import { motion } from 'framer-motion';

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  Animated content
</motion.div>
```

## ♿ Accessibility

- Semantic HTML
- ARIA labels and roles
- Keyboard navigation
- Focus management
- Screen reader support
- Color contrast (4.5:1)
- Reduced motion support

## 📈 Performance

- **Code Splitting**: Automatic route-based splitting
- **Image Optimization**: Next.js Image component with WebP
- **Lazy Loading**: Components and images below fold
- **Bundle Analysis**: Use `npm run analyze`
- **Caching**: React Query for API responses
- **Prefetching**: Link prefetching for faster navigation

Target Metrics:
- LCP < 2.5s
- FID < 100ms
- CLS < 0.1
- Lighthouse Score ≥ 90

## 🚀 Deployment

### Vercel (Recommended)

```bash
npm run build
vercel --prod
```

### Docker

```bash
docker build -t anivibe-frontend .
docker run -p 3000:3000 anivibe-frontend
```

### Static Export

```bash
npm run build
npm run export
```

## 🔧 Configuration

### Environment Variables

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_3D_ATLAS=true

# Analytics (Optional)
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=
NEXT_PUBLIC_SENTRY_DSN=
```

### Tailwind Configuration

Customize in `tailwind.config.ts`:

```typescript
export default {
  theme: {
    extend: {
      colors: {
        // Add custom colors
      },
    },
  },
};
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Kill process on port 3000
   npx kill-port 3000
   ```

2. **Dependencies not installing**:
   ```bash
   # Clear npm cache
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **API connection errors**:
   - Check backend is running on correct port
   - Verify `NEXT_PUBLIC_API_URL` in `.env.local`
   - Check CORS settings in backend

## 📝 Development Guidelines

### Code Style

- Use TypeScript for type safety
- Follow ESLint and Prettier rules
- Use functional components with hooks
- Prefer composition over inheritance
- Write descriptive variable names

### Component Guidelines

- One component per file
- Export as default
- Include TypeScript types
- Document props with JSDoc
- Keep components small and focused

### Commit Messages

Follow conventional commits:

```
feat: Add semantic search component
fix: Resolve anime card hover bug
docs: Update README installation steps
style: Format code with Prettier
refactor: Simplify API client error handling
test: Add watchlist store tests
```

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Run linting and formatting
5. Submit a pull request

## 📄 License

This project is proprietary and confidential.

## 🙏 Acknowledgments

- Next.js team for the amazing framework
- shadcn/ui for component inspiration
- MyAnimeList and AniList for data sources

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact: dev@anivibe.com

---

Built with ❤️ by the AniVibe team
