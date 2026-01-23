'use client';

import { useEffect, useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { Stars, Sparkles } from '@react-three/drei';
import { motion, AnimatePresence } from 'framer-motion';

export function CinematicContainer({ children }: { children: React.ReactNode }) {
    const [tier, setTier] = useState<'high' | 'low'>('high');

    useEffect(() => {
        // Simple hardware tier detection
        // If pixel ratio is < 2 (likely desktop or cheap mobile) or hardware concurrency is low, downgrade.
        const pixelRatio = window.devicePixelRatio;
        const cores = navigator.hardwareConcurrency || 4;

        // Logic: High end phones have high pixel ratio (3+) but we want to render roughly at 1.5-2x 
        // for battery saving, but here we strictly check if we should even show particles.
        const isLowEnd = cores <= 4 && pixelRatio < 2;

        setTier(isLowEnd ? 'low' : 'high');
    }, []);

    return (
        <div className="relative min-h-screen w-full overflow-x-hidden bg-black text-white selection:bg-primary-500/30">
            {/* 
        LAYER 1: The Void (Background)
        Static gradient fallback is always there to prevent Flash of Unstyled Content (FOUC)
      */}
            <div className="fixed inset-0 z-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-gray-900 via-black to-black opacity-80" />

            {/* 
        LAYER 2: The Simulation (R3F)
        Only render on high-tier devices to save battery
      */}
            {tier === 'high' && (
                <div className="fixed inset-0 z-0 pointer-events-none opacity-60">
                    <Canvas
                        camera={{ position: [0, 0, 1] }}
                        dpr={[1, 1.5]} // Clamp pixel ratio to save battery on high-res mobile
                        gl={{
                            antialias: false, // Starfields don't really need AA
                            powerPreference: "high-performance",
                            preserveDrawingBuffer: false
                        }}
                    >
                        <Suspense fallback={null}>
                            <Stars
                                radius={300}
                                depth={50}
                                count={1500} // Reduced from 5000 for performance
                                factor={4}
                                saturation={0}
                                fade
                                speed={0.5} // Slowed down for calmer vibe
                            />
                            <Sparkles
                                count={50} // Reduced count
                                scale={10}
                                size={2}
                                speed={0.4}
                                opacity={0.5}
                                color="#8B5CF6" // Spirit Purple
                            />
                            <Sparkles
                                count={30} // Reduced count
                                scale={5}
                                size={1}
                                speed={0.2}
                                opacity={0.3}
                                color="#00F0FF" // Tech Cyan
                            />
                        </Suspense>
                    </Canvas>
                </div>
            )}

            {/* 
        LAYER 3: Film Grain & Scanlines (Global CSS)
        These are applied via globals.css classes
      */}
            <div className="film-grain" />
            <div className="scanlines" />

            {/* LAYER 4: Content */}
            <AnimatePresence mode="wait">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="relative z-10"
                >
                    {children}
                </motion.div>
            </AnimatePresence>
        </div>
    );
}
