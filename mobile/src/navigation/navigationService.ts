import { createNavigationContainerRef, CommonActions } from '@react-navigation/native';

// Create a navigation ref that can be used outside of React components
export const navigationRef = createNavigationContainerRef();

/**
 * Navigate to a screen from anywhere in the app
 */
export function navigate(name: string, params?: Record<string, unknown>) {
  if (navigationRef.isReady()) {
    navigationRef.dispatch(
      CommonActions.navigate({
        name,
        params,
      })
    );
  } else {
    // Navigation not ready, queue the navigation
    console.log('Navigation not ready, queuing:', name, params);
    pendingNavigation = { name, params };
  }
}

let pendingNavigation: { name: string; params?: Record<string, unknown> } | null = null;

/**
 * Process any pending navigation after navigator is ready
 */
export function processPendingNavigation() {
  if (pendingNavigation && navigationRef.isReady()) {
    navigate(pendingNavigation.name, pendingNavigation.params);
    pendingNavigation = null;
  }
}

/**
 * Navigate to session detail screen
 */
export function navigateToSession(sessionId: string) {
  navigate('SessionDetail', { sessionId });
}

/**
 * Navigate to friends tab
 */
export function navigateToFriends() {
  if (navigationRef.isReady()) {
    navigationRef.dispatch(
      CommonActions.reset({
        index: 0,
        routes: [
          {
            name: 'Main',
            state: {
              routes: [
                {
                  name: 'MainTabs',
                  state: {
                    routes: [{ name: 'FriendsTab' }],
                    index: 3, // FriendsTab index
                  },
                },
              ],
            },
          },
        ],
      })
    );
  }
}

/**
 * Navigate to feed/home
 */
export function navigateToFeed() {
  if (navigationRef.isReady()) {
    navigationRef.dispatch(
      CommonActions.reset({
        index: 0,
        routes: [
          {
            name: 'Main',
            state: {
              routes: [
                {
                  name: 'MainTabs',
                  state: {
                    routes: [{ name: 'FeedTab' }],
                    index: 0,
                  },
                },
              ],
            },
          },
        ],
      })
    );
  }
}

export type NotificationData = {
  type: 'session_invite' | 'friend_request' | 'session_reminder' | 'test';
  session_id?: string;
  sessionId?: string;
  friendship_id?: string;
  friendshipId?: string;
};

/**
 * Handle navigation based on notification data
 */
export function handleNotificationNavigation(data: NotificationData | Record<string, unknown>) {
  const type = data?.type as string;

  switch (type) {
    case 'session_invite':
    case 'session_reminder':
      const sessionId = (data.session_id || data.sessionId) as string;
      if (sessionId) {
        navigateToSession(sessionId);
      }
      break;
    case 'friend_request':
      navigateToFriends();
      break;
    default:
      console.log('Unknown notification type:', type);
      break;
  }
}
