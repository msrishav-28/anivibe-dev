# AniVibe Frontend Setup Guide

This guide will help you set up the AniVibe frontend from scratch.

## Quick Start

```bash
# 1. Navigate to frontend directory
cd frontend

# 2. Install dependencies
npm install

# 3. Copy environment variables
cp .env.local.example .env.local

# 4. Start development server
npm run dev
```

## Detailed Installation Steps

### 1. Prerequisites Check

Verify you have the required versions:

```bash
node --version  # Should be >= 18.17.0
npm --version   # Should be >= 9.0.0
```

If you need to update Node.js, visit [nodejs.org](https://nodejs.org)

### 2. Install Dependencies

The project uses many modern packages. Installation might take 2-5 minutes:

```bash
npm install
```

This will install:
- **Next.js 14**: React framework with App Router
- **React 18**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Utility-first CSS
- **Framer Motion**: Animations
- **Zustand**: State management
- **React Query**: Server state management
- **Axios**: HTTP client
- **Radix UI**: Accessible components
- **Lucide React**: Icons
- **D3.js & Recharts**: Data visualization
- **Three.js**: 3D graphics
- **And many more...**

### 3. Environment Configuration

Create `.env.local` file:

```bash
cp .env.local.example .env.local
```

Edit the file with your settings:

```env
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000

# Optional Feature Flags
NEXT_PUBLIC_ENABLE_ANALYTICS=true
NEXT_PUBLIC_ENABLE_3D_ATLAS=true

# Optional Analytics
NEXT_PUBLIC_GOOGLE_ANALYTICS_ID=
NEXT_PUBLIC_SENTRY_DSN=
```

### 4. Verify Backend Connection

Make sure the backend API is running:

```bash
# Test backend connection
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

If backend is not running, start it first:

```bash
cd ../  # Go to root directory
make dev  # or python -m uvicorn app.main:app --reload
```

### 5. Start Development Server

```bash
npm run dev
```

You should see:

```
   ▲ Next.js 14.2.0
   - Local:        http://localhost:3000
   - Ready in 2.5s
```

### 6. Open in Browser

Navigate to [http://localhost:3000](http://localhost:3000)

You should see the AniVibe landing page with:
- Hero section with search bar
- Trending anime carousel
- Feature cards

## Development Workflow

### File Watching

The development server watches for file changes and hot-reloads automatically:

- **React components**: Instant hot reload
- **Tailwind CSS**: Automatic recompilation
- **TypeScript**: Real-time type checking

### Lint on Save

Configure your editor to lint on save:

**VS Code** (`.vscode/settings.json`):
```json
{
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### Type Checking

Run type check manually:

```bash
npm run type-check
```

## Building for Production

### Local Production Build

```bash
# Build the application
npm run build

# Start production server
npm start
```

### Build Output

The build process:
1. Compiles TypeScript to JavaScript
2. Bundles and minifies code
3. Optimizes images
4. Generates static pages
5. Creates optimized CSS

Expected build output:

```
Route (app)                              Size     First Load JS
┌ ○ /                                   5.2 kB         85.3 kB
├ ○ /anime/[id]                          3.8 kB         95.7 kB
├ ○ /explore                             4.1 kB         92.4 kB
├ ○ /search                              3.9 kB         89.1 kB
└ ○ /profile                             4.3 kB         97.2 kB

○  (Static)  automatically rendered as static HTML
```

### Bundle Analysis

Analyze bundle size:

```bash
npm run analyze
```

This will:
1. Build the project
2. Generate bundle visualization
3. Open analysis in browser

## Testing

### Unit Tests

```bash
# Run all tests
npm test

# Watch mode (re-run on changes)
npm run test:watch

# Coverage report
npm run test:coverage
```

### E2E Tests

```bash
# Run E2E tests
npm run e2e

# UI mode (interactive)
npm run e2e:ui

# Specific browser
npx playwright test --project=chromium
```

## Component Development

### Storybook

Develop components in isolation:

```bash
npm run storybook
```

Access at [http://localhost:6006](http://localhost:6006)

Features:
- Component library
- Interactive props
- Visual testing
- Accessibility checks
- Responsive preview

### Creating New Components

Use this template:

```tsx
// src/components/ui/MyComponent.tsx
import { cn } from '@/lib/utils';
import type { ComponentBaseProps } from '@/types';

export interface MyComponentProps extends ComponentBaseProps {
  variant?: 'default' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

export function MyComponent({
  variant = 'default',
  size = 'md',
  className,
  children,
}: MyComponentProps) {
  return (
    <div className={cn('my-component', className)}>
      {children}
    </div>
  );
}
```

Create Storybook story:

```tsx
// src/components/ui/MyComponent.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { MyComponent } from './MyComponent';

const meta: Meta<typeof MyComponent> = {
  title: 'UI/MyComponent',
  component: MyComponent,
  tags: ['autodocs'],
};

export default meta;
type Story = StoryObj<typeof MyComponent>;

export const Default: Story = {
  args: {
    children: 'My Component',
  },
};
```

## Troubleshooting

### Issue: Port 3000 in use

```bash
# Find and kill process
npx kill-port 3000

# Or use different port
PORT=3001 npm run dev
```

### Issue: Module not found

```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm cache clean --force
npm install
```

### Issue: TypeScript errors

```bash
# Restart TypeScript server in VS Code
# Ctrl+Shift+P -> "TypeScript: Restart TS Server"

# Or run type check
npm run type-check
```

### Issue: Styles not updating

```bash
# Clear Next.js cache
rm -rf .next

# Restart dev server
npm run dev
```

### Issue: API connection failed

1. Check backend is running: `curl http://localhost:8000/health`
2. Verify `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Check browser console for CORS errors
4. Ensure backend allows `http://localhost:3000` origin

### Issue: Build fails

```bash
# Check for TypeScript errors
npm run type-check

# Check for lint errors
npm run lint

# Clear and rebuild
rm -rf .next
npm run build
```

## IDE Setup

### VS Code Extensions

Recommended extensions:

```json
{
  "recommendations": [
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "ms-playwright.playwright",
    "csstools.postcss"
  ]
}
```

Install all:
```
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension bradlc.vscode-tailwindcss
```

### WebStorm/IntelliJ IDEA

1. Enable ESLint: Settings → Languages & Frameworks → JavaScript → Code Quality Tools → ESLint
2. Enable Prettier: Settings → Languages & Frameworks → JavaScript → Prettier
3. Enable Tailwind CSS: Settings → Languages & Frameworks → Style Sheets → Tailwind CSS

## Performance Optimization

### Development

- Use React DevTools Profiler
- Monitor bundle size with `npm run analyze`
- Check Core Web Vitals in Lighthouse

### Production

- Enable compression (Gzip/Brotli)
- Use CDN for static assets
- Implement service worker for caching
- Optimize images with Next.js Image

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy
vercel --prod
```

### Docker

```bash
# Build image
docker build -t anivibe-frontend .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=https://api.anivibe.com \
  anivibe-frontend
```

### Static Export

```bash
# Build static site
npm run build
npm run export

# Output in 'out' directory
# Deploy to any static host (Netlify, GitHub Pages, etc.)
```

## Next Steps

1. ✅ Complete setup
2. 📖 Read [README.md](./README.md) for full documentation
3. 🎨 Explore components in Storybook
4. 🧪 Run tests to verify everything works
5. 🚀 Start building!

## Getting Help

- 📚 Documentation: [README.md](./README.md)
- 🐛 Report bugs: GitHub Issues
- 💬 Ask questions: Team Slack/Discord
- 📧 Email: dev@anivibe.com

---

Happy coding! 🎉
