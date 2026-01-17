import React from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { RouteProp, useRoute } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import { useSession, useJoinSession, useLeaveSession, useCheckIn } from '../../hooks';
import { useAuthStore } from '../../store';
import { MainStackParamList } from '../../navigation/MainNavigator';

type RouteProps = RouteProp<MainStackParamList, 'SessionDetail'>;

export default function SessionDetailScreen() {
  const route = useRoute<RouteProps>();
  const { sessionId } = route.params;
  const { user } = useAuthStore();
  
  const { data: session, isLoading } = useSession(sessionId);
  const joinMutation = useJoinSession();
  const leaveMutation = useLeaveSession();
  const checkInMutation = useCheckIn();

  if (isLoading || !session) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  const isCreator = session.creator.id === user?.id;
  const myParticipation = session.participants.find(p => p.user.id === user?.id);
  const isParticipant = !!myParticipation;

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const handleJoin = async () => {
    try {
      await joinMutation.mutateAsync(sessionId);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Could not join session');
    }
  };

  const handleLeave = async () => {
    Alert.alert('Leave Session', 'Are you sure you want to leave this session?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Leave',
        style: 'destructive',
        onPress: async () => {
          try {
            await leaveMutation.mutateAsync(sessionId);
          } catch (error: any) {
            Alert.alert('Error', 'Could not leave session');
          }
        },
      },
    ]);
  };

  const handleCheckIn = async () => {
    try {
      await checkInMutation.mutateAsync(sessionId);
      Alert.alert('Checked In!', 'You have successfully checked in to this session');
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Could not check in');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>{session.title}</Text>
        <View style={styles.badge}>
          <Text style={styles.badgeText}>{session.visibility}</Text>
        </View>
      </View>

      {session.description && (
        <Text style={styles.description}>{session.description}</Text>
      )}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Details</Text>
        <View style={styles.detailRow}>
          <Ionicons name="location" size={20} color="#007AFF" />
          <View style={styles.detailContent}>
            <Text style={styles.detailLabel}>Location</Text>
            <Text style={styles.detailValue}>{session.gym.name}</Text>
            <Text style={styles.detailSubtext}>{session.gym.address}</Text>
          </View>
        </View>
        <View style={styles.detailRow}>
          <Ionicons name="calendar" size={20} color="#007AFF" />
          <View style={styles.detailContent}>
            <Text style={styles.detailLabel}>When</Text>
            <Text style={styles.detailValue}>{formatDate(session.scheduled_at)}</Text>
          </View>
        </View>
        <View style={styles.detailRow}>
          <Ionicons name="time" size={20} color="#007AFF" />
          <View style={styles.detailContent}>
            <Text style={styles.detailLabel}>Duration</Text>
            <Text style={styles.detailValue}>{session.duration_minutes} minutes</Text>
          </View>
        </View>
      </View>

      {session.exercises.length > 0 && (
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Exercises</Text>
          {session.exercises.map((exercise, index) => (
            <View key={exercise.id} style={styles.exerciseRow}>
              <Text style={styles.exerciseNumber}>{index + 1}</Text>
              <View style={styles.exerciseContent}>
                <Text style={styles.exerciseName}>{exercise.name}</Text>
                {exercise.sets && exercise.reps && (
                  <Text style={styles.exerciseDetails}>
                    {exercise.sets} sets × {exercise.reps} reps
                  </Text>
                )}
                {exercise.notes && (
                  <Text style={styles.exerciseNotes}>{exercise.notes}</Text>
                )}
              </View>
            </View>
          ))}
        </View>
      )}

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>
          Participants ({session.participants.length})
        </Text>
        {session.participants.map((participant) => (
          <View key={participant.id} style={styles.participantRow}>
            <Ionicons name="person-circle" size={36} color="#007AFF" />
            <View style={styles.participantContent}>
              <Text style={styles.participantName}>
                {participant.user.name}
                {participant.user.id === session.creator.id && ' (Host)'}
              </Text>
              <Text style={styles.participantStatus}>
                {participant.rsvp_status}
                {participant.checked_in && ' • ✓ Checked in'}
              </Text>
            </View>
          </View>
        ))}
      </View>

      <View style={styles.actions}>
        {!isParticipant && (
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={handleJoin}
            disabled={joinMutation.isPending}
          >
            <Ionicons name="add" size={20} color="#fff" />
            <Text style={styles.primaryButtonText}>
              {joinMutation.isPending ? 'Joining...' : 'Join Session'}
            </Text>
          </TouchableOpacity>
        )}

        {isParticipant && !myParticipation?.checked_in && (
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={handleCheckIn}
            disabled={checkInMutation.isPending}
          >
            <Ionicons name="checkmark-circle" size={20} color="#fff" />
            <Text style={styles.primaryButtonText}>
              {checkInMutation.isPending ? 'Checking in...' : 'Check In'}
            </Text>
          </TouchableOpacity>
        )}

        {isParticipant && !isCreator && (
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={handleLeave}
            disabled={leaveMutation.isPending}
          >
            <Text style={styles.secondaryButtonText}>Leave Session</Text>
          </TouchableOpacity>
        )}
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    padding: 16,
    paddingTop: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
  },
  badge: {
    backgroundColor: '#e8f4fd',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  badgeText: {
    color: '#007AFF',
    fontSize: 12,
    fontWeight: '600',
  },
  description: {
    fontSize: 16,
    color: '#666',
    paddingHorizontal: 16,
    marginBottom: 16,
  },
  section: {
    padding: 16,
    borderTopWidth: 8,
    borderTopColor: '#f5f5f5',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 16,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 16,
    gap: 12,
  },
  detailContent: {
    flex: 1,
  },
  detailLabel: {
    fontSize: 12,
    color: '#999',
    marginBottom: 2,
  },
  detailValue: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  detailSubtext: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  exerciseRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 12,
    gap: 12,
  },
  exerciseNumber: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#007AFF',
    color: '#fff',
    textAlign: 'center',
    lineHeight: 24,
    fontSize: 12,
    fontWeight: '600',
  },
  exerciseContent: {
    flex: 1,
  },
  exerciseName: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  exerciseDetails: {
    fontSize: 14,
    color: '#666',
    marginTop: 2,
  },
  exerciseNotes: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
    marginTop: 4,
  },
  participantRow: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    gap: 12,
  },
  participantContent: {
    flex: 1,
  },
  participantName: {
    fontSize: 16,
    color: '#333',
    fontWeight: '500',
  },
  participantStatus: {
    fontSize: 14,
    color: '#666',
  },
  actions: {
    padding: 16,
    gap: 12,
    paddingBottom: 32,
  },
  primaryButton: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 12,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 8,
  },
  primaryButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  secondaryButton: {
    borderWidth: 1,
    borderColor: '#ff3b30',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: '#ff3b30',
    fontSize: 16,
    fontWeight: '600',
  },
});
