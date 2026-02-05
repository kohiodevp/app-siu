export const environment = {
  production: false,
  apiUrl: 'https://flashcroquisapi-tkdm.onrender.com',
  apiPrefix: '/api',
  
  // WebSocket configuration
  wsUrl: 'wss://flashcroquisapi-tkdm.onrender.com/ws',
  wsReconnectInterval: 5000,
  wsMaxReconnectAttempts: 5,

  // Feature flags
  features: {
    enableWebSocket: true,
    enableOfflineMode: true,
    enableAnalytics: true,
    enableErrorReporting: false,
    enableAdvancedGeo: true,
    enableMutationTracking: true,
    enableComplianceChecks: true,
    enableZoneManagement: true,
  },

  // Logging
  logging: {
    enabled: true,
    level: 'debug', // debug, info, warn, error
  },

  // Error reporting (Sentry, Rollbar, etc.)
  errorReporting: {
    enabled: false,
    dsn: '', // To be configured if enabled
  },

  // Analytics (Google Analytics, Mixpanel, etc.)
  analytics: {
    enabled: false,
    trackingId: '', // To be configured if enabled
  },

  // Cache configuration
  cache: {
    enableServiceWorker: true,  // ✅ Activé pour PWA
    cacheExpiration: 3600000, // 1 hour in ms
  },

  // Push notifications (VAPID key)
  // Note: Cette clé est utilisée pour les notifications push Web
  // Pour la production, générer une vraie clé avec: npx web-push generate-vapid-keys
  vapidPublicKey: '-noVJd9QVpjDJaWpQWiR_CSVnH1dWqlPZ-T4S6A25q4=',

  // API configuration
  api: {
    timeout: 30000, // 30 seconds
    retryAttempts: 3,
    retryDelay: 1000,
  },

  // Upload configuration
  upload: {
    maxFileSize: 10, // MB
    allowedTypes: ['image/*', 'application/pdf', 'application/msword'],
    chunkSize: 1024 * 1024, // 1 MB
  },

  // Map configuration
  map: {
    defaultCenter: [12.3714, -1.5197], // Center of Burkina Faso
    defaultZoom: 13,
    maxZoom: 18,
    minZoom: 3,
    tileLayer: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    maxFeaturesForClustering: 1000, // Maximum number of features before clustering activation
    clustering: {
      maxClusterRadius: 100,
      disableClusteringAtZoom: 18,
      chunkedLoading: true
    }
  },

  // Notification configuration
  notification: {
    defaultDuration: 5000, // Default notification duration in ms
    maxNotifications: 10, // Maximum number of notifications displayed
    position: 'bottom-right' // Notification position
  },

  // Analytics configuration
  analyticsConfig: {
    enableRealTimeUpdates: true,
    refreshInterval: 30000, // Data refresh interval in ms
    maxDataPoints: 1000, // Maximum number of data points to keep
    enablePerformanceTracking: true
  },

  // Workflow configuration
  workflow: {
    enableRealTimeNotifications: true,
    enableEmailNotifications: false,
    enableSmsNotifications: false,
    maxWorkflowSteps: 20, // Maximum number of steps in a workflow
    enableParallelProcessing: true,
    enableConditionalLogic: true
  },

  // Search configuration
  search: {
    enableGeocoding: true,
    enableReverseGeocoding: true,
    enableFuzzySearch: true,
    maxSearchResults: 100,
    searchDebounceTime: 300, // Debounce time for search in ms
    enableAdvancedFilters: true
  },

  // Export configuration
  export: {
    enablePdfExport: true,
    enableExcelExport: true,
    enableCsvExport: true,
    enableJsonExport: true,
    enableShapefileExport: true,
    enableGeoJsonExport: true,
    maxExportRecords: 10000 // Maximum number of records that can be exported
  },

  // Security configuration
  security: {
    enableAuditLogging: true,
    enableAccessControl: true,
    enableDataEncryption: false, // Enabled if data encryption is required
    enableTwoFactorAuth: false,
    sessionTimeout: 3600000 // Session timeout in ms (1 hour)
  }
};