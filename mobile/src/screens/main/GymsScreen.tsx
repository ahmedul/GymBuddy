import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  FlatList,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import * as Location from 'expo-location';
import { useGymsSearch, useFavoriteGyms, useAddFavoriteGym, useRemoveFavoriteGym } from '../../hooks';
import { Gym } from '../../api';

function GymCard({ 
  gym, 
  isFavorite, 
  onToggleFavorite 
}: { 
  gym: Gym; 
  isFavorite: boolean;
  onToggleFavorite: () => void;
}) {
  return (
    <View style={styles.card}>
      <View style={styles.cardContent}>
        <Text style={styles.gymName}>{gym.name}</Text>
        <Text style={styles.gymAddress}>{gym.address}</Text>
      </View>
      <TouchableOpacity onPress={onToggleFavorite} style={styles.favoriteButton}>
        <Ionicons
          name={isFavorite ? 'heart' : 'heart-outline'}
          size={24}
          color={isFavorite ? '#ff3b30' : '#ccc'}
        />
      </TouchableOpacity>
    </View>
  );
}

export default function GymsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [location, setLocation] = useState<{ lat: number; lon: number } | null>(null);
  const [activeTab, setActiveTab] = useState<'search' | 'favorites'>('favorites');

  const { data: favoriteGyms, isLoading: loadingFavorites } = useFavoriteGyms();
  const { data: searchResults, isLoading: loadingSearch } = useGymsSearch({
    q: searchQuery || undefined,
    lat: location?.lat,
    lon: location?.lon,
  });

  const addFavorite = useAddFavoriteGym();
  const removeFavorite = useRemoveFavoriteGym();

  const favoriteIds = new Set(favoriteGyms?.map(g => g.id) || []);

  useEffect(() => {
    (async () => {
      const { status } = await Location.requestForegroundPermissionsAsync();
      if (status === 'granted') {
        const loc = await Location.getCurrentPositionAsync({});
        setLocation({
          lat: loc.coords.latitude,
          lon: loc.coords.longitude,
        });
      }
    })();
  }, []);

  const handleToggleFavorite = (gym: Gym) => {
    if (favoriteIds.has(gym.id)) {
      removeFavorite.mutate(gym.id);
    } else {
      addFavorite.mutate(gym.id);
    }
  };

  const gyms = activeTab === 'favorites' ? favoriteGyms : searchResults;
  const isLoading = activeTab === 'favorites' ? loadingFavorites : loadingSearch;

  return (
    <View style={styles.container}>
      <View style={styles.tabs}>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'favorites' && styles.tabActive]}
          onPress={() => setActiveTab('favorites')}
        >
          <Ionicons
            name="heart"
            size={18}
            color={activeTab === 'favorites' ? '#007AFF' : '#666'}
          />
          <Text style={[styles.tabText, activeTab === 'favorites' && styles.tabTextActive]}>
            Favorites
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.tab, activeTab === 'search' && styles.tabActive]}
          onPress={() => setActiveTab('search')}
        >
          <Ionicons
            name="search"
            size={18}
            color={activeTab === 'search' ? '#007AFF' : '#666'}
          />
          <Text style={[styles.tabText, activeTab === 'search' && styles.tabTextActive]}>
            Search
          </Text>
        </TouchableOpacity>
      </View>

      {activeTab === 'search' && (
        <View style={styles.searchContainer}>
          <Ionicons name="search" size={20} color="#999" style={styles.searchIcon} />
          <TextInput
            style={styles.searchInput}
            placeholder="Search gyms..."
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
        </View>
      )}

      {isLoading ? (
        <View style={styles.centered}>
          <ActivityIndicator size="large" color="#007AFF" />
        </View>
      ) : (
        <FlatList
          data={gyms}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            <GymCard
              gym={item}
              isFavorite={favoriteIds.has(item.id)}
              onToggleFavorite={() => handleToggleFavorite(item)}
            />
          )}
          contentContainerStyle={styles.list}
          ListEmptyComponent={
            <View style={styles.empty}>
              <Ionicons name="location-outline" size={64} color="#ccc" />
              <Text style={styles.emptyTitle}>
                {activeTab === 'favorites' ? 'No Favorite Gyms' : 'No Results'}
              </Text>
              <Text style={styles.emptyText}>
                {activeTab === 'favorites'
                  ? 'Search for gyms and add them to your favorites'
                  : 'Try a different search term'}
              </Text>
            </View>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  tabs: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    padding: 8,
    gap: 8,
  },
  tab: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 12,
    borderRadius: 10,
    gap: 6,
    backgroundColor: '#f5f5f5',
  },
  tabActive: {
    backgroundColor: '#e8f4fd',
  },
  tabText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#666',
  },
  tabTextActive: {
    color: '#007AFF',
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    margin: 16,
    marginTop: 8,
    borderRadius: 12,
    paddingHorizontal: 12,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    padding: 14,
    fontSize: 16,
  },
  list: {
    padding: 16,
    paddingTop: 0,
    gap: 12,
  },
  card: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  cardContent: {
    flex: 1,
  },
  gymName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 4,
  },
  gymAddress: {
    fontSize: 14,
    color: '#666',
  },
  favoriteButton: {
    padding: 8,
  },
  empty: {
    alignItems: 'center',
    padding: 48,
  },
  emptyTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginTop: 16,
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
});
