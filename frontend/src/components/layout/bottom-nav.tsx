'use client';

import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { Home, User, Sparkles } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useAuthStore } from '@/store/auth-store';

export function BottomNav() {
    const pathname = usePathname();
    const { isAuthenticated } = useAuthStore();
    const router = useRouter();

    // If we are on a desktop size, we traditionally hide this, 
    // but Neo-Tokyo strategy says "Mobile First". 
    // We will keep it visible on mobile only via CSS media queries.

    const navItems = [
        {
            label: 'Home',
            icon: Home,
            href: '/',
            isActive: pathname === '/',
        },
        {
            // The FAB (Central Vibe Tuner Trigger)
            label: 'Vibe',
            icon: Sparkles,
            href: '/search', // Or open modal
            isFab: true,
            isActive: pathname === '/search',
        },
        {
            label: 'Profile',
            icon: User,
            href: isAuthenticated ? '/profile' : '/login',
            isActive: pathname.startsWith('/profile') || pathname.startsWith('/login'),
        },
    ];

    return (
        <div className="fixed bottom-0 left-0 right-0 z-50 md:hidden">
            {/* 
        Glassmorphic Container
        Background is solid enough to read, transparent enough to feel immersive
      */}
            <div className="mx-4 mb-4 rounded-2xl border border-white/10 bg-black/80 backdrop-blur-xl shadow-2xl">
                <nav className="flex h-16 items-center justify-around px-2">
                    {navItems.map((item) => {
                        if (item.isFab) {
                            return (
                                <div key={item.label} className="relative -top-6">
                                    <motion.button
                                        whileTap={{ scale: 0.9 }}
                                        onClick={() => router.push(item.href)}
                                        className={cn(
                                            "flex h-14 w-14 items-center justify-center rounded-full shadow-[0_0_15px_#8b5cf6] transition-all",
                                            "bg-gradient-to-tr from-primary-600 to-primary-400 border border-white/20",
                                            item.isActive ? "ring-2 ring-white/50" : ""
                                        )}
                                    >
                                        <Sparkles className="h-6 w-6 text-white fill-white/20" />
                                    </motion.button>
                                </div>
                            );
                        }

                        return (
                            <Link
                                key={item.label}
                                href={item.href}
                                className={cn(
                                    "relative flex flex-col items-center justify-center gap-1 p-2 transition-colors",
                                    item.isActive ? "text-primary-400" : "text-muted-foreground hover:text-white"
                                )}
                            >
                                <item.icon className={cn("h-6 w-6", item.isActive && "fill-current")} />
                                <span className="text-[10px] font-medium">{item.label}</span>

                                {item.isActive && (
                                    <motion.div
                                        layoutId="nav-dot"
                                        className="absolute -bottom-1 h-1 w-1 rounded-full bg-primary-400"
                                        transition={{ type: "spring", stiffness: 500, damping: 30 }}
                                    />
                                )}
                            </Link>
                        );
                    })}
                </nav>
            </div>
        </div>
    );
}
