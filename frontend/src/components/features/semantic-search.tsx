'use client';

import { useState } from 'react';
import { Search, Sparkles, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import { api } from '@/lib/api-client';
import { useDebounce } from '@/hooks/use-debounce';
import type { SemanticSearchResult } from '@/types';

interface SemanticSearchProps {
  onSearch: (query: string, results: SemanticSearchResult[]) => void;
  placeholder?: string;
  className?: string;
}

const EXAMPLE_QUERIES = [
  'emotional romance with beautiful animation',
  'dark psychological thriller',
  'uplifting slice of life',
  'intense action with complex plot',
  'supernatural mystery with twists',
  'comedy with wholesome characters',
];

export function SemanticSearch({
  onSearch,
  placeholder = 'Describe what you\'re looking for...',
  className = '',
}: SemanticSearchProps) {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [queryUnderstanding, setQueryUnderstanding] = useState<any>(null);
  const debouncedQuery = useDebounce(query, 500);

  const handleSearch = async (searchQuery: string) => {
    if (!searchQuery.trim()) return;

    setIsSearching(true);
    try {
      const results = await api.semanticSearch(searchQuery);
      
      // Extract query understanding from first result if available
      if (results.length > 0 && results[0].query_understanding) {
        setQueryUnderstanding(results[0].query_understanding);
      }
      
      onSearch(searchQuery, results);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
    handleSearch(example);
  };

  return (
    <div className={className}>
      {/* Search Input */}
      <div className="relative">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSearch(query);
            }
          }}
          placeholder={placeholder}
          leftIcon={<Search className="h-5 w-5" />}
          onClear={() => setQuery('')}
          className="h-14 text-lg"
        />
        <Button
          size="lg"
          className="absolute right-2 top-2 h-10"
          onClick={() => handleSearch(query)}
          loading={isSearching}
          disabled={!query.trim()}
        >
          <Sparkles className="mr-2 h-4 w-4" />
          Search
        </Button>
      </div>

      {/* Query Understanding */}
      {queryUnderstanding && (
        <Card className="mt-4 border-primary-500/20 bg-primary-500/5">
          <CardContent className="p-4">
            <div className="flex items-start gap-2">
              <Sparkles className="mt-1 h-5 w-5 text-primary-500" />
              <div className="flex-1">
                <p className="mb-2 text-sm font-medium">AI Understanding</p>
                <div className="space-y-2">
                  {queryUnderstanding.emotions?.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      <span className="text-xs text-muted-foreground">Emotions:</span>
                      {queryUnderstanding.emotions.map((emotion: string) => (
                        <Badge key={emotion} variant="secondary" className="text-xs">
                          {emotion}
                        </Badge>
                      ))}
                    </div>
                  )}
                  {queryUnderstanding.genres?.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      <span className="text-xs text-muted-foreground">Genres:</span>
                      {queryUnderstanding.genres.map((genre: string) => (
                        <Badge key={genre} variant="secondary" className="text-xs">
                          {genre}
                        </Badge>
                      ))}
                    </div>
                  )}
                  {queryUnderstanding.themes?.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      <span className="text-xs text-muted-foreground">Themes:</span>
                      {queryUnderstanding.themes.map((theme: string) => (
                        <Badge key={theme} variant="secondary" className="text-xs">
                          {theme}
                        </Badge>
                      ))}
                    </div>
                  )}
                  {queryUnderstanding.visual_elements?.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      <span className="text-xs text-muted-foreground">Visual Style:</span>
                      {queryUnderstanding.visual_elements.map((element: string) => (
                        <Badge key={element} variant="secondary" className="text-xs">
                          {element}
                        </Badge>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Example Queries */}
      {!query && !queryUnderstanding && (
        <div className="mt-6">
          <p className="mb-3 text-sm text-muted-foreground">Try these examples:</p>
          <div className="flex flex-wrap gap-2">
            {EXAMPLE_QUERIES.map((example) => (
              <button
                key={example}
                onClick={() => handleExampleClick(example)}
                className="rounded-full border border-border bg-background px-4 py-2 text-sm transition-colors hover:border-primary-500 hover:bg-primary-500/10"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Tips */}
      <div className="mt-6 rounded-lg border border-border/50 bg-muted/30 p-4">
        <p className="mb-2 text-sm font-medium">💡 Search Tips</p>
        <ul className="space-y-1 text-xs text-muted-foreground">
          <li>• Describe emotions: "heartwarming", "intense", "dark"</li>
          <li>• Mention visual style: "beautiful animation", "vibrant colors"</li>
          <li>• Include themes: "coming of age", "time travel", "supernatural"</li>
          <li>• Combine multiple aspects for better results</li>
        </ul>
      </div>
    </div>
  );
}
