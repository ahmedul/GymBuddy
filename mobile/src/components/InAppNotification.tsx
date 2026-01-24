import React, { useEffect, useRef, useState } from 'react';
import {
  Animated,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import * as Notifications from 'expo-notifications';
import { handleNotificationNavigation, NotificationData } from '../navigation/navigationService';

const { width } = Dimensions.get('window');

interface InAppNotificationProps {
  notification: Notifications.Notification | null;
  onDismiss: () => void;
}

export default function InAppNotification({ notification, onDismiss }: InAppNotificationProps) {
  const insets = useSafeAreaInsets();
  const slideAnim = useRef(new Animated.Value(-150)).current;
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (notification) {
      setIsVisible(true);
      // Slide in
      Animated.spring(slideAnim, {
        toValue: 0,
        useNativeDriver: true,
        tension: 50,
        friction: 8,
      }).start();

      // Auto dismiss after 4 seconds
      const timer = setTimeout(() => {
        dismiss();
      }, 4000);

      return () => clearTimeout(timer);
    }
  }, [notification]);

  const dismiss = () => {
    Animated.timing(slideAnim, {
      toValue: -150,
      duration: 200,
      useNativeDriver: true,
    }).start(() => {
      setIsVisible(false);
      onDismiss();
    });
  };

  const handlePress = () => {
    dismiss();
    if (notification) {
      const data = notification.request.content.data as NotificationData;
      handleNotificationNavigation(data);
    }
  };

  if (!isVisible || !notification) {
    return null;
  }

  const { title, body } = notification.request.content;
  const data = notification.request.content.data as NotificationData;
  
  // Get icon based on notification type
  let iconName: keyof typeof Ionicons.glyphMap = 'notifications';
  let iconColor = '#007AFF';
  
  switch (data?.type) {
    case 'session_invite':
    case 'session_reminder':
      iconName = 'fitness';
      iconColor = '#FF6B35';
      break;
    case 'friend_request':
      iconName = 'people';
      iconColor = '#34C759';
      break;
  }

  return (
    <Animated.View
      style={[
        styles.container,
        {
          transform: [{ translateY: slideAnim }],
          top: insets.top + 10,
        },
      ]}
    >
      <TouchableOpacity
        style={styles.content}
        activeOpacity={0.9}
        onPress={handlePress}
      >
        <View style={[styles.iconContainer, { backgroundColor: iconColor + '20' }]}>
          <Ionicons name={iconName} size={24} color={iconColor} />
        </View>
        <View style={styles.textContainer}>
          <Text style={styles.title} numberOfLines={1}>
            {title || 'Notification'}
          </Text>
          <Text style={styles.body} numberOfLines={2}>
            {body}
          </Text>
        </View>
        <TouchableOpacity onPress={dismiss} style={styles.closeButton}>
          <Ionicons name="close" size={20} color="#999" />
        </TouchableOpacity>
      </TouchableOpacity>
    </Animated.View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: 'absolute',
    left: 16,
    right: 16,
    zIndex: 9999,
  },
  content: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 8,
  },
  iconContainer: {
    width: 44,
    height: 44,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  textContainer: {
    flex: 1,
  },
  title: {
    fontSize: 16,
    fontWeight: '600',
    color: '#1a1a1a',
    marginBottom: 2,
  },
  body: {
    fontSize: 14,
    color: '#666',
    lineHeight: 18,
  },
  closeButton: {
    padding: 4,
    marginLeft: 8,
  },
});
