import * as Notifications from 'expo-notifications';
import * as Device from 'expo-device';
import Constants from 'expo-constants';
import { Platform } from 'react-native';
import { useAuthStore } from '../store/authStore';
import api from '../api/client';

// Configure how notifications appear when app is in foreground
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

export interface PushNotificationState {
  expoPushToken: string | null;
  notification: Notifications.Notification | null;
}

/**
 * Register for push notifications and get the Expo push token
 */
export async function registerForPushNotificationsAsync(): Promise<string | null> {
  let token: string | null = null;

  // Push notifications only work on physical devices
  if (!Device.isDevice) {
    console.log('Push notifications require a physical device');
    return null;
  }

  // Check if we already have permission
  const { status: existingStatus } = await Notifications.getPermissionsAsync();
  let finalStatus = existingStatus;

  // If we don't have permission, ask for it
  if (existingStatus !== 'granted') {
    const { status } = await Notifications.requestPermissionsAsync();
    finalStatus = status;
  }

  // If permission denied, return null
  if (finalStatus !== 'granted') {
    console.log('Push notification permission denied');
    return null;
  }

  // Get the Expo push token
  try {
    const projectId = Constants.expoConfig?.extra?.eas?.projectId;
    
    const pushTokenResponse = await Notifications.getExpoPushTokenAsync({
      projectId: projectId,
    });
    
    token = pushTokenResponse.data;
    console.log('Expo push token:', token);
  } catch (error) {
    console.error('Error getting push token:', error);
    return null;
  }

  // Android needs a notification channel
  if (Platform.OS === 'android') {
    await Notifications.setNotificationChannelAsync('default', {
      name: 'Default',
      importance: Notifications.AndroidImportance.MAX,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF6B35',
    });

    await Notifications.setNotificationChannelAsync('sessions', {
      name: 'Workout Sessions',
      description: 'Notifications about workout sessions and invites',
      importance: Notifications.AndroidImportance.HIGH,
      vibrationPattern: [0, 250, 250, 250],
      lightColor: '#FF6B35',
    });

    await Notifications.setNotificationChannelAsync('social', {
      name: 'Social',
      description: 'Friend requests and social notifications',
      importance: Notifications.AndroidImportance.DEFAULT,
    });
  }

  return token;
}

/**
 * Send the push token to our backend
 */
export async function registerTokenWithBackend(token: string): Promise<void> {
  try {
    await api.post('/notifications/token', {
      token,
      platform: Platform.OS,
    });
    console.log('Push token registered with backend');
  } catch (error) {
    console.error('Failed to register push token with backend:', error);
  }
}

/**
 * Unregister the push token from our backend (call on logout)
 */
export async function unregisterTokenFromBackend(token: string): Promise<void> {
  try {
    await api.delete('/notifications/token', {
      data: { token },
    });
    console.log('Push token unregistered from backend');
  } catch (error) {
    console.error('Failed to unregister push token:', error);
  }
}

/**
 * Schedule a local notification (for testing)
 */
export async function scheduleTestNotification(): Promise<void> {
  await Notifications.scheduleNotificationAsync({
    content: {
      title: "🏋️ GymBuddy",
      body: 'Push notifications are working!',
      data: { type: 'test' },
    },
    trigger: { seconds: 2 },
  });
}

/**
 * Add listener for incoming notifications (when app is open)
 */
export function addNotificationReceivedListener(
  callback: (notification: Notifications.Notification) => void
): Notifications.Subscription {
  return Notifications.addNotificationReceivedListener(callback);
}

/**
 * Add listener for notification responses (when user taps notification)
 */
export function addNotificationResponseReceivedListener(
  callback: (response: Notifications.NotificationResponse) => void
): Notifications.Subscription {
  return Notifications.addNotificationResponseReceivedListener(callback);
}

/**
 * Get the last notification response (for when app was opened via notification)
 */
export async function getLastNotificationResponse(): Promise<Notifications.NotificationResponse | null> {
  return await Notifications.getLastNotificationResponseAsync();
}

/**
 * Clear all notifications
 */
export async function clearAllNotifications(): Promise<void> {
  await Notifications.dismissAllNotificationsAsync();
}

/**
 * Get current badge count
 */
export async function getBadgeCount(): Promise<number> {
  return await Notifications.getBadgeCountAsync();
}

/**
 * Set badge count
 */
export async function setBadgeCount(count: number): Promise<void> {
  await Notifications.setBadgeCountAsync(count);
}
