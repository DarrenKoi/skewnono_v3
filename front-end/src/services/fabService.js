import api from './api'

export const fabQueries = {
  list: () => ({
    queryKey: ['fab', 'list'],
    queryFn: async () => {
      const response = await api.get('/fab-list')
      return response.data
    },
    staleTime: 24 * 60 * 60 * 1000, // 24 hours
    cacheTime: 24 * 60 * 60 * 1000, // 24 hours
  }),
}