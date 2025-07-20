import api from './api'

// API functions
const fetchDeviceOptions = async (facId) => {
  const { data } = await api.get('/device-statistics/device-options', {
    params: { fac_id: facId }
  })
  return data
}

const fetchDeviceData = async ({ facId, option, prodIds }) => {
  const { data } = await api.get('/device-statistics/device-data', {
    params: {
      fac_id: facId,
      option,
      'prod_ids[]': prodIds
    },
    paramsSerializer: params => {
      const searchParams = new URLSearchParams()
      searchParams.append('fac_id', params.fac_id)
      searchParams.append('option', params.option)
      params['prod_ids[]'].forEach(id => searchParams.append('prod_ids[]', id))
      return searchParams.toString()
    }
  })
  return data
}

// Query options with different cache strategies
export const deviceStatisticsQueries = {
  // Device options - relatively static data, updates infrequently
  deviceOptions: (facId) => ({
    queryKey: ['device-statistics', 'options', facId],
    queryFn: () => fetchDeviceOptions(facId),
    staleTime: 1000 * 60 * 30, // 30 minutes
    cacheTime: 1000 * 60 * 60 * 2, // 2 hours
    enabled: !!facId,
  }),

  // Device data - dynamic based on selections, moderate update frequency
  deviceData: (facId, option, prodIds) => ({
    queryKey: ['device-statistics', 'data', facId, option, prodIds],
    queryFn: () => fetchDeviceData({ facId, option, prodIds }),
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 15, // 15 minutes
    enabled: !!(facId && option && prodIds?.length > 0),
  }),

  // Multiple device data queries - for batch fetching
  multipleDeviceData: (facId, selections) => ({
    queryKey: ['device-statistics', 'multiple-data', facId, selections],
    queryFn: async () => {
      const promises = selections
        .filter(selection => selection.prodIds?.length > 0)
        .map(selection => 
          fetchDeviceData({
            facId,
            option: selection.option,
            prodIds: selection.prodIds
          })
        )
      return Promise.all(promises)
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
    cacheTime: 1000 * 60 * 15, // 15 minutes
    enabled: !!(facId && selections?.length > 0),
  }),
}