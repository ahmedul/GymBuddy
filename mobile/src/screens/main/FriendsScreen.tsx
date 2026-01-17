import React from 'react';
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useFriends, usePendingRequests, useAcceptFriendRequest } from '../../hooks';

export default function FriendsScreen() {
  const { data: friends, isLoading: loadingFriends } = useFriends();
  const { data: pendingRequests, isLoading: loadingRequests } = usePendingRequests();
  const acceptMutation = useAcceptFriendRequest();

  const handleAccept = async (friendshipId: string) => {
    try {
      await acceptMutation.mutateAsync(friendshipId);
    } catch (error) {
      Alert.alert('Error', 'Could not accept friend request');
    }
  };

  if (loadingFriends || loadingRequests) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {pendingRequests && pendingRequests.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Friend Requests</Text>
          {pendingRequests.map((request) => (
            <View key={request.id} style={styles.requestCard}>
              <View style={styles.requestInfo}>
                <Ionicons name="person-circle" size={40} color="#007AFF" />
                <Text style={styles.requestText}>New friend request</Text>
              </View>
              <View style={styles.requestActions}>
                <TouchableOpacity
                  style={styles.acceptButton}
                  onPress={() => handleAccept(request.id)}
                >
                  <Text style={styles.acceptButtonText}>Accept</Text>
                </TouchableOpacity>
              </View>
            </View>
          ))}
        </View>
      )}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>
          Friends {friends ? `(${friends.length})` : ''}
        </Text>
        
        {friends && friends.length > 0 ? (
          <FlatList
            data={friends}
            keyExtractor={(item) => item.friendship_id}
            renderItem={({ item }) => (
              <View style={styles.friendCard}>
                <Ionicons name="person-circle" size={48} color="#007AFF" />
                <View style={styles.friendInfo}>
                  <Text style={styles.friendName}>{item.user.name}</Text>
                  <Text style={styles.friendLevel}>{item.user.training_level}</Text>
                </View>
                <TouchableOpacity style={styles.inviteButton}>
                  <Ionicons name="calendar-outline" size={20} color="#007AFF" />
                </TouchableOpacity>
              </View>
            )}
            contentContainerStyle={styles.list}
          />
        ) : (
          <View style={styles.empty}>
            <Ionicons name="people-outline" size={64} color="#ccc" />
            <Text style={styles.emptyTitle}>No Friends Yet</Text>
            <Text style={styles.emptyText}>
              Invite friends to join GymBuddy and start working out together
            </Text>
          </View>
        )}
      </View>
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
  section: {
    backgroundColor: '#fff',
    marginTop: 8,
    paddingVertical: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    paddingHorizontal: 16,
    marginBottom: 12,
  },
  list: {
    paddingHorizontal: 16,
    gap: 8,
  },
  requestCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
    backgroundColor: '#fffbeb',
    marginHorizontal: 16,
    borderRadius: 12,
    marginBottom: 8,
  },
  requestInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 12,
  },
  requestText: {
    fontSize: 14,
    color: '#333',
  },
  requestActions: {
    flexDirection: 'row',
    gap: 8,
  },
  acceptButton: {
    backgroundColor: '#007AFF',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 8,
  },
  acceptButtonText: {
    color: '#fff',
    fontWeight: '600',
    fontSize: 14,
  },
  friendCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 12,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#eee',
    gap: 12,
  },
  friendInfo: {
    flex: 1,
  },
  friendName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
  },
  friendLevel: {
    fontSize: 14,
    color: '#666',
    textTransform: 'capitalize',
  },
  inviteButton: {
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
    paddingHorizontal: 32,
  },
});
