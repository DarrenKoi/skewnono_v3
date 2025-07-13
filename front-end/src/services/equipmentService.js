import api from './api'
import { queryKeys, CACHE_TIMES } from './queryClient'

// API functions
const fetchEquipmentList = async () => {
  const { data } = await api.get('/equipment')
  return data
}

const fetchEquipmentStatus = async () => {
  const { data } = await api.get('/equipment/status')
  return data
}

const fetchCurrentEquipmentStatus = async () => {
  const { data } = await api.get('/equipment-status/current-status')
  return data
}

const fetchEquipmentDetails = async (equipmentId) => {
  const { data } = await api.get(`/equipment/${equipmentId}`)
  return data
}

// Query options with different cache strategies
export const equipmentQueries = {
  // Equipment list - updates every 4 hours
  list: () => ({
    queryKey: queryKeys.equipment(),
    queryFn: fetchEquipmentList,
    staleTime: CACHE_TIMES.FOUR_HOURS,
    cacheTime: CACHE_TIMES.EIGHT_HOURS,
  }),

  // Equipment status - updates every 30 minutes
  status: () => ({
    queryKey: queryKeys.equipmentStatus(),
    queryFn: fetchEquipmentStatus,
    staleTime: CACHE_TIMES.THIRTY_MINUTES,
    cacheTime: CACHE_TIMES.FOUR_HOURS,
    refetchInterval: CACHE_TIMES.THIRTY_MINUTES, // Auto-refetch every 30 minutes
  }),

  // Equipment details - updates every 8 hours
  details: (equipmentId) => ({
    queryKey: [...queryKeys.equipment(), 'details', equipmentId],
    queryFn: () => fetchEquipmentDetails(equipmentId),
    staleTime: CACHE_TIMES.EIGHT_HOURS,
    cacheTime: CACHE_TIMES.TWENTY_FOUR_HOURS,
    enabled: !!equipmentId, // Only fetch if equipmentId is provided
  }),

  // Current equipment status - real-time data, updates frequently
  currentStatus: () => ({
    queryKey: [...queryKeys.equipment(), 'current-status'],
    queryFn: fetchCurrentEquipmentStatus,
    staleTime: 1000 * 60, // 1 minute
    cacheTime: 1000 * 60 * 5, // 5 minutes
    refetchInterval: 1000 * 60, // Auto-refetch every minute
  }),
}

// Mutations for updating equipment
export const equipmentMutations = {
  updateStatus: () => ({
    mutationFn: async ({ equipmentId, status }) => {
      const { data } = await api.put(`/equipment/${equipmentId}/status`, { status })
      return data
    },
    onSuccess: (data, variables, context) => {
      // Invalidate related queries after successful update
      queryClient.invalidateQueries({ queryKey: queryKeys.equipmentStatus() })
      queryClient.invalidateQueries({ queryKey: [...queryKeys.equipment(), 'details', variables.equipmentId] })
    },
  }),
}