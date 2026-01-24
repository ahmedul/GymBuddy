import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Switch,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import api from '../../api/client';

interface NotificationPreferences {
  notify_session_invites: boolean;
  notify_friend_requests: boolean;
  notify_session_reminders: boolean;
}

export default function NotificationSettingsScreen() {
  const insets = useSafeAreaInsets();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [preferences, setPreferences] = useState<NotificationPreferences>({
    notify_session_invites: true,
    notify_friend_requests: true,
    notify_session_reminders: true,
  });

  useEffect(() => {
    fetchPreferences();
  }, []);

  const fetchPreferences = async () => {
    try {
      const response = await api.get('/notifications/preferences');
      setPreferences(response.data);
    } catch (error) {
      console.error('Failed to fetch notification preferences:', error);
      Alert.alert('Error', 'Failed to load notification settings');
    } finally {
      setLoading(false);
    }
  };

  const updatePreference = async (key: keyof NotificationPreferences, value: boolean) => {
    // Optimistic update
    const oldPreferences = { ...preferences };
    setPreferences({ ...preferences, [key]: value });
    setSaving(true);

    try {
      await api.patch('/notifications/preferences', { [key]: value });
    } catch (error) {
      // Revert on error
      setPreferences(oldPreferences);
      console.error('Failed to update preference:', error);
      Alert.alert('Error', 'Failed to update notification setting');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={{ paddingBottom: insets.bottom + 20 }}
    >
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Push Notifications</Text>
        <Text style={styles.sectionDescription}>
          Choose which notifications you'd like to receive
        </Text>

        <View style={styles.settingItem}>
          <View style={styles.settingIcon}>
            <Ionicons name="fitness" size={24} color="#FF6B35" />
          </View>
          <View style={styles.settingContent}>
            <Text style={styles.settingTitle}>Session Invites</Text>
            <Text style={styles.settingDescription}>
              Get notified when someone invites you to a workout
            </Text>
          </View>
          <Switch
            value={preferences.notify_session_invites}
            onValueChange={(value) => updatePreference('notify_session_invites', value)}
            trackColor={{ false: '#e0e0e0', true: '#007AFF80' }}
            thumbColor={preferences.notify_session_invites ? '#007AFF' : '#f4f4f4'}
          />
        </View>

        <View style={styles.divider} />

        <View style={styles.settingItem}>
          <View style={styles.settingIcon}>
            <Ionicons name="people" size={24} color="#34C759" />
          </View>
          <View style={styles.settingContent}>
            <Text style={styles.settingTitle}>Friend Requests</Text>
            <Text style={styles.settingDescription}>
              Get notified when someone wants to be your gym buddy
            </Text>
          </View>
          <Switch
            value={preferences.notify_friend_requests}
            onValueChange={(value) => updatePreference('notify_friend_requests', value)}
            trackColor={{ false: '#e0e0e0', true: '#007AFF80' }}
            thumbColor={preferences.notify_friend_requests ? '#007AFF' : '#f4f4f4'}
          />
        </View>

        <View style={styles.divider} />

        <View style={styles.settingItem}>
          <View style={styles.settingIcon}>
            <Ionicons name="alarm" size={24} color="#5856D6" />
          </View>
          <View style={styles.settingContent}>
            <Text style={styles.settingTitle}>Session Reminders</Text>
            <Text style={styles.settingDescription}>
              Get reminded before your scheduled workouts
            </Text>
          </View>
          <Switch
            value={preferences.notify_session_reminders}
            onValueChange={(value) => updatePreference('notify_session_reminders', value)}
            trackColor={{ false: '#e0e0e0', true: '#007AFF80' }}
            thumbColor={preferences.notify_session_reminders ? '#007AFF' : '#f4f4f4'}
          />
        </View>
      </View>

      <View style={styles.infoSection}>
        <Ionicons name="information-circle-outline" size={20} color="#666" />
        <Text style={styles.infoText}>
          You can also manage notification permissions in your device settings.
        </Text>
      </View>

      {saving && (
        <View style={styles.savingIndicator}>
          <ActivityIndicator size="small" color="#007AFF" />
          <Text style={styles.savingText}>Saving...</Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  section: {
    backgroundColor: '#fff',
    marginTop: 20,
    marginHorizontal: 16,
    borderRadius: 12,
    padding: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 4,
  },
  sectionDescription: {
    fontSize: 14,
    color: '#666',
    marginBottom: 20,
  },
  settingItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
  },
  settingIcon: {
    width: 44,
    height: 44,
    borderRadius: 10,
    backgroundColor: '#f5f5f5',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  settingContent: {
    flex: 1,
    marginRight: 12,
  },
  settingTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#1a1a1a',
    marginBottom: 2,
  },
  settingDescription: {
    fontSize: 13,
    color: '#666',
    lineHeight: 18,
  },
  divider: {
    height: 1,
    backgroundColor: '#e0e0e0',
    marginLeft: 56,
  },
  infoSection: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginHorizontal: 16,
    marginTop: 16,
    paddingHorizontal: 4,
  },
  infoText: {
    flex: 1,
    fontSize: 13,
    color: '#666',
    marginLeft: 8,
    lineHeight: 18,
  },
  savingIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 16,
  },
  savingText: {
    marginLeft: 8,
    fontSize: 14,
    color: '#007AFF',
  },
});
