'use client';

import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { Stars, Sparkles } from '@react-three/drei';
import { motion, AnimatePresence } from 'framer-motion';
import { useHardwareTier } from '@/hooks/use-hardware-tier';
import { GlobalEffects } from './global-effects';

function MeshGradient() {
    return (
        <div
            className="fixed inset-0 z-0 opacity-80 pointer-events-none"
            style={{
                background: 'radial-gradient(at 0% 0%, hsla(253,16%,7%,1) 0, transparent 50%), radial-gradient(at 50% 0%, hsla(225,39%,30%,1) 0, transparent 50%), radial-gradient(at 100% 0%, hsla(339,49%,30%,1) 0, transparent 50%)',
                backgroundSize: '200% 200%',
                animation: 'mesh-pulse 15s ease infinite alternate'
            }}
        >
            <style jsx>{`
        @keyframes mesh-pulse {
          0% { background-position: 0% 50%; opacity: 0.6; }
          50% { background-position: 100% 50%; opacity: 0.8; }
          100% { background-position: 0% 50%; opacity: 0.6; }
        }
      `}</style>
        </div>
    );
}

export function CinematicContainer({ children }: { children: React.ReactNode }) {
    const tier = useHardwareTier();

    return (
        <div className="relative min-h-screen w-full overflow-x-hidden bg-black text-white selection:bg-primary-500/30">
            {/* 
                MANDATORY: Global Atmosphere (Grain + Scanlines)
                Must exist on ALL tiers.
            */}
            <GlobalEffects />

            {/* 
                LAYER 1: The Void (Base)
                Static gradient fallback is always there to prevent Flash of Unstyled Content (FOUC)
            */}
            <div className="fixed inset-0 z-0 bg-black" />

            {/* 
                LAYER 2: The Simulation
                TIER HIGH: Full R3F Particle Simulation
                TIER LOW/MED: Animated Mesh Gradient (Smart Scaling)
            */}
            {tier === 'HIGH' ? (
                <div className="fixed inset-0 z-0 pointer-events-none opacity-100 mix-blend-screen">
                    <Canvas
                        camera={{ position: [0, 0, 1] }}
                        dpr={[1, 1.5]}
                        gl={{
                            antialias: false,
                            powerPreference: "high-performance",
                            preserveDrawingBuffer: false,
                            alpha: true
                        }}
                    >
                        <Suspense fallback={null}>
                            <Stars
                                radius={300}
                                depth={50}
                                count={1500}
                                factor={4}
                                saturation={0}
                                fade
                                speed={0.5}
                            />
                            <Sparkles
                                count={50}
                                scale={10}
                                size={2}
                                speed={0.4}
                                opacity={0.6}
                                color="#8B5CF6" // Spirit Purple
                            />
                            <Sparkles
                                count={30}
                                scale={5}
                                size={1}
                                speed={0.2}
                                opacity={0.4}
                                color="#00F0FF" // Tech Cyan
                            />
                        </Suspense>
                    </Canvas>
                </div>
            ) : (
                <MeshGradient />
            )}

            {/* LAYER 3: Content */}
            <AnimatePresence mode="wait">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.5 }}
                    className="relative z-10"
                >
                    {children}
                </motion.div>
            </AnimatePresence>
        </div>
    );
}
