import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { Ionicons } from '@expo/vector-icons';

import FeedScreen from '../screens/main/FeedScreen';
import SessionDetailScreen from '../screens/main/SessionDetailScreen';
import CreateSessionScreen from '../screens/main/CreateSessionScreen';
import FriendsScreen from '../screens/main/FriendsScreen';
import ProfileScreen from '../screens/main/ProfileScreen';
import GymsScreen from '../screens/main/GymsScreen';

export type MainTabParamList = {
  FeedTab: undefined;
  GymsTab: undefined;
  CreateTab: undefined;
  FriendsTab: undefined;
  ProfileTab: undefined;
};

export type MainStackParamList = {
  MainTabs: undefined;
  SessionDetail: { sessionId: string };
  CreateSession: { gymId?: string };
};

const Tab = createBottomTabNavigator<MainTabParamList>();
const Stack = createNativeStackNavigator<MainStackParamList>();

function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap = 'home';

          switch (route.name) {
            case 'FeedTab':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'GymsTab':
              iconName = focused ? 'location' : 'location-outline';
              break;
            case 'CreateTab':
              iconName = focused ? 'add-circle' : 'add-circle-outline';
              break;
            case 'FriendsTab':
              iconName = focused ? 'people' : 'people-outline';
              break;
            case 'ProfileTab':
              iconName = focused ? 'person' : 'person-outline';
              break;
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: 'gray',
        headerShown: true,
      })}
    >
      <Tab.Screen name="FeedTab" component={FeedScreen} options={{ title: 'Feed' }} />
      <Tab.Screen name="GymsTab" component={GymsScreen} options={{ title: 'Gyms' }} />
      <Tab.Screen name="CreateTab" component={CreateSessionScreen} options={{ title: 'Create' }} />
      <Tab.Screen name="FriendsTab" component={FriendsScreen} options={{ title: 'Friends' }} />
      <Tab.Screen name="ProfileTab" component={ProfileScreen} options={{ title: 'Profile' }} />
    </Tab.Navigator>
  );
}

export default function MainNavigator() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="MainTabs" 
        component={MainTabs} 
        options={{ headerShown: false }} 
      />
      <Stack.Screen 
        name="SessionDetail" 
        component={SessionDetailScreen}
        options={{ title: 'Session' }}
      />
      <Stack.Screen 
        name="CreateSession" 
        component={CreateSessionScreen}
        options={{ title: 'New Session' }}
      />
    </Stack.Navigator>
  );
}
