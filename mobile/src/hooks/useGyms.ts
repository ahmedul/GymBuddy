import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { gymsApi, Gym, GymSearchParams } from '../api';

export const useGymsSearch = (params: GymSearchParams) => {
  return useQuery({
    queryKey: ['gyms', 'search', params],
    queryFn: () => gymsApi.search(params),
    enabled: !!(params.q || (params.lat && params.lon)),
  });
};

export const useGym = (id: string) => {
  return useQuery({
    queryKey: ['gyms', id],
    queryFn: () => gymsApi.getById(id),
    enabled: !!id,
  });
};

export const useFavoriteGyms = () => {
  return useQuery({
    queryKey: ['gyms', 'favorites'],
    queryFn: () => gymsApi.getFavorites(),
  });
};

export const useAddFavoriteGym = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (gymId: string) => gymsApi.addFavorite(gymId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['gyms', 'favorites'] });
    },
  });
};

export const useRemoveFavoriteGym = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (gymId: string) => gymsApi.removeFavorite(gymId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['gyms', 'favorites'] });
    },
  });
};
