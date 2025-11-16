import { create } from 'zustand';
import { persist } from 'zustand/middleware';
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

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const { user, access_token } = await api.login(email, password);
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: any) {
          set({
            error: error.message || 'Login failed',
            isLoading: false,
          });
          throw error;
        }
      },

      signup: async (username: string, email: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
          const user = await api.signup(username, email, password);
          // After signup, need to login
          await get().login(email, password);
        } catch (error: any) {
          set({
            error: error.message || 'Signup failed',
            isLoading: false,
          });
          throw error;
        }
      },

      logout: async () => {
        set({ isLoading: true });
        try {
          await api.logout();
          set({ user: null, isAuthenticated: false, isLoading: false });
        } catch (error: any) {
          set({ isLoading: false });
          // Still clear user data even if API call fails
          set({ user: null, isAuthenticated: false });
        }
      },

      fetchCurrentUser: async () => {
        set({ isLoading: true });
        try {
          const user = await api.getCurrentUser();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: any) {
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: error.message || 'Failed to fetch user',
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
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
