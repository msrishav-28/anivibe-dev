'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Search, Sparkles, TrendingUp, Globe, Star, Users } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

export default function HomePage() {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-background to-background/50 py-20 md:py-32">
        <div className="absolute inset-0 bg-grid-white/10 [mask-image:radial-gradient(white,transparent_85%)]" />
        <div className="container-custom relative">
          <div className="mx-auto max-w-4xl text-center">
            <Badge className="mb-4 glassmorphism" variant="secondary">
              <Sparkles className="mr-1 h-3 w-3" />
              AI-Powered Recommendations
            </Badge>
            <h1 className="mb-6 text-5xl font-bold tracking-tight md:text-7xl">
              Discover Your Next
              <span className="gradient-text"> Favorite Anime</span>
            </h1>
            <p className="mb-8 text-lg text-muted-foreground md:text-xl">
              Experience emotion-first anime discovery with semantic search, AI recommendations,
              and interactive visualizations. Find exactly what you're looking for, even if you
              don't know the title.
            </p>

            {/* Search Bar */}
            <div className="mx-auto max-w-2xl">
              <div className="relative">
                <Input
                  placeholder='Try "dark psychological anime" or "uplifting slice of life"...'
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onClear={() => setSearchQuery('')}
                  leftIcon={<Search className="h-5 w-5" />}
                  className="h-14 text-lg"
                />
                <Button
                  size="lg"
                  className="absolute right-2 top-2 h-10"
                  onClick={() => {
                    if (searchQuery) {
                      window.location.href = `/search?q=${encodeURIComponent(searchQuery)}`;
                    }
                  }}
                >
                  Search
                </Button>
              </div>
              <p className="mt-4 text-sm text-muted-foreground">
                Powered by BERT + CLIP for understanding natural language and visual style
              </p>
            </div>

            {/* CTA Buttons */}
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Button size="lg" variant="primary" asChild>
                <Link href="/explore">
                  <Globe className="mr-2 h-5 w-5" />
                  Explore Anime
                </Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/atlas">
                  <Star className="mr-2 h-5 w-5" />
                  View Atlas
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container-custom">
          <div className="mb-12 text-center">
            <h2 className="mb-4 text-3xl font-bold md:text-4xl">
              Powerful Features for Anime Lovers
            </h2>
            <p className="text-lg text-muted-foreground">
              Everything you need to discover, track, and enjoy anime
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            <Card className="glassmorphism">
              <CardHeader>
                <Search className="mb-2 h-10 w-10 text-primary-500" />
                <CardTitle>Semantic Search</CardTitle>
                <CardDescription>
                  Search by mood, theme, or visual style - not just titles. Our AI understands
                  what you're looking for.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="glassmorphism">
              <CardHeader>
                <Sparkles className="mb-2 h-10 w-10 text-primary-500" />
                <CardTitle>AI Recommendations</CardTitle>
                <CardDescription>
                  Get personalized suggestions powered by multiple algorithms with full
                  explainability.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="glassmorphism">
              <CardHeader>
                <Globe className="mb-2 h-10 w-10 text-primary-500" />
                <CardTitle>Interactive Atlas</CardTitle>
                <CardDescription>
                  Explore 26,000+ anime in a 3D visualization space. Discover patterns and hidden
                  gems.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="glassmorphism">
              <CardHeader>
                <TrendingUp className="mb-2 h-10 w-10 text-primary-500" />
                <CardTitle>Taste Analytics</CardTitle>
                <CardDescription>
                  Understand your preferences with detailed analytics, genre distributions, and
                  viewing patterns.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="glassmorphism">
              <CardHeader>
                <Star className="mb-2 h-10 w-10 text-primary-500" />
                <CardTitle>Hidden Gems</CardTitle>
                <CardDescription>
                  Discover underrated anime you'll love. Our algorithms surface quality shows
                  beyond the mainstream.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="glassmorphism">
              <CardHeader>
                <Users className="mb-2 h-10 w-10 text-primary-500" />
                <CardTitle>Social Features</CardTitle>
                <CardDescription>
                  Connect with friends, share reviews, and see what others with similar taste are
                  watching.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="border-y border-border bg-muted/50 py-16">
        <div className="container-custom">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            <div className="text-center">
              <div className="mb-2 text-4xl font-bold gradient-text">26,000+</div>
              <div className="text-sm text-muted-foreground">Anime Titles</div>
            </div>
            <div className="text-center">
              <div className="mb-2 text-4xl font-bold gradient-text">10+</div>
              <div className="text-sm text-muted-foreground">AI Algorithms</div>
            </div>
            <div className="text-center">
              <div className="mb-2 text-4xl font-bold gradient-text">95%</div>
              <div className="text-sm text-muted-foreground">Match Accuracy</div>
            </div>
            <div className="text-center">
              <div className="mb-2 text-4xl font-bold gradient-text">24/7</div>
              <div className="text-sm text-muted-foreground">Available</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="container-custom">
          <Card className="glassmorphism border-primary-500/20 bg-gradient-to-br from-primary-500/10 to-accent-pink/10">
            <CardHeader className="text-center">
              <CardTitle className="text-3xl">Ready to Start Your Anime Journey?</CardTitle>
              <CardDescription className="text-lg">
                Join thousands of anime fans discovering their next favorite shows
              </CardDescription>
            </CardHeader>
            <CardContent className="flex justify-center gap-4">
              <Button size="lg" variant="primary" asChild>
                <Link href="/signup">Get Started Free</Link>
              </Button>
              <Button size="lg" variant="outline" asChild>
                <Link href="/explore">Browse Anime</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
}
