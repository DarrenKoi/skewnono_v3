import { computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import api from './api'

// Recipe API functions
export const recipeApi = {
  // Get recipe list for a specific facility and tool
  getRecipeList: (facId, toolType) => {
    return api.get(`/recipe-search/${facId}/${toolType}`)
  }
}

// Recipe query keys factory
export const recipeKeys = {
  all: ['recipe'],
  lists: () => [...recipeKeys.all, 'list'],
  list: (facId, toolType) => [...recipeKeys.lists(), facId, toolType]
}

// Recipe query options
export const recipeQueries = {
  list: (facId, toolType) => ({
    queryKey: recipeKeys.list(facId, toolType),
    queryFn: () => recipeApi.getRecipeList(facId, toolType).then(res => res.data),
    staleTime: 15 * 60 * 1000, // 15 minutes
    gcTime: 15 * 60 * 1000, // 15 minutes (formerly cacheTime)
    enabled: !!(facId && toolType) // Only run query if both params are available
  })
}

// Vue Query hook for recipe list
export const useRecipeList = (facId, toolType) => {
  return useQuery({
    queryKey: computed(() => recipeKeys.list(facId.value || facId, toolType.value || toolType)),
    queryFn: () => recipeApi.getRecipeList(facId.value || facId, toolType.value || toolType).then(res => res.data),
    staleTime: 15 * 60 * 1000, // 15 minutes
    gcTime: 15 * 60 * 1000, // 15 minutes
    enabled: computed(() => !!(
      (facId.value || facId) && 
      (toolType.value || toolType)
    ))
  })
}