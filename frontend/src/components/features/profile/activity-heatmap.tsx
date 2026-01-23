'use client';

import { motion } from 'framer-motion';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { cn } from '@/lib/utils';

// Mock data generator for the heatmap
const generateHeatmapData = () => {
    const today = new Date();
    const data = [];
    // Generate last 365 days
    for (let i = 364; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        // Random intensity 0-4
        // Make weekends more active specifically for "weeb" realism
        const isWeekend = date.getDay() === 0 || date.getDay() === 6;
        const baseChance = isWeekend ? 0.7 : 0.4;
        const intensity = Math.random() > (1 - baseChance) ? Math.floor(Math.random() * 5) : 0;

        data.push({
            date: date.toISOString().split('T')[0],
            intensity, // 0: none, 1: light, 2: medium, 3: high, 4: extreme
        });
    }
    return data;
};

const heatmapData = generateHeatmapData();

const intensityColors = {
    0: 'bg-white/5',
    1: 'bg-primary/20',
    2: 'bg-primary/40',
    3: 'bg-primary/70',
    4: 'bg-primary shadow-[0_0_10px_theme(colors.primary.DEFAULT)]',
};

import { Card } from '@/components/ui/card';

// ... imports

export function ActivityHeatmap() {
    return (
        <Card variant="holo" className="w-full overflow-x-auto p-6 border-white/10">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold uppercase tracking-widest text-white/70">Sync Rate (365 Days)</h3>
                <div className="flex gap-2 items-center text-xs text-muted-foreground">
                    <span>Less</span>
                    <div className="flex gap-1">
                        <div className={`h-3 w-3 rounded-sm ${intensityColors[0]}`} />
                        <div className={`h-3 w-3 rounded-sm ${intensityColors[2]}`} />
                        <div className={`h-3 w-3 rounded-sm ${intensityColors[4]}`} />
                    </div>
                    <span>More</span>
                </div>
            </div>

            <div className="flex gap-1 min-w-max">
                {/* Simple columns logic: 52 columns of 7 days */}
                {Array.from({ length: 53 }).map((_, colIndex) => (
                    <div key={colIndex} className="flex flex-col gap-1">
                        {Array.from({ length: 7 }).map((_, rowIndex) => {
                            const dayIndex = colIndex * 7 + rowIndex;
                            if (dayIndex >= heatmapData.length) return null;

                            const day = heatmapData[dayIndex];
                            if (!day) return null;

                            return (
                                <TooltipProvider key={day.date} delayDuration={0}>
                                    <Tooltip>
                                        <TooltipTrigger asChild>
                                            <motion.div
                                                initial={{ scale: 0 }}
                                                animate={{ scale: 1 }}
                                                transition={{ delay: dayIndex * 0.002, duration: 0.2 }}
                                                className={cn(
                                                    "h-3 w-3 rounded-sm transition-all duration-300 hover:scale-125 hover:z-10",
                                                    intensityColors[day.intensity as keyof typeof intensityColors],
                                                    day.intensity > 2 && "shadow-glow"
                                                )}
                                            />
                                        </TooltipTrigger>
                                        <TooltipContent side="top">
                                            <span className="font-mono">{day.date}</span>: <span className="text-primary-400 font-bold">{day.intensity > 0 ? `${day.intensity * 2} eps` : 'Idle'}</span>
                                        </TooltipContent>
                                    </Tooltip>
                                </TooltipProvider>
                            );
                        })}
                    </div>
                ))}
            </div>
        </Card>
    );
}
