import { QueryClient } from '@tanstack/vue-query'

// Cache time constants matching server refresh periods
export const CACHE_TIMES = {
  THIRTY_MINUTES: 30 * 60 * 1000, // 30 minutes
  FOUR_HOURS: 4 * 60 * 60 * 1000, // 4 hours
  EIGHT_HOURS: 8 * 60 * 60 * 1000, // 8 hours
  TWENTY_FOUR_HOURS: 24 * 60 * 60 * 1000, // 24 hours
}

// Create a query client with default options
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Data is considered fresh for 5 minutes by default
      staleTime: 5 * 60 * 1000,
      // Cache data for 30 minutes by default
      cacheTime: CACHE_TIMES.THIRTY_MINUTES,
      // Retry failed requests 3 times
      retry: 3,
      // Retry delay doubles each time: 1s, 2s, 4s
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      // Don't refetch on window focus by default
      refetchOnWindowFocus: false,
      // Don't refetch on reconnect by default
      refetchOnReconnect: 'always',
    },
  },
})

// Query key factory for consistent key generation
export const queryKeys = {
  all: ['api'],
  health: () => [...queryKeys.all, 'health'],
  jobs: () => [...queryKeys.all, 'jobs'],
  jobsStatus: () => [...queryKeys.jobs(), 'status'],
  users: () => [...queryKeys.all, 'users'],
  user: (id) => [...queryKeys.users(), id],
  equipment: () => [...queryKeys.all, 'equipment'],
  equipmentStatus: () => [...queryKeys.equipment(), 'status'],
  recipes: () => [...queryKeys.all, 'recipes'],
  recipe: (id) => [...queryKeys.recipes(), id],
  deviceStats: () => [...queryKeys.all, 'device-stats'],
  failIssues: () => [...queryKeys.all, 'fail-issues'],
}
