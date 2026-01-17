import api from './client';
import { User } from './auth';
import { Gym } from './gyms';

export type SessionVisibility = 'private' | 'friends' | 'group' | 'public';
export type RSVPStatus = 'going' | 'maybe' | 'not_going';

export interface Exercise {
  id: string;
  name: string;
  sets?: number;
  reps?: string;
  duration_seconds?: number;
  notes?: string;
  order: number;
}

export interface SessionParticipant {
  id: string;
  user: User;
  rsvp_status: RSVPStatus;
  checked_in: boolean;
  checked_in_at?: string;
}

export interface Session {
  id: string;
  title: string;
  description?: string;
  gym: Gym;
  scheduled_at: string;
  duration_minutes: number;
  visibility: SessionVisibility;
  max_participants?: number;
  creator: User;
  is_recurring: boolean;
  is_cancelled: boolean;
  participant_count: number;
  created_at: string;
}

export interface SessionDetail extends Session {
  participants: SessionParticipant[];
  exercises: Exercise[];
  group_id?: string;
}

export interface CreateSessionRequest {
  title: string;
  description?: string;
  gym_id: string;
  scheduled_at: string;
  duration_minutes: number;
  visibility: SessionVisibility;
  max_participants?: number;
  exercises?: Omit<Exercise, 'id'>[];
}

export interface SessionFeedParams {
  from_date?: string;
  to_date?: string;
  include_public?: boolean;
}

export const sessionsApi = {
  async getFeed(params?: SessionFeedParams): Promise<Session[]> {
    const response = await api.get<Session[]>('/sessions', { params });
    return response.data;
  },

  async getById(id: string): Promise<SessionDetail> {
    const response = await api.get<SessionDetail>(`/sessions/${id}`);
    return response.data;
  },

  async create(data: CreateSessionRequest): Promise<SessionDetail> {
    const response = await api.post<SessionDetail>('/sessions', data);
    return response.data;
  },

  async update(id: string, data: Partial<CreateSessionRequest>): Promise<SessionDetail> {
    const response = await api.patch<SessionDetail>(`/sessions/${id}`, data);
    return response.data;
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/sessions/${id}`);
  },

  async join(id: string): Promise<void> {
    await api.post(`/sessions/${id}/join`);
  },

  async leave(id: string): Promise<void> {
    await api.post(`/sessions/${id}/leave`);
  },

  async updateRSVP(id: string, status: RSVPStatus): Promise<void> {
    await api.post(`/sessions/${id}/rsvp`, { status });
  },

  async checkIn(id: string): Promise<{ checked_in: boolean; checked_in_at: string }> {
    const response = await api.post(`/sessions/${id}/check-in`);
    return response.data;
  },

  async addExercise(sessionId: string, exercise: Omit<Exercise, 'id'>): Promise<Exercise> {
    const response = await api.post<Exercise>(`/sessions/${sessionId}/exercises`, exercise);
    return response.data;
  },

  async invite(sessionId: string, userIds: string[], message?: string): Promise<void> {
    await api.post(`/sessions/${sessionId}/invite`, { user_ids: userIds, message });
  },
};
