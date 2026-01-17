import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ScrollView,
  Alert,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { Ionicons } from '@expo/vector-icons';
import DateTimePicker from '@react-native-community/datetimepicker';
import { useCreateSession, useFavoriteGyms } from '../../hooks';
import { SessionVisibility } from '../../api';

export default function CreateSessionScreen() {
  const navigation = useNavigation();
  const { data: favoriteGyms } = useFavoriteGyms();
  const createMutation = useCreateSession();

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [selectedGymId, setSelectedGymId] = useState<string>('');
  const [scheduledAt, setScheduledAt] = useState(new Date());
  const [duration, setDuration] = useState('60');
  const [visibility, setVisibility] = useState<SessionVisibility>('friends');
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showTimePicker, setShowTimePicker] = useState(false);

  const handleCreate = async () => {
    if (!title.trim()) {
      Alert.alert('Error', 'Please enter a session title');
      return;
    }

    if (!selectedGymId) {
      Alert.alert('Error', 'Please select a gym location');
      return;
    }

    try {
      await createMutation.mutateAsync({
        title: title.trim(),
        description: description.trim() || undefined,
        gym_id: selectedGymId,
        scheduled_at: scheduledAt.toISOString(),
        duration_minutes: parseInt(duration) || 60,
        visibility,
      });
      Alert.alert('Success', 'Session created!', [
        { text: 'OK', onPress: () => navigation.goBack() },
      ]);
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Could not create session');
    }
  };

  const visibilityOptions: { value: SessionVisibility; label: string; icon: string }[] = [
    { value: 'private', label: 'Private', icon: 'lock-closed' },
    { value: 'friends', label: 'Friends', icon: 'people' },
    { value: 'public', label: 'Public', icon: 'globe' },
  ];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.label}>Session Title *</Text>
      <TextInput
        style={styles.input}
        placeholder="e.g., Morning Leg Day"
        value={title}
        onChangeText={setTitle}
      />

      <Text style={styles.label}>Description</Text>
      <TextInput
        style={[styles.input, styles.textArea]}
        placeholder="What's the plan?"
        value={description}
        onChangeText={setDescription}
        multiline
        numberOfLines={3}
      />

      <Text style={styles.label}>Location *</Text>
      {favoriteGyms && favoriteGyms.length > 0 ? (
        <View style={styles.gymList}>
          {favoriteGyms.map((gym) => (
            <TouchableOpacity
              key={gym.id}
              style={[
                styles.gymOption,
                selectedGymId === gym.id && styles.gymOptionSelected,
              ]}
              onPress={() => setSelectedGymId(gym.id)}
            >
              <Ionicons
                name={selectedGymId === gym.id ? 'location' : 'location-outline'}
                size={20}
                color={selectedGymId === gym.id ? '#007AFF' : '#666'}
              />
              <Text
                style={[
                  styles.gymOptionText,
                  selectedGymId === gym.id && styles.gymOptionTextSelected,
                ]}
              >
                {gym.name}
              </Text>
            </TouchableOpacity>
          ))}
        </View>
      ) : (
        <Text style={styles.hint}>
          Add favorite gyms from the Gyms tab first
        </Text>
      )}

      <Text style={styles.label}>Date & Time *</Text>
      <View style={styles.dateTimeRow}>
        <TouchableOpacity
          style={styles.dateTimeButton}
          onPress={() => setShowDatePicker(true)}
        >
          <Ionicons name="calendar-outline" size={20} color="#007AFF" />
          <Text style={styles.dateTimeText}>
            {scheduledAt.toLocaleDateString()}
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.dateTimeButton}
          onPress={() => setShowTimePicker(true)}
        >
          <Ionicons name="time-outline" size={20} color="#007AFF" />
          <Text style={styles.dateTimeText}>
            {scheduledAt.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </Text>
        </TouchableOpacity>
      </View>

      {showDatePicker && (
        <DateTimePicker
          value={scheduledAt}
          mode="date"
          onChange={(_: unknown, date?: Date) => {
            setShowDatePicker(false);
            if (date) setScheduledAt(date);
          }}
        />
      )}

      {showTimePicker && (
        <DateTimePicker
          value={scheduledAt}
          mode="time"
          onChange={(_: unknown, date?: Date) => {
            setShowTimePicker(false);
            if (date) setScheduledAt(date);
          }}
        />
      )}

      <Text style={styles.label}>Duration (minutes)</Text>
      <TextInput
        style={styles.input}
        placeholder="60"
        value={duration}
        onChangeText={setDuration}
        keyboardType="number-pad"
      />

      <Text style={styles.label}>Who can see this?</Text>
      <View style={styles.visibilityRow}>
        {visibilityOptions.map((option) => (
          <TouchableOpacity
            key={option.value}
            style={[
              styles.visibilityOption,
              visibility === option.value && styles.visibilityOptionSelected,
            ]}
            onPress={() => setVisibility(option.value)}
          >
            <Ionicons
              name={option.icon as any}
              size={20}
              color={visibility === option.value ? '#007AFF' : '#666'}
            />
            <Text
              style={[
                styles.visibilityText,
                visibility === option.value && styles.visibilityTextSelected,
              ]}
            >
              {option.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity
        style={[styles.createButton, createMutation.isPending && styles.createButtonDisabled]}
        onPress={handleCreate}
        disabled={createMutation.isPending}
      >
        <Text style={styles.createButtonText}>
          {createMutation.isPending ? 'Creating...' : 'Create Session'}
        </Text>
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    padding: 16,
    paddingBottom: 32,
  },
  label: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
    marginTop: 16,
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    padding: 14,
    fontSize: 16,
    backgroundColor: '#f9f9f9',
  },
  textArea: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  gymList: {
    gap: 8,
  },
  gymOption: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    gap: 10,
  },
  gymOptionSelected: {
    borderColor: '#007AFF',
    backgroundColor: '#e8f4fd',
  },
  gymOptionText: {
    fontSize: 16,
    color: '#333',
  },
  gymOptionTextSelected: {
    color: '#007AFF',
    fontWeight: '500',
  },
  hint: {
    fontSize: 14,
    color: '#999',
    fontStyle: 'italic',
  },
  dateTimeRow: {
    flexDirection: 'row',
    gap: 12,
  },
  dateTimeButton: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    padding: 14,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    gap: 8,
  },
  dateTimeText: {
    fontSize: 16,
    color: '#333',
  },
  visibilityRow: {
    flexDirection: 'row',
    gap: 8,
  },
  visibilityOption: {
    flex: 1,
    alignItems: 'center',
    padding: 12,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 12,
    gap: 4,
  },
  visibilityOptionSelected: {
    borderColor: '#007AFF',
    backgroundColor: '#e8f4fd',
  },
  visibilityText: {
    fontSize: 12,
    color: '#666',
  },
  visibilityTextSelected: {
    color: '#007AFF',
    fontWeight: '500',
  },
  createButton: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 12,
    alignItems: 'center',
    marginTop: 32,
  },
  createButtonDisabled: {
    opacity: 0.6,
  },
  createButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
  },
});
