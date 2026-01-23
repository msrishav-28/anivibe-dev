import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { GlitchText } from '@/components/ui/glitch-text';

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-4 bg-black/90">
      <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-20 pointer-events-none" />
      <Card variant="holo" className="max-w-md w-full border-primary-500/30 text-center p-8 bg-black/80 backdrop-blur-xl">
        <div className="space-y-6">
          <div className="relative">
            <GlitchText
              text="404"
              as="h1"
              className="text-8xl font-black font-heading tracking-tighter text-transparent bg-clip-text bg-gradient-to-b from-white to-white/50 drop-shadow-[0_0_15px_rgba(255,255,255,0.5)]"
            />
            <div className="absolute -inset-1 bg-primary-500/20 blur-3xl rounded-full opacity-20 animate-pulse" />
          </div>

          <div className="space-y-2">
            <h2 className="text-xl font-bold uppercase tracking-widest text-primary-400">
              Signal Lost
            </h2>
            <p className="text-sm text-muted-foreground font-mono">
              The neural link you are trying to access has been severed or does not exist in this timeline.
            </p>
          </div>

          <div className="pt-4">
            <Button asChild variant="spirit" className="w-full">
              <Link href="/">
                Re-establish Connection
              </Link>
            </Button>
          </div>
        </div>
      </Card>
      <div className="mt-8 text-xs font-mono text-white/20">
        ERROR_CODE: PAGE_NOT_FOUND_EXCEPTION
      </div>
    </div>
  );
}
