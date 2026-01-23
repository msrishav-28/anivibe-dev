'use client';

import { useEffect, useState } from 'react';
import { cn } from '@/lib/utils';
import { motion } from 'framer-motion';

interface GlitchTextProps {
    text: string;
    className?: string;
    as?: 'h1' | 'h2' | 'h3' | 'h4' | 'span' | 'p' | 'div';
}

const CHARS = '!<>-_\\/[]{}—=+*^?#________';

export function GlitchText({ text, className, as: Component = 'h2' }: GlitchTextProps) {
    const [displayText, setDisplayText] = useState('');

    useEffect(() => {
        let iteration = 0;
        let frameId: number;

        const animate = () => {
            setDisplayText(_prev =>
                text
                    .split('')
                    .map((_letter, index) => {
                        if (index < iteration) {
                            return text[index];
                        }
                        return CHARS[Math.floor(Math.random() * CHARS.length)];
                    })
                    .join('')
            );

            if (iteration < text.length) {
                iteration += 1 / 3; // Slow down the reveal
                frameId = requestAnimationFrame(animate);
            }
        };

        frameId = requestAnimationFrame(animate);

        return () => cancelAnimationFrame(frameId);
    }, [text]);

    const Tag = motion(Component as any);

    return (
        <Tag className={cn("font-heading font-bold tracking-tight uppercase", className)}>
            {displayText}
        </Tag>
    );
}
