'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw } from 'lucide-react';
import { Button } from '@/components/ui/button';


interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }

      return (
        <div className="flex min-h-screen items-center justify-center p-4 bg-black/90">
          <div className="max-w-lg w-full border border-error/50 rounded-xl bg-black/80 backdrop-blur-xl p-6">
            <div className="flex flex-col space-y-1.5 pb-6">
              <div className="flex items-center gap-3 text-error">
                <AlertTriangle className="h-6 w-6 animate-pulse" />
                <h2 className="text-lg font-bold font-heading text-error">SYSTEM CRITICAL</h2>
              </div>
              <p className="text-error/80 font-mono text-xs uppercase tracking-wider">
                Unrecoverable exception detected. Process terminated.
              </p>
            </div>
            <div className="space-y-6">
              {this.state.error && (
                <div className="rounded-lg bg-black/60 border border-error/30 p-4 font-mono text-xs text-error/90 overflow-auto max-h-48 shadow-inner">
                  <div className="mb-2 opacity-50 border-b border-error/20 pb-1">STACK TRACE:</div>
                  {this.state.error.message}
                </div>
              )}
              <div className="flex gap-3">
                <Button onClick={this.handleReset} variant="spirit" className="flex-1">
                  <RefreshCw className="mr-2 h-4 w-4" />
                  Reboot System
                </Button>
                <Button
                  variant="outline"
                  onClick={() => window.location.href = '/'}
                  className="flex-1 border-white/10 hover:bg-white/5"
                >
                  Return to Base
                </Button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
