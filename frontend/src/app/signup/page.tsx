'use client';

import { useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { GlitchText } from '@/components/ui/glitch-text';
import { useAuthStore } from '@/store/auth-store';

export default function SignupPage() {
  const { signup, isLoading } = useAuthStore();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await signup(username, email, password);
  };

  return (
    <div className="relative flex min-h-screen items-center justify-center p-4">
      {/* Background Glow */}
      <div className="absolute inset-0 bg-gradient-to-b from-black/50 to-background z-0 pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "outCirc" }}
        className="w-full max-w-md relative z-10"
      >
        <div className="backdrop-blur-xl bg-black/40 border border-white/10 p-8 rounded-3xl shadow-2xl">
          <div className="text-center mb-8">
            <GlitchText text="NEW SEQUENCE" as="h1" className="text-3xl mb-2 text-white" />
            <p className="text-primary-400 text-sm tracking-widest uppercase font-mono">
              Construct Identity
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-4">
              <div className="space-y-2">
                <label className="text-xs font-bold text-muted-foreground uppercase tracking-wider ml-1">Username</label>
                <Input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  className="bg-black/50 border-white/10 text-white focus:border-primary-500/50 h-12 rounded-xl"
                  placeholder="NeoUser"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-muted-foreground uppercase tracking-wider ml-1">Email</label>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="bg-black/50 border-white/10 text-white focus:border-primary-500/50 h-12 rounded-xl"
                  placeholder="agent@anivibe.net"
                />
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-muted-foreground uppercase tracking-wider ml-1">Password</label>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="bg-black/50 border-white/10 text-white focus:border-primary-500/50 h-12 rounded-xl"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <Button
              type="submit"
              className="w-full h-12 text-lg font-bold bg-primary-600 hover:bg-primary-500 text-white shadow-glow transition-all"
              loading={isLoading}
            >
              ESTABLISH LINK
            </Button>

            <div className="text-center pt-4">
              <Link href="/login" className="text-sm text-muted-foreground hover:text-white transition-colors">
                Already have access? <span className="text-primary-400 hover:text-primary-300 ml-1">Login</span>
              </Link>
            </div>
          </form>
        </div>
      </motion.div>
    </div>
  );
}
