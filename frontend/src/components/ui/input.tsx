import * as React from 'react';
import { cn } from '@/lib/utils';
import { X } from 'lucide-react';

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  onClear?: () => void;
  containerClassName?: string;
  variant?: 'default' | 'vibe-tuner';
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      type,
      label,
      error,
      leftIcon,
      rightIcon,
      onClear,
      containerClassName,
      value,
      variant = 'default',
      ...props
    },
    ref
  ) => {
    const hasValue = value !== undefined && value !== '';

    return (
      <div className={cn('w-full', containerClassName)}>
        {label && (
          <label className="mb-2 block text-xs font-bold text-muted-foreground uppercase tracking-wider pl-1">
            {label}
          </label>
        )}
        <div className="relative group">
          {leftIcon && (
            <div className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground group-focus-within:text-primary-400 transition-colors">
              {leftIcon}
            </div>
          )}
          <input
            type={type}
            className={cn(
              'flex h-11 w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-primary-500 focus-visible:border-primary-500/50 disabled:cursor-not-allowed disabled:opacity-50 transition-all duration-300',
              variant === 'vibe-tuner' && 'h-14 rounded-full bg-black/60 backdrop-blur-md shadow-lg border-white/20 px-6 text-lg focus-visible:shadow-[0_0_25px_rgba(139,92,246,0.3)]',
              leftIcon && 'pl-11',
              (rightIcon || (onClear && hasValue)) && 'pr-11',
              error && 'border-error ring-error focus-visible:ring-error',
              className
            )}
            ref={ref}
            value={value}
            {...props}
          />

          {/* Vibe Tuner Pulse Effect */}
          {variant === 'vibe-tuner' && (
            <div className="absolute right-0 top-1/2 -translate-y-1/2 h-8 w-[2px] bg-primary/20 mr-14 pointer-events-none opacity-0 group-focus-within:opacity-100 transition-opacity" />
          )}

          {rightIcon && !onClear && (
            <div className="pointer-events-none absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground">
              {rightIcon}
            </div>
          )}
          {onClear && hasValue && (
            <button
              type="button"
              onClick={onClear}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              tabIndex={-1}
            >
              <X className="h-4 w-4" />
            </button>
          )}
        </div>
        {error && <p className="mt-1 text-sm text-error">{error}</p>}
      </div>
    );
  }
);
Input.displayName = 'Input';

export { Input };
