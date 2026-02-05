export const environment = {
  production: true,
  apiUrl: '', // Sera la même URL que le frontend (servi par FastAPI)
  apiPrefix: '/api',
  
  // WebSocket configuration
  wsUrl: '', // Sera déterminé dynamiquement depuis window.location
  wsReconnectInterval: 5000,
  wsMaxReconnectAttempts: 10,
  
  // Feature flags
  features: {
    enableWebSocket: true,
    enableOfflineMode: true,
    enableAnalytics: true,
    enableErrorReporting: true,
    enableAdvancedGeo: true,
    enableMutationTracking: true,
    enableComplianceChecks: true,
    enableZoneManagement: true,
  },
  
  // Logging (désactivé en production sauf erreurs)
  logging: {
    enabled: true,
    level: 'error', // Uniquement les erreurs en prod
  },
  
  // Error reporting (à configurer avec votre service)
  errorReporting: {
    enabled: true,
    dsn: '', // TODO: Configurer avec Sentry DSN
  },
  
  // Analytics (à configurer avec votre service)
  analytics: {
    enabled: true,
    trackingId: '', // TODO: Configurer avec GA4 Tracking ID
  },
  
  // Cache configuration
  cache: {
    enableServiceWorker: true,
    cacheExpiration: 86400000, // 24 heures en ms
  },

  // Push notifications (VAPID key)
  // For production, generate a real key with: npx web-push generate-vapid-keys
  vapidPublicKey: '-noVJd9QVpjDJaWpQWiR_CSVnH1dWqlPZ-T4S6A25q4=',
  
  // API configuration
  api: {
    timeout: 60000, // 60 secondes (plus long en prod)
    retryAttempts: 3,
    retryDelay: 2000,
  },
  
  // Upload configuration
  upload: {
    maxFileSize: 50, // MB (plus grand en prod)
    allowedTypes: ['image/*', 'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
    chunkSize: 2 * 1024 * 1024, // 2 MB
  },
};
