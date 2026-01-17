import api from './client';
import * as SecureStore from 'expo-secure-store';

export interface LoginRequest {
  username: string; // email
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface User {
  id: string;
  email: string;
  name: string;
  photo_url?: string;
  bio?: string;
  training_level: 'beginner' | 'intermediate' | 'advanced';
  visibility: 'public' | 'friends' | 'private';
  is_verified: boolean;
  created_at: string;
}

export const authApi = {
  async login(data: LoginRequest): Promise<AuthResponse> {
    const formData = new URLSearchParams();
    formData.append('username', data.username);
    formData.append('password', data.password);
    
    const response = await api.post<AuthResponse>('/auth/login', formData.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    
    await SecureStore.setItemAsync('accessToken', response.data.access_token);
    return response.data;
  },

  async register(data: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },

  async getMe(): Promise<User> {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  async logout(): Promise<void> {
    await SecureStore.deleteItemAsync('accessToken');
  },
};
