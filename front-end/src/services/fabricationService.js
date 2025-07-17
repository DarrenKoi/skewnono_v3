import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000'

// Fabrication service for tool and fab data
export const fabricationService = {
  // Get tool-specific fab lists
  async getToolFabMapping() {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/fab-list`)
      return response.data
    } catch (error) {
      console.error('Error fetching tool-fab mapping:', error)
      throw error
    }
  }
}

// Query options for Vue Query integration
export const fabricationQueries = {
  toolFabMapping: () => ({
    queryKey: ['tool-fab-mapping'],
    queryFn: fabricationService.getToolFabMapping,
    staleTime: 1000 * 60 * 30, // 30 minutes
    cacheTime: 1000 * 60 * 60 * 4, // 4 hours
    retry: 3,
    retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000)
  })
}