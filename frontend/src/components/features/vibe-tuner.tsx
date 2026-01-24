'use client';

import { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { motion } from 'framer-motion';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

export function VibeTuner() {
    const [query, setQuery] = useState('');
    const [moodColor, setMoodColor] = useState('rgba(139,92,246,0.3)'); // Default Spirit Purple

    // Dynamic Mood Logic
    useEffect(() => {
        const lower = query.toLowerCase();
        if (lower.includes('sad') || lower.includes('lonely') || lower.includes('rain')) {
            setMoodColor('rgba(59,130,246,0.6)'); // Blue
        } else if (lower.includes('hype') || lower.includes('action') || lower.includes('fight')) {
            setMoodColor('rgba(239,68,68,0.6)'); // Red
        } else if (lower.includes('chill') || lower.includes('healing') || lower.includes('nature')) {
            setMoodColor('rgba(16,185,129,0.6)'); // Green
        } else if (lower.includes('dark') || lower.includes('horror')) {
            setMoodColor('rgba(0,0,0,0.8)'); // Void
        } else {
            setMoodColor('rgba(139,92,246,0.3)'); // Default
        }
    }, [query]);

    const handleSearch = () => {
        if (query) {
            window.location.href = `/search?q=${encodeURIComponent(query)}`;
        }
    };

    return (
        <div className="mx-auto max-w-3xl relative z-20">
            <motion.div
                className="relative group"
                animate={{
                    boxShadow: `0 0 20px ${moodColor}`,
                }}
                transition={{ duration: 0.5 }}
            >
                {/* Pulse Effect */}
                <motion.div
                    className="absolute -inset-1 rounded-full opacity-20 blur-lg transition duration-500 pointer-events-none"
                    animate={{
                        backgroundColor: moodColor,
                        scale: [1, 1.02, 1],
                    }}
                    transition={{
                        duration: 2,
                        repeat: Infinity,
                        ease: "easeInOut"
                    }}
                />

                <Input
                    placeholder="Type a feeling... 'cyberpunk rain', 'healing slice of life'"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                    leftIcon={<Search className="h-5 w-5" />}
                    className="h-16 text-lg bg-black/40 backdrop-blur-xl border-white/10 rounded-full pl-12 pr-16 focus-visible:ring-0 focus-visible:border-white/20 transition-all placeholder:text-muted-foreground/50"
                />

                <Button
                    size="icon"
                    variant="ghost" // Changed to ghost to blend better, or keep custom style
                    className="absolute right-2 top-2 h-12 w-12 rounded-full bg-white/5 hover:bg-white/10 transition-colors"
                    onClick={handleSearch}
                    style={{
                        boxShadow: `0 0 10px ${moodColor}`
                    }}
                >
                    <Search className="h-5 w-5 text-white" />
                </Button>
            </motion.div>

            {/* Neural Status Indicators */}
            <div className="mt-6 flex flex-wrap justify-center gap-4 text-sm text-muted-foreground/60 font-mono">
                <span className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-success animate-pulse"></span>
                    CLIP Vision Model Active
                </span>
                <span className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-secondary animate-pulse"></span>
                    BERT Semantic Analysis Ready
                </span>
            </div>
        </div>
    );
}
