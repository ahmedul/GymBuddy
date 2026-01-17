import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { sessionsApi, Session, SessionDetail, CreateSessionRequest, SessionFeedParams, RSVPStatus } from '../api';

export const useSessionsFeed = (params?: SessionFeedParams) => {
  return useQuery({
    queryKey: ['sessions', 'feed', params],
    queryFn: () => sessionsApi.getFeed(params),
  });
};

export const useSession = (id: string) => {
  return useQuery({
    queryKey: ['sessions', id],
    queryFn: () => sessionsApi.getById(id),
    enabled: !!id,
  });
};

export const useCreateSession = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: CreateSessionRequest) => sessionsApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['sessions'] });
    },
  });
};

export const useJoinSession = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (sessionId: string) => sessionsApi.join(sessionId),
    onSuccess: (_, sessionId) => {
      queryClient.invalidateQueries({ queryKey: ['sessions', sessionId] });
      queryClient.invalidateQueries({ queryKey: ['sessions', 'feed'] });
    },
  });
};

export const useLeaveSession = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (sessionId: string) => sessionsApi.leave(sessionId),
    onSuccess: (_, sessionId) => {
      queryClient.invalidateQueries({ queryKey: ['sessions', sessionId] });
      queryClient.invalidateQueries({ queryKey: ['sessions', 'feed'] });
    },
  });
};

export const useUpdateRSVP = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ sessionId, status }: { sessionId: string; status: RSVPStatus }) => 
      sessionsApi.updateRSVP(sessionId, status),
    onSuccess: (_, { sessionId }) => {
      queryClient.invalidateQueries({ queryKey: ['sessions', sessionId] });
    },
  });
};

export const useCheckIn = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (sessionId: string) => sessionsApi.checkIn(sessionId),
    onSuccess: (_, sessionId) => {
      queryClient.invalidateQueries({ queryKey: ['sessions', sessionId] });
    },
  });
};
