import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { fabQueries } from '@/services/fabService'

export const useFabStore = defineStore('fab', () => {
  // State
  const selectedFab = ref('')
  const selectedTool = ref('')
  const localStorageInitialized = ref(false)
  
  // Fetch fab list from API
  const { data: fabListData, isLoading: fabListLoading } = useQuery(fabQueries.list())
  
  // Computed fab list - fallback to empty object if not loaded
  const fabListDict = computed(() => fabListData.value || {})
  const fabList = computed(() => Object.keys(fabListDict.value).sort().reverse())
  
  // Tool availability mapping
  const toolMapping = computed(() => ({
    'R3': ['CD-SEM'],
    'M16': ['HV-SEM'],
    'C1': ['CD-SEM', 'HV-SEM'],
    'C2': ['CD-SEM', 'HV-SEM'],
    'C3': ['CD-SEM', 'HV-SEM'],
    'default': ['CD-SEM', 'HV-SEM'] // fallback for other fabs
  }))
  
  // Cascade select options for fab → tool selection
  const cascadeOptions = computed(() => {
    return fabList.value.map(fab => ({
      label: fab,
      value: fab,
      children: (toolMapping.value[fab] || toolMapping.value.default).map(tool => ({
        label: tool,
        value: tool
      }))
    }))
  })

  // Getters
  const hasFabSelection = computed(() => selectedFab.value !== '')
  const hasToolSelection = computed(() => selectedTool.value !== '')
  const hasCompleteSelection = computed(() => hasFabSelection.value && hasToolSelection.value)
  const currentFab = computed(() => selectedFab.value)
  const currentTool = computed(() => selectedTool.value)
  const currentFabNames = computed(() => fabListDict.value[selectedFab.value] || [])
  const availableTools = computed(() => {
    if (!selectedFab.value) return []
    return toolMapping.value[selectedFab.value] || toolMapping.value.default
  })

  // Actions
  const initializeFabSelection = () => {
    const savedFab = localStorage.getItem('selectedFab')
    const savedTool = localStorage.getItem('selectedTool')
    
    if (savedFab && fabList.value.includes(savedFab)) {
      selectedFab.value = savedFab
      
      // Validate tool selection against available tools for this fab
      const availableToolsForFab = toolMapping.value[savedFab] || toolMapping.value.default
      if (savedTool && availableToolsForFab.includes(savedTool)) {
        selectedTool.value = savedTool
      } else if (availableToolsForFab.length === 1) {
        // Auto-select if only one tool available
        selectedTool.value = availableToolsForFab[0]
        localStorage.setItem('selectedTool', availableToolsForFab[0])
      }
      
      localStorageInitialized.value = true
    }
  }

  const setSelectedFab = (fab) => {
    if (fab && fabList.value.includes(fab)) {
      selectedFab.value = fab
      localStorage.setItem('selectedFab', fab)
      
      // Reset tool selection when fab changes
      const availableToolsForFab = toolMapping.value[fab] || toolMapping.value.default
      if (availableToolsForFab.length === 1) {
        // Auto-select if only one tool available
        selectedTool.value = availableToolsForFab[0]
        localStorage.setItem('selectedTool', availableToolsForFab[0])
      } else {
        // Clear tool selection if multiple options
        selectedTool.value = ''
        localStorage.removeItem('selectedTool')
      }
    }
  }
  
  const setSelectedTool = (tool) => {
    if (tool && availableTools.value.includes(tool)) {
      selectedTool.value = tool
      localStorage.setItem('selectedTool', tool)
    }
  }
  
  const setCascadeSelection = (selection) => {
    if (selection && selection.length === 2) {
      const [fab, tool] = selection
      setSelectedFab(fab)
      setSelectedTool(tool)
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
    selectedTool,
    fabList,
    fabListDict,
    fabListLoading,
    cascadeOptions,
    // Getters
    hasFabSelection,
    hasToolSelection,
    hasCompleteSelection,
    currentFab,
    currentTool,
    currentFabNames,
    availableTools,
    toolMapping,
    // Actions
    setSelectedFab,
    setSelectedTool,
    setCascadeSelection,
    initializeFabSelection
  }
})