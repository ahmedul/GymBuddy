import api from './client';

export interface Gym {
  id: string;
  name: string;
  address: string;
  latitude: number;
  longitude: number;
  phone?: string;
  website?: string;
  photo_url?: string;
  is_custom: boolean;
  created_at: string;
}

export interface GymSearchParams {
  q?: string;
  lat?: number;
  lon?: number;
  radius?: number;
}

export const gymsApi = {
  async search(params: GymSearchParams): Promise<Gym[]> {
    const response = await api.get<Gym[]>('/gyms', { params });
    return response.data;
  },

  async getById(id: string): Promise<Gym> {
    const response = await api.get<Gym>(`/gyms/${id}`);
    return response.data;
  },

  async getFavorites(): Promise<Gym[]> {
    const response = await api.get<Gym[]>('/gyms/favorites');
    return response.data;
  },

  async addFavorite(gymId: string): Promise<void> {
    await api.post(`/gyms/favorites/${gymId}`);
  },

  async removeFavorite(gymId: string): Promise<void> {
    await api.delete(`/gyms/favorites/${gymId}`);
  },

  async create(data: Omit<Gym, 'id' | 'is_custom' | 'created_at'>): Promise<Gym> {
    const response = await api.post<Gym>('/gyms', data);
    return response.data;
  },
};
