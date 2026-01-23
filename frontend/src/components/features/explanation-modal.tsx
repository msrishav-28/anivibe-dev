'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ExplanationCard } from './explanation-card';
import { api } from '@/lib/api-client';
import { Loader2 } from 'lucide-react';

interface ExplanationModalProps {
  animeId: number;
  isOpen: boolean;
  onClose: () => void;
}

export function ExplanationModal({ animeId, isOpen, onClose }: ExplanationModalProps) {
  const [explanations, setExplanations] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedMethod, setSelectedMethod] = useState('hybrid');

  const loadExplanation = useCallback(async () => {
    setIsLoading(true);
    try {
      const result = await api.explainRecommendation(animeId, selectedMethod);
      setExplanations([result]);
    } catch (error) {
      console.error('Failed to load explanation:', error);
    } finally {
      setIsLoading(false);
    }
  }, [animeId, selectedMethod]);

  useEffect(() => {
    if (isOpen && animeId) {
      loadExplanation();
    }
  }, [isOpen, animeId, loadExplanation]);

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Recommendation Explanation</DialogTitle>
          <DialogDescription>
            Understand why this anime was recommended to you
          </DialogDescription>
        </DialogHeader>

        <Tabs value={selectedMethod} onValueChange={setSelectedMethod}>
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="hybrid">Hybrid</TabsTrigger>
            <TabsTrigger value="collaborative">Collaborative</TabsTrigger>
            <TabsTrigger value="content">Content</TabsTrigger>
            <TabsTrigger value="semantic">Semantic</TabsTrigger>
          </TabsList>

          <TabsContent value={selectedMethod} className="mt-4">
            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-primary-500" />
              </div>
            ) : explanations.length > 0 ? (
              <div className="space-y-4">
                {explanations.map((exp, idx) => (
                  <ExplanationCard key={idx} explanation={exp} />
                ))}
              </div>
            ) : (
              <div className="py-12 text-center text-muted-foreground">
                No explanation available for this method
              </div>
            )}
          </TabsContent>
        </Tabs>

        <div className="flex justify-end">
          <Button variant="outline" onClick={onClose}>
            Close
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}
