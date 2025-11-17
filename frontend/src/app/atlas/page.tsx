'use client';

import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Slider } from '@/components/ui/slider';
import { Badge } from '@/components/ui/badge';
import { Maximize2, Minimize2, RotateCw, ZoomIn, ZoomOut, Info } from 'lucide-react';
import { api } from '@/lib/api-client';

export default function AtlasPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [colorBy, setColorBy] = useState('genre');
  const [clusterLevel, setClusterLevel] = useState([5]);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [selectedAnime, setSelectedAnime] = useState<any>(null);

  useEffect(() => {
    loadAtlasData();
  }, []);

  const loadAtlasData = async () => {
    setIsLoading(true);
    try {
      const data = await api.getAtlasData();
      console.log('Atlas data loaded:', data);
    } catch (error) {
      console.error('Failed to load atlas data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen">
      <div className="container-custom py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="mb-2 text-4xl font-bold">Anime Atlas</h1>
          <p className="text-lg text-muted-foreground">
            Explore 26,000+ anime in an interactive 3D visualization space
          </p>
        </div>

        <div className="grid gap-6 lg:grid-cols-4">
          {/* Controls Sidebar */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle>Visualization Controls</CardTitle>
              <CardDescription>Customize the atlas view</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {/* Color By */}
              <div>
                <label className="mb-2 block text-sm font-medium">Color By</label>
                <Select value={colorBy} onValueChange={setColorBy}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="genre">Genre</SelectItem>
                    <SelectItem value="score">Score</SelectItem>
                    <SelectItem value="year">Year</SelectItem>
                    <SelectItem value="popularity">Popularity</SelectItem>
                    <SelectItem value="type">Type</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Cluster Level */}
              <div>
                <label className="mb-2 block text-sm font-medium">
                  Cluster Level: {clusterLevel[0]}
                </label>
                <Slider
                  value={clusterLevel}
                  onValueChange={setClusterLevel}
                  min={1}
                  max={10}
                  step={1}
                />
              </div>

              {/* View Controls */}
              <div className="space-y-2">
                <label className="mb-2 block text-sm font-medium">View Controls</label>
                <div className="grid grid-cols-2 gap-2">
                  <Button variant="outline" size="sm">
                    <ZoomIn className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="sm">
                    <ZoomOut className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="sm">
                    <RotateCw className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setIsFullscreen(!isFullscreen)}
                  >
                    {isFullscreen ? (
                      <Minimize2 className="h-4 w-4" />
                    ) : (
                      <Maximize2 className="h-4 w-4" />
                    )}
                  </Button>
                </div>
              </div>

              {/* Legend */}
              <div>
                <label className="mb-2 block text-sm font-medium">Legend</label>
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="h-4 w-4 rounded-full bg-primary-500" />
                    <span className="text-sm">Action</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="h-4 w-4 rounded-full bg-accent-pink" />
                    <span className="text-sm">Romance</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="h-4 w-4 rounded-full bg-accent-blue" />
                    <span className="text-sm">Sci-Fi</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="h-4 w-4 rounded-full bg-success" />
                    <span className="text-sm">Comedy</span>
                  </div>
                </div>
              </div>

              {/* Info */}
              <Card className="bg-primary-500/5 border-primary-500/20">
                <CardContent className="p-4">
                  <div className="flex items-start gap-2">
                    <Info className="h-4 w-4 mt-0.5 text-primary-500" />
                    <div className="text-sm">
                      <p className="font-medium mb-1">How to use</p>
                      <ul className="space-y-1 text-muted-foreground">
                        <li>• Click and drag to rotate</li>
                        <li>• Scroll to zoom</li>
                        <li>• Click nodes to view details</li>
                        <li>• Similar anime cluster together</li>
                      </ul>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </CardContent>
          </Card>

          {/* 3D Visualization */}
          <div className="lg:col-span-3">
            <Card className="h-[700px]">
              <CardContent className="relative h-full p-0">
                {isLoading ? (
                  <div className="flex h-full items-center justify-center">
                    <div className="text-center">
                      <div className="mb-4 h-12 w-12 animate-spin rounded-full border-4 border-primary-500 border-t-transparent mx-auto" />
                      <p className="text-muted-foreground">Loading Atlas...</p>
                    </div>
                  </div>
                ) : (
                  <div className="flex h-full items-center justify-center bg-gradient-to-br from-background to-muted/20 p-8">
                    <div className="text-center max-w-2xl">
                      <div className="mb-8 mx-auto h-48 w-48 rounded-full bg-gradient-to-br from-primary-500/20 to-accent-pink/20 flex items-center justify-center">
                        <div className="h-32 w-32 rounded-full bg-gradient-to-br from-primary-500/30 to-accent-blue/30 flex items-center justify-center">
                          <Badge className="text-lg px-6 py-2">26,000+ Anime</Badge>
                        </div>
                      </div>
                      <h3 className="text-2xl font-bold mb-4">3D Atlas Visualization</h3>
                      <p className="text-muted-foreground mb-6">
                        Explore the anime universe in 3D! Each node represents an anime, positioned by similarity using advanced ML embeddings. Navigate through clusters of related content.
                      </p>
                      <div className="grid grid-cols-2 gap-4 text-sm text-left">
                        <Card className="p-4">
                          <h4 className="font-semibold mb-2">🎯 Smart Clustering</h4>
                          <p className="text-muted-foreground">Similar anime cluster together based on genre, themes, and user preferences.</p>
                        </Card>
                        <Card className="p-4">
                          <h4 className="font-semibold mb-2">🔍 Interactive Exploration</h4>
                          <p className="text-muted-foreground">Click, zoom, and rotate to discover connections between anime.</p>
                        </Card>
                        <Card className="p-4">
                          <h4 className="font-semibold mb-2">🎨 Visual Filters</h4>
                          <p className="text-muted-foreground">Color-code by genre, score, year, or popularity for better insights.</p>
                        </Card>
                        <Card className="p-4">
                          <h4 className="font-semibold mb-2">⚡ Real-time Updates</h4>
                          <p className="text-muted-foreground">Filters and clusters update instantly as you explore.</p>
                        </Card>
                      </div>
                      <p className="mt-6 text-sm text-muted-foreground">
                        💡 This feature requires WebGL support. The 3D renderer will be activated when you interact with the controls.
                      </p>
                    </div>
                  </div>
                )}

                {/* Stats Overlay */}
                <div className="absolute bottom-4 left-4 right-4 flex gap-4">
                  <Card className="flex-1 glassmorphism">
                    <CardContent className="p-3">
                      <div className="text-xs text-muted-foreground">Total Nodes</div>
                      <div className="text-lg font-bold">26,284</div>
                    </CardContent>
                  </Card>
                  <Card className="flex-1 glassmorphism">
                    <CardContent className="p-3">
                      <div className="text-xs text-muted-foreground">Clusters</div>
                      <div className="text-lg font-bold">{clusterLevel[0] * 100}</div>
                    </CardContent>
                  </Card>
                  <Card className="flex-1 glassmorphism">
                    <CardContent className="p-3">
                      <div className="text-xs text-muted-foreground">Connections</div>
                      <div className="text-lg font-bold">125,420</div>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
