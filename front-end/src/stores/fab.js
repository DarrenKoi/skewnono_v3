import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useFabStore = defineStore('fab', () => {
  // State
  const selectedFab = ref('')
  const fabList = ref(['R3', 'M16', 'M14', 'M15', 'M11', 'M10'])

  // Getters
  const hasFabSelection = computed(() => selectedFab.value !== '')
  const currentFab = computed(() => selectedFab.value)

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

  const clearFabSelection = () => {
    selectedFab.value = ''
    localStorage.removeItem('selectedFab')
  }

  const addFab = (fab) => {
    if (fab && !fabList.value.includes(fab)) {
      fabList.value.push(fab)
    }
  }

  const removeFab = (fab) => {
    const index = fabList.value.indexOf(fab)
    if (index > -1) {
      fabList.value.splice(index, 1)
      if (selectedFab.value === fab) {
        clearFabSelection()
      }
    }
  }

  // Initialize on store creation
  initializeFabSelection()

  return {
    // State
    selectedFab,
    fabList,
    // Getters
    hasFabSelection,
    currentFab,
    // Actions
    setSelectedFab,
    clearFabSelection,
    initializeFabSelection,
    addFab,
    removeFab
  }
})