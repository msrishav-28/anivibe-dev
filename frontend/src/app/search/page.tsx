'use client';

import { useState } from 'react';
import { SemanticSearch } from '@/components/features/semantic-search';
import { AnimeGrid } from '@/components/features/anime-grid';
import { Card, CardContent } from '@/components/ui/card';
import type { Anime, SemanticSearchResult } from '@/types';

export default function SearchPage() {
  const [results, setResults] = useState<Anime[]>([]);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = (_query: string, searchResults: SemanticSearchResult[]) => {
    setHasSearched(true);
    // Convert search results to Anime objects
    const animeResults = searchResults.map((result) => result.anime);
    setResults(animeResults);
  };

  return (
    <div className="min-h-screen">
      <div className="container-custom py-12">
        {/* Header */}
        <div className="mb-8 text-center">
          <h1 className="mb-4 text-4xl font-bold">Semantic Search</h1>
          <p className="text-lg text-muted-foreground">
            Search by emotion, mood, visual style, or theme - our AI understands what you're
            looking for
          </p>
        </div>

        {/* Search Component */}
        <div className="mx-auto max-w-3xl">
          <SemanticSearch onSearch={handleSearch} />
        </div>

        {/* Results */}
        {hasSearched && (
          <div className="mt-12">
            {results.length > 0 ? (
              <>
                <h2 className="mb-6 text-2xl font-bold">
                  Found {results.length} results
                </h2>
                <AnimeGrid anime={results} />
              </>
            ) : (
              <Card>
                <CardContent className="py-12 text-center">
                  <p className="text-lg text-muted-foreground">
                    No results found. Try adjusting your search query.
                  </p>
                </CardContent>
              </Card>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
