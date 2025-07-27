import api from './api'

// API functions
const fetchAllDeviceData = async (facId = 'R3') => {
  console.log(`[DeviceStatisticsService] Fetching device data for facility: ${facId}`)
  const { data } = await api.get('/device-statistics/device-data', {
    params: { fac_id: facId }
  })
  
  // Log response data
  console.log('[DeviceStatisticsService] Response data:', data)
  
  return data
}

// Query options with different cache strategies
export const deviceStatisticsQueries = {
  // All device data - fetches everything at once
  allDeviceData: (facId = 'R3') => ({
    queryKey: ['device-statistics', 'all-data', facId],
    queryFn: () => fetchAllDeviceData(facId),
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 15, // 15 minutes
  }),
}