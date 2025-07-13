import api from './api'
import { queryKeys, CACHE_TIMES } from './queryClient'

// API functions
const fetchHealth = async () => {
  const { data } = await api.get('/health')
  return data
}

const fetchJobsStatus = async () => {
  const { data } = await api.get('/jobs/status')
  return data
}

// Query options
export const healthQueries = {
  health: () => ({
    queryKey: queryKeys.health(),
    queryFn: fetchHealth,
    staleTime: 1 * 60 * 1000, // Consider fresh for 1 minute
    cacheTime: 5 * 60 * 1000, // Keep in cache for 5 minutes
  }),

  jobsStatus: () => ({
    queryKey: queryKeys.jobsStatus(),
    queryFn: fetchJobsStatus,
    staleTime: 5 * 60 * 1000, // Consider fresh for 5 minutes
    cacheTime: CACHE_TIMES.THIRTY_MINUTES, // Keep in cache for 30 minutes
  }),
}

// Legacy service methods for backward compatibility
export const healthService = {
  checkHealth: fetchHealth,
  getJobsStatus: fetchJobsStatus,
}