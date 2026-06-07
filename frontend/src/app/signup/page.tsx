'use client';

import { SignUp } from '@clerk/nextjs';
import { motion } from 'framer-motion';
import { GlitchText } from '@/components/ui/glitch-text';

export default function SignupPage() {
  return (
    <div className="relative flex min-h-screen items-center justify-center p-4">
      <div className="absolute inset-0 bg-gradient-to-b from-black/50 to-background z-0 pointer-events-none" />
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: 'circOut' }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="mb-8 text-center">
          <GlitchText text="NEW SEQUENCE" as="h1" className="mb-2 text-3xl text-white" />
          <p className="font-mono text-sm uppercase tracking-widest text-primary-400">Construct Identity</p>
        </div>
        <SignUp routing="path" path="/signup" signInUrl="/login" forceRedirectUrl="/" />
      </motion.div>
    </div>
  );
}
