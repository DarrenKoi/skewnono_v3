import api from './api'

// API functions
const fetchCurrentEquipmentStatus = async () => {
  const { data } = await api.get('/equipment-status/current-status')
  return data
}

const fetchNotAvailableEquipment = async () => {
  const { data } = await api.get('/equipment-status/not_available')
  return data
}

const fetchStorageData = async () => {
  const { data } = await api.get('/equipment-status/storage')
  return data
}

// Query options with different cache strategies
export const equipmentQueries = {
  // Current equipment status - real-time data, updates frequently
  currentStatus: () => ({
    queryKey: ['equipment-status', 'current'],
    queryFn: fetchCurrentEquipmentStatus,
    staleTime: 1000 * 60, // 1 minute
    cacheTime: 1000 * 60 * 5, // 5 minutes
    refetchInterval: 1000 * 60, // Auto-refetch every minute
  }),

  // Not available equipment - updates every 5 minutes
  notAvailable: () => ({
    queryKey: ['equipment-status', 'not-available'],
    queryFn: fetchNotAvailableEquipment,
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 10, // 10 minutes
    refetchInterval: 1000 * 60 * 5, // Auto-refetch every 5 minutes
  }),

  // Storage data - updates every 5 minutes
  storage: () => ({
    queryKey: ['equipment-status', 'storage'],
    queryFn: fetchStorageData,
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 10, // 10 minutes
  }),
}