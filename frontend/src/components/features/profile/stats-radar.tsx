'use client';

import { ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';

const defaultStats = [
    { subject: 'Action', A: 120, fullMark: 150 },
    { subject: 'Romance', A: 98, fullMark: 150 },
    { subject: 'Strategy', A: 86, fullMark: 150 },
    { subject: 'Comedy', A: 99, fullMark: 150 },
    { subject: 'Dark', A: 85, fullMark: 150 },
    { subject: 'SoL', A: 65, fullMark: 150 },
];

export function StatsRadar({ data }: { data?: any }) {
    // Transform data if provided, else use default
    // We expect data to be like { "Action": 10, "Romance": 5 ... }
    const chartData = data ? Object.entries(data).map(([key, value]) => ({
        subject: key,
        A: value as number,
        fullMark: 100 // Normalized
    })).slice(0, 6) : defaultStats;

    return (
        <div className="h-[300px] w-full relative">
            {/* Decorative rings */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="w-[80%] h-[80%] border border-white/5 rounded-full animate-[spin_60s_linear_infinite]" />
                <div className="w-[60%] h-[60%] border border-primary-500/10 rounded-full animate-pulse-slow" />
                <div className="w-[40%] h-[40%] border border-white/5 rounded-full" />
            </div>

            <ResponsiveContainer width="100%" height="100%">
                <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                    <PolarGrid stroke="rgba(255,255,255,0.05)" />
                    <PolarAngleAxis
                        dataKey="subject"
                        tick={{ fill: 'rgba(255,255,255,0.6)', fontSize: 11, fontWeight: 600 }}
                    />
                    <PolarRadiusAxis angle={30} domain={[0, 150]} tick={false} axisLine={false} />
                    <Radar
                        name="Stats"
                        dataKey="A"
                        stroke="var(--primary-500)"
                        strokeWidth={2}
                        fill="var(--primary-500)"
                        fillOpacity={0.3}
                    />
                </RadarChart>
            </ResponsiveContainer>
        </div>
    );
}
