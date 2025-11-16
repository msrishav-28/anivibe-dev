import { create } from 'zustand';

interface Toast {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  description?: string;
  duration?: number;
}

interface Modal {
  id: string;
  component: React.ReactNode;
  props?: Record<string, any>;
}

interface UIState {
  // Theme
  theme: 'light' | 'dark' | 'system';
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  
  // Sidebar
  isSidebarOpen: boolean;
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  
  // Mobile menu
  isMobileMenuOpen: boolean;
  toggleMobileMenu: () => void;
  setMobileMenuOpen: (open: boolean) => void;
  
  // Toasts
  toasts: Toast[];
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
  
  // Modals
  modals: Modal[];
  openModal: (modal: Omit<Modal, 'id'>) => string;
  closeModal: (id: string) => void;
  closeAllModals: () => void;
  
  // Loading states
  globalLoading: boolean;
  setGlobalLoading: (loading: boolean) => void;
  
  // Search bar focus
  isSearchFocused: boolean;
  setSearchFocused: (focused: boolean) => void;
}

export const useUIStore = create<UIState>((set, get) => ({
  // Theme
  theme: 'dark',
  setTheme: (theme) => {
    set({ theme });
    if (typeof window !== 'undefined') {
      localStorage.setItem('theme', theme);
      
      // Apply theme to document
      const root = window.document.documentElement;
      root.classList.remove('light', 'dark');
      
      if (theme === 'system') {
        const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches
          ? 'dark'
          : 'light';
        root.classList.add(systemTheme);
      } else {
        root.classList.add(theme);
      }
    }
  },
  
  // Sidebar
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  setSidebarOpen: (open) => set({ isSidebarOpen: open }),
  
  // Mobile menu
  isMobileMenuOpen: false,
  toggleMobileMenu: () => set((state) => ({ isMobileMenuOpen: !state.isMobileMenuOpen })),
  setMobileMenuOpen: (open) => set({ isMobileMenuOpen: open }),
  
  // Toasts
  toasts: [],
  addToast: (toast) => {
    const id = Math.random().toString(36).substring(2, 9);
    const newToast: Toast = { ...toast, id };
    set((state) => ({ toasts: [...state.toasts, newToast] }));
    
    // Auto-remove after duration
    const duration = toast.duration || 4000;
    setTimeout(() => {
      get().removeToast(id);
    }, duration);
    
    return id;
  },
  removeToast: (id) => {
    set((state) => ({ toasts: state.toasts.filter((toast) => toast.id !== id) }));
  },
  
  // Modals
  modals: [],
  openModal: (modal) => {
    const id = Math.random().toString(36).substring(2, 9);
    const newModal: Modal = { ...modal, id };
    set((state) => ({ modals: [...state.modals, newModal] }));
    return id;
  },
  closeModal: (id) => {
    set((state) => ({ modals: state.modals.filter((modal) => modal.id !== id) }));
  },
  closeAllModals: () => {
    set({ modals: [] });
  },
  
  // Loading states
  globalLoading: false,
  setGlobalLoading: (loading) => set({ globalLoading: loading }),
  
  // Search bar focus
  isSearchFocused: false,
  setSearchFocused: (focused) => set({ isSearchFocused: focused }),
}));

// Initialize theme on mount
if (typeof window !== 'undefined') {
  const savedTheme = localStorage.getItem('theme') as 'light' | 'dark' | 'system' | null;
  if (savedTheme) {
    useUIStore.getState().setTheme(savedTheme);
  }
}
