import type { Metadata } from 'next';
import { Inter, Outfit } from 'next/font/google';
import { Header } from '@/components/layout/header';
import { Footer } from '@/components/layout/footer';
import { ErrorBoundary } from '@/components/error-boundary';
import { ToastProvider } from '@/components/toast-provider';
import '@/styles/globals.css';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const outfit = Outfit({ subsets: ['latin'], variable: '--font-outfit' });

export const metadata: Metadata = {
  title: 'AniVibe - AI-Powered Anime Discovery',
  description:
    'Discover your next favorite anime with AI-powered recommendations, semantic search, and interactive visualizations.',
  keywords: ['anime', 'recommendations', 'AI', 'discovery', 'semantic search'],
  authors: [{ name: 'AniVibe Team' }],
  openGraph: {
    title: 'AniVibe - AI-Powered Anime Discovery',
    description: 'Discover your next favorite anime with AI',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.variable} ${outfit.variable} font-sans`}>
        <ErrorBoundary>
          <div className="relative flex min-h-screen flex-col">
            <Header />
            <main className="flex-1">{children}</main>
            <Footer />
          </div>
          <ToastProvider />
        </ErrorBoundary>
      </body>
    </html>
  );
}
