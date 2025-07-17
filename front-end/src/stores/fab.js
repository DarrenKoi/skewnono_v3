import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { fabQueries } from '@/services/fabService'

export const useFabStore = defineStore('fab', () => {
  // State
  const selectedFab = ref('')
  const localStorageInitialized = ref(false)
  
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
      localStorageInitialized.value = true
    }
  }

  const setSelectedFab = (fab) => {
    if (fab && fabList.value.includes(fab)) {
      selectedFab.value = fab
      localStorage.setItem('selectedFab', fab)
    }
  }

  // Watch for fabList changes to re-initialize from localStorage
  watch(fabList, (newFabList) => {
    // Only initialize once when fabList is loaded and we haven't initialized yet
    if (newFabList.length > 0 && !localStorageInitialized.value && !selectedFab.value) {
      const savedFab = localStorage.getItem('selectedFab')
      if (savedFab && newFabList.includes(savedFab)) {
        selectedFab.value = savedFab
        localStorageInitialized.value = true
      }
    }
  }, { immediate: true })

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