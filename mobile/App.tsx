import { useEffect, useRef, useState } from 'react';
import { StatusBar } from 'expo-status-bar';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { NavigationContainer } from '@react-navigation/native';
import * as Notifications from 'expo-notifications';
import RootNavigator from './src/navigation/RootNavigator';
import InAppNotification from './src/components/InAppNotification';
import {
  registerForPushNotificationsAsync,
  registerTokenWithBackend,
  addNotificationReceivedListener,
  addNotificationResponseReceivedListener,
  getLastNotificationResponse,
  setBadgeCount,
  getBadgeCount,
} from './src/services/notifications';
import {
  navigationRef,
  processPendingNavigation,
  handleNotificationNavigation,
} from './src/navigation/navigationService';
import { useAuthStore } from './src/store/authStore';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 2,
      staleTime: 5 * 60 * 1000,
    },
  },
});

export default function App() {
  const [expoPushToken, setExpoPushToken] = useState<string | null>(null);
  const [inAppNotification, setInAppNotification] = useState<Notifications.Notification | null>(null);
  const notificationListener = useRef<Notifications.Subscription>();
  const responseListener = useRef<Notifications.Subscription>();
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  useEffect(() => {
    // Register for push notifications
    registerForPushNotificationsAsync().then((token) => {
      if (token) {
        setExpoPushToken(token);
        // Register with backend if user is authenticated
        if (isAuthenticated) {
          registerTokenWithBackend(token);
        }
      }
    });

    // Check if app was opened via a notification
    getLastNotificationResponse().then((response) => {
      if (response) {
        const data = response.notification.request.content.data;
        handleNotificationNavigation(data);
      }
    });

    // Listen for incoming notifications (app in foreground)
    notificationListener.current = addNotificationReceivedListener(
      (notification) => {
        console.log('Notification received:', notification);
        // Show in-app notification banner
        setInAppNotification(notification);
        // Increment badge count
        getBadgeCount().then((count) => setBadgeCount(count + 1));
      }
    );

    // Listen for notification taps
    responseListener.current = addNotificationResponseReceivedListener(
      (response) => {
        console.log('Notification tapped:', response);
        const data = response.notification.request.content.data;
        handleNotificationNavigation(data);
        // Clear badge when user interacts
        setBadgeCount(0);
      }
    );

    return () => {
      if (notificationListener.current) {
        Notifications.removeNotificationSubscription(notificationListener.current);
      }
      if (responseListener.current) {
        Notifications.removeNotificationSubscription(responseListener.current);
      }
    };
  }, [isAuthenticated]);

  // Re-register token when user logs in
  useEffect(() => {
    if (isAuthenticated && expoPushToken) {
      registerTokenWithBackend(expoPushToken);
    }
  }, [isAuthenticated, expoPushToken]);

  // Handle navigation ready
  const onNavigationReady = () => {
    processPendingNavigation();
  };

  return (
    <QueryClientProvider client={queryClient}>
      <SafeAreaProvider>
        <NavigationContainer ref={navigationRef} onReady={onNavigationReady}>
          <RootNavigator />
          <InAppNotification
            notification={inAppNotification}
            onDismiss={() => setInAppNotification(null)}
          />
          <StatusBar style="auto" />
        </NavigationContainer>
      </SafeAreaProvider>
    </QueryClientProvider>
  );
}
