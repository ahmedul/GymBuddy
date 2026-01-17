import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { socialApi, Friend, Friendship, Group } from '../api';

export const useFriends = () => {
  return useQuery({
    queryKey: ['friends'],
    queryFn: () => socialApi.getFriends(),
  });
};

export const usePendingRequests = () => {
  return useQuery({
    queryKey: ['friends', 'pending'],
    queryFn: () => socialApi.getPendingRequests(),
  });
};

export const useSendFriendRequest = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (addresseeId: string) => socialApi.sendFriendRequest(addresseeId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['friends'] });
    },
  });
};

export const useAcceptFriendRequest = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (friendshipId: string) => socialApi.acceptRequest(friendshipId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['friends'] });
    },
  });
};

export const useGroups = () => {
  return useQuery({
    queryKey: ['groups'],
    queryFn: () => socialApi.getGroups(),
  });
};

export const useCreateGroup = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (data: Omit<Group, 'id' | 'owner_id' | 'created_at'>) => socialApi.createGroup(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['groups'] });
    },
  });
};
