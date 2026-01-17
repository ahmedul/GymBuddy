import { create } from 'zustand';
import * as SecureStore from 'expo-secure-store';
import { User, authApi } from '../api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, name: string) => Promise<void>;
  logout: () => Promise<void>;
  loadUser: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (email: string, password: string) => {
    await authApi.login({ username: email, password });
    const user = await authApi.getMe();
    set({ user, isAuthenticated: true });
  },

  register: async (email: string, password: string, name: string) => {
    await authApi.register({ email, password, name });
    // Auto login after registration
    await authApi.login({ username: email, password });
    const user = await authApi.getMe();
    set({ user, isAuthenticated: true });
  },

  logout: async () => {
    await authApi.logout();
    set({ user: null, isAuthenticated: false });
  },

  loadUser: async () => {
    try {
      const token = await SecureStore.getItemAsync('accessToken');
      if (token) {
        const user = await authApi.getMe();
        set({ user, isAuthenticated: true, isLoading: false });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      set({ isLoading: false });
    }
  },
}));
