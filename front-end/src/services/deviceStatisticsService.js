import api from './api'

// API functions
const fetchAllDeviceData = async () => {
  console.log('[DeviceStatisticsService] Fetching all device data...')
  const { data } = await api.get('/device-statistics/device-data')
  
  // Log data structure for debugging
  console.log('[DeviceStatisticsService] Response data structure:', {
    hasWorkingDevices: !!data.working_devices,
    workingDevicesCount: data.working_devices ? Object.keys(data.working_devices).length : 0,
    hasDeviceOptions: !!data.device_options,
    deviceCategories: data.device_options?.devices?.map(d => d.category),
    dateKeys: Object.keys(data).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/)),
    totalKeys: Object.keys(data).length
  })
  
  // Log sample date data
  const dateKeys = Object.keys(data).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/))
  if (dateKeys.length > 0) {
    const firstDate = dateKeys[0]
    console.log(`[DeviceStatisticsService] Sample data for ${firstDate}:`, {
      hasAllRcpInfo: !!data[firstDate].all_rcp_info,
      allRcpInfoCount: data[firstDate].all_rcp_info?.length,
      hasAllRecipeList: !!data[firstDate].all_recipe_list,
      allRecipeListCount: data[firstDate].all_recipe_list?.length,
      dataKeys: Object.keys(data[firstDate])
    })
  }
  
  return data
}

// Query options with different cache strategies
export const deviceStatisticsQueries = {
  // All device data - fetches everything at once
  allDeviceData: () => ({
    queryKey: ['device-statistics', 'all-data'],
    queryFn: fetchAllDeviceData,
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 15, // 15 minutes
  }),
}