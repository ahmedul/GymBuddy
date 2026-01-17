import api from './client';
import { User } from './auth';

export type FriendshipStatus = 'pending' | 'accepted' | 'declined' | 'blocked';

export interface Friendship {
  id: string;
  requester_id: string;
  addressee_id: string;
  status: FriendshipStatus;
  created_at: string;
}

export interface Friend {
  user: User;
  friendship_id: string;
  since: string;
}

export interface Group {
  id: string;
  name: string;
  description?: string;
  photo_url?: string;
  owner_id: string;
  is_private: boolean;
  max_members: number;
  created_at: string;
}

export const socialApi = {
  // Friends
  async getFriends(): Promise<Friend[]> {
    const response = await api.get<Friend[]>('/friends');
    return response.data;
  },

  async getPendingRequests(): Promise<Friendship[]> {
    const response = await api.get<Friendship[]>('/friends/requests');
    return response.data;
  },

  async sendFriendRequest(addresseeId: string): Promise<Friendship> {
    const response = await api.post<Friendship>('/friends/request', { addressee_id: addresseeId });
    return response.data;
  },

  async acceptRequest(friendshipId: string): Promise<Friendship> {
    const response = await api.post<Friendship>(`/friends/requests/${friendshipId}/accept`);
    return response.data;
  },

  async declineRequest(friendshipId: string): Promise<Friendship> {
    const response = await api.post<Friendship>(`/friends/requests/${friendshipId}/decline`);
    return response.data;
  },

  // Groups
  async getGroups(): Promise<Group[]> {
    const response = await api.get<Group[]>('/groups');
    return response.data;
  },

  async getGroup(id: string): Promise<Group> {
    const response = await api.get<Group>(`/groups/${id}`);
    return response.data;
  },

  async createGroup(data: Omit<Group, 'id' | 'owner_id' | 'created_at'>): Promise<Group> {
    const response = await api.post<Group>('/groups', data);
    return response.data;
  },

  async updateGroup(id: string, data: Partial<Group>): Promise<Group> {
    const response = await api.patch<Group>(`/groups/${id}`, data);
    return response.data;
  },
};
