'use client';

import { useState } from 'react';
import { X, SlidersHorizontal } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Checkbox } from '@/components/ui/checkbox';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@radix-ui/react-scroll-area';

interface FilterSidebarProps {
  onFiltersChange: (filters: any) => void;
  initialFilters?: any;
}

const GENRES = [
  'Action', 'Adventure', 'Comedy', 'Drama', 'Fantasy', 'Horror',
  'Mystery', 'Psychological', 'Romance', 'Sci-Fi', 'Slice of Life',
  'Sports', 'Supernatural', 'Thriller'
];

const TYPES = ['TV', 'Movie', 'OVA', 'ONA', 'Special'];
const STATUSES = ['Finished Airing', 'Currently Airing', 'Not yet aired'];

export function FilterSidebar({ onFiltersChange, initialFilters = {} }: FilterSidebarProps) {
  const [filters, setFilters] = useState({
    genres: initialFilters.genres || [],
    types: initialFilters.types || [],
    statuses: initialFilters.statuses || [],
    ratingRange: initialFilters.ratingRange || [0, 10],
    yearRange: initialFilters.yearRange || [1960, 2024],
    sort: initialFilters.sort || 'popularity_desc',
  });

  const updateFilter = (key: string, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFiltersChange(newFilters);
  };

  const toggleArrayFilter = (key: string, value: string) => {
    const current = filters[key as keyof typeof filters] as string[];
    const updated = current.includes(value)
      ? current.filter((item) => item !== value)
      : [...current, value];
    updateFilter(key, updated);
  };

  const clearFilters = () => {
    const defaultFilters = {
      genres: [],
      types: [],
      statuses: [],
      ratingRange: [0, 10],
      yearRange: [1960, 2024],
      sort: 'popularity_desc',
    };
    setFilters(defaultFilters);
    onFiltersChange(defaultFilters);
  };

  const activeFilterCount =
    filters.genres.length + filters.types.length + filters.statuses.length;

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-border p-4">
        <div className="flex items-center gap-2">
          <SlidersHorizontal className="h-5 w-5" />
          <h2 className="font-semibold">Filters</h2>
          {activeFilterCount > 0 && (
            <Badge variant="secondary">{activeFilterCount}</Badge>
          )}
        </div>
        <Button variant="ghost" size="sm" onClick={clearFilters}>
          Clear All
        </Button>
      </div>

      {/* Filters */}
      <div className="flex-1 overflow-auto p-4">
        <Accordion type="multiple" defaultValue={['sort', 'genres', 'rating']} className="space-y-2">
          {/* Sort */}
          <AccordionItem value="sort">
            <AccordionTrigger>Sort By</AccordionTrigger>
            <AccordionContent>
              <Select value={filters.sort} onValueChange={(value) => updateFilter('sort', value)}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="popularity_desc">Most Popular</SelectItem>
                  <SelectItem value="rating_desc">Highest Rated</SelectItem>
                  <SelectItem value="rating_asc">Lowest Rated</SelectItem>
                  <SelectItem value="year_desc">Newest</SelectItem>
                  <SelectItem value="year_asc">Oldest</SelectItem>
                  <SelectItem value="title_asc">Title A-Z</SelectItem>
                  <SelectItem value="title_desc">Title Z-A</SelectItem>
                </SelectContent>
              </Select>
            </AccordionContent>
          </AccordionItem>

          {/* Genres */}
          <AccordionItem value="genres">
            <AccordionTrigger>
              Genres
              {filters.genres.length > 0 && (
                <Badge variant="secondary" className="ml-2">
                  {filters.genres.length}
                </Badge>
              )}
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-2">
                {GENRES.map((genre) => (
                  <div key={genre} className="flex items-center space-x-2">
                    <Checkbox
                      id={`genre-${genre}`}
                      checked={filters.genres.includes(genre)}
                      onCheckedChange={() => toggleArrayFilter('genres', genre)}
                    />
                    <label
                      htmlFor={`genre-${genre}`}
                      className="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                    >
                      {genre}
                    </label>
                  </div>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Rating */}
          <AccordionItem value="rating">
            <AccordionTrigger>Rating</AccordionTrigger>
            <AccordionContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between text-sm">
                  <span>{filters.ratingRange[0].toFixed(1)}</span>
                  <span>{filters.ratingRange[1].toFixed(1)}</span>
                </div>
                <Slider
                  min={0}
                  max={10}
                  step={0.5}
                  value={filters.ratingRange}
                  onValueChange={(value) => updateFilter('ratingRange', value)}
                />
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Year */}
          <AccordionItem value="year">
            <AccordionTrigger>Year</AccordionTrigger>
            <AccordionContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between text-sm">
                  <span>{filters.yearRange[0]}</span>
                  <span>{filters.yearRange[1]}</span>
                </div>
                <Slider
                  min={1960}
                  max={2024}
                  step={1}
                  value={filters.yearRange}
                  onValueChange={(value) => updateFilter('yearRange', value)}
                />
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Type */}
          <AccordionItem value="type">
            <AccordionTrigger>
              Type
              {filters.types.length > 0 && (
                <Badge variant="secondary" className="ml-2">
                  {filters.types.length}
                </Badge>
              )}
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-2">
                {TYPES.map((type) => (
                  <div key={type} className="flex items-center space-x-2">
                    <Checkbox
                      id={`type-${type}`}
                      checked={filters.types.includes(type)}
                      onCheckedChange={() => toggleArrayFilter('types', type)}
                    />
                    <label
                      htmlFor={`type-${type}`}
                      className="text-sm font-medium leading-none"
                    >
                      {type}
                    </label>
                  </div>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>

          {/* Status */}
          <AccordionItem value="status">
            <AccordionTrigger>
              Status
              {filters.statuses.length > 0 && (
                <Badge variant="secondary" className="ml-2">
                  {filters.statuses.length}
                </Badge>
              )}
            </AccordionTrigger>
            <AccordionContent>
              <div className="space-y-2">
                {STATUSES.map((status) => (
                  <div key={status} className="flex items-center space-x-2">
                    <Checkbox
                      id={`status-${status}`}
                      checked={filters.statuses.includes(status)}
                      onCheckedChange={() => toggleArrayFilter('statuses', status)}
                    />
                    <label
                      htmlFor={`status-${status}`}
                      className="text-sm font-medium leading-none"
                    >
                      {status}
                    </label>
                  </div>
                ))}
              </div>
            </AccordionContent>
          </AccordionItem>
        </Accordion>
      </div>
    </div>
  );
}
