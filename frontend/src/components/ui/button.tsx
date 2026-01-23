import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import { Loader2 } from 'lucide-react';
import { motion } from 'framer-motion';

const buttonVariants = cva(
  'inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        primary:
          'bg-gradient-spirit text-white hover:shadow-glow hover:scale-105 active:scale-95 border border-white/10 uppercase tracking-widest font-bold',
        secondary:
          'bg-secondary text-secondary-foreground hover:bg-secondary/80 hover:shadow-glow-lg font-bold uppercase tracking-wider',
        ghost: 'bg-transparent border border-white/20 text-white hover:bg-white hover:text-black hover:shadow-glow transition-colors duration-300',
        outline:
          'border border-input bg-background hover:bg-accent hover:text-accent-foreground',
        danger: 'bg-error text-white hover:bg-red-600 hover:shadow-[0_0_20px_rgba(239,68,68,0.5)]',
        success: 'bg-success text-white hover:bg-green-600 hover:shadow-neon-green',
        link: 'text-primary underline-offset-4 hover:underline',
        spirit: 'bg-primary-500 text-white hover:bg-primary-600 hover:shadow-glow active:scale-95',
      },
      size: {
        sm: 'h-8 rounded-md px-3 text-xs',
        md: 'h-10 px-6 py-2',
        lg: 'h-12 rounded-md px-8 text-base',
        icon: 'h-10 w-10',
      },
      width: {
        default: '',
        full: 'w-full',
      }
    },
    defaultVariants: {
      variant: 'primary',
      size: 'md',
      width: 'default',
    },
  }
);

export interface ButtonProps
  extends Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, 'onAnimationStart' | 'onDragStart' | 'onDragEnd' | 'onDrag' | 'ref'>,
  VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  loading?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      width,
      asChild = false,
      loading = false,
      leftIcon,
      rightIcon,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const Comp = asChild ? Slot : motion.button;
    // Cast to any to bypass strict motion prop types mismatch with Slot
    const Component = Comp as any;

    return (
      <Component
        className={cn(buttonVariants({ variant, size, width, className }))}
        ref={ref}
        disabled={disabled || loading}
        whileTap={{ scale: 0.95 }}
        {...props}
      >
        {loading ? (
          <>
            <Loader2 className="h-4 w-4 animate-spin" />
            {children}
          </>
        ) : (
          <>
            {leftIcon && <span className="inline-flex">{leftIcon}</span>}
            {children}
            {rightIcon && <span className="inline-flex">{rightIcon}</span>}
          </>
        )}
      </Component>
    );
  }
);
Button.displayName = 'Button';

export { Button, buttonVariants };
