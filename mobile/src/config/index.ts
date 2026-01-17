// API configuration
export const API_URL = __DEV__ 
  ? 'http://localhost:8000/api/v1'
  : 'https://api.gymbuddy.app/api/v1';

export const config = {
  api: {
    baseUrl: API_URL,
    timeout: 10000,
  },
};
