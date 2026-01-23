'use client';

import { Toast } from '@/components/ui/toast';
import { useToast } from '@/hooks/use-toast';

export function Toaster() {
  const { toasts } = useToast();

  return (
    <div className="fixed bottom-0 right-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px]">
      {toasts.map((t) => {
        const { id, title, description, ...props } = t as any;
        return (
          <Toast
            key={id}
            title={title || ''}
            description={description || ''}
            variant={props.type || 'default'}
            {...props}
          />
        );
      })}
    </div>
  );
}
