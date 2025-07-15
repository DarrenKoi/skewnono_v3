import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { fabQueries } from '@/services/fabService'

export const useFabStore = defineStore('fab', () => {
  // State
  const selectedFab = ref('')
  
  // Fetch fab list from API
  const { data: fabListData, isLoading: fabListLoading } = useQuery(fabQueries.list())
  
  // Computed fab list - fallback to empty object if not loaded
  const fabListDict = computed(() => fabListData.value || {})
  const fabList = computed(() => Object.keys(fabListDict.value).sort().reverse())

  // Getters
  const hasFabSelection = computed(() => selectedFab.value !== '')
  const currentFab = computed(() => selectedFab.value)
  const currentFabNames = computed(() => fabListDict.value[selectedFab.value] || [])

  // Actions
  const initializeFabSelection = () => {
    const savedFab = localStorage.getItem('selectedFab')
    if (savedFab && fabList.value.includes(savedFab)) {
      selectedFab.value = savedFab
    }
  }

  const setSelectedFab = (fab) => {
    if (fab && fabList.value.includes(fab)) {
      selectedFab.value = fab
      localStorage.setItem('selectedFab', fab)
    }
  }


  // Initialize on store creation
  initializeFabSelection()

  return {
    // State
    selectedFab,
    fabList,
    fabListDict,
    fabListLoading,
    // Getters
    hasFabSelection,
    currentFab,
    currentFabNames,
    // Actions
    setSelectedFab,
    initializeFabSelection
  }
})