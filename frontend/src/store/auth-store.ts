import { create } from 'zustand';
// import { persist } from 'zustand/middleware'; // Removed
import type { User } from '@/types';
import { api } from '@/lib/api-client';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  login: (email: string, password: string) => Promise<void>;
  signup: (username: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  fetchCurrentUser: () => Promise<void>;
  updateUser: (userData: Partial<User>) => void;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true, // Start loading to check session
  error: null,

  login: async (email: string, password: string) => {
    void email;
    void password;
    set({ isLoading: true, error: null });
    set({ error: 'Login is handled by Clerk', isLoading: false });
    throw new Error('Login is handled by Clerk');
  },

  signup: async (username: string, email: string, password: string) => {
    void username;
    void email;
    void password;
    set({ isLoading: true, error: null });
    set({ error: 'Signup is handled by Clerk', isLoading: false });
    throw new Error('Signup is handled by Clerk');
  },

  logout: async () => {
    set({ isLoading: true });
    try {
      await api.logout();
      set({ user: null, isAuthenticated: false, isLoading: false });
    } catch (error: any) {
      set({ isLoading: false, user: null, isAuthenticated: false });
    }
  },

  fetchCurrentUser: async () => {
    set({ isLoading: true });
    try {
      const user = await api.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error: any) {
      // 401 Error is expected if not logged in
      set({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null, // Don't show error for initial check
      });
    }
  },

  updateUser: (userData: Partial<User>) => {
    const currentUser = get().user;
    if (currentUser) {
      set({ user: { ...currentUser, ...userData } });
    }
  },

  clearError: () => {
    set({ error: null });
  },
}));
