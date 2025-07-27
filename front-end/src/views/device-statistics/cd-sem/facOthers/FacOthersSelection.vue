<template>
  <div>
    <!-- Product Selection -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-surface-900 dark:text-surface-0">Product Selection</h3>
        <div class="flex gap-2">
          <Button label="Select All" size="small" text @click="selectAllProducts" />
          <Button label="Clear All" size="small" text severity="secondary" @click="clearAllProducts" />
        </div>
      </div>
      
      <!-- Product buttons in grid -->
      <div class="grid grid-cols-6 gap-2">
        <Button 
          v-for="prodId in availableProducts" 
          :key="prodId"
          :label="prodId"
          :severity="selectedProducts.includes(prodId) ? 'primary' : 'secondary'"
          :outlined="!selectedProducts.includes(prodId)"
          size="small"
          class="font-mono"
          @click="toggleProduct(prodId)"
        />
      </div>
      
      <div class="mt-4 text-sm text-surface-500">
        Selected: {{ selectedProducts.length }} of {{ availableProducts.length }} products
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border text-center">
      <i class="pi pi-spin pi-spinner text-4xl text-primary"></i>
      <p class="mt-2 text-surface-600 dark:text-surface-400">Loading CD-SEM data...</p>
    </div>

    <!-- Content Display for Other Fabs -->
    <div v-if="hasValidSelection && !loading" class="mt-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Current Status Card -->
        <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="selectView('current')">
          <template #content>
            <div class="text-center py-8">
              <i class="pi pi-chart-bar text-6xl text-primary mb-4"></i>
              <h3 class="text-xl font-semibold mb-2">Current Status</h3>
              <p class="text-surface-600 dark:text-surface-400">View latest parameter distribution</p>
            </div>
          </template>
        </Card>

        <!-- Weekly Trend Card -->
        <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="selectView('trend')">
          <template #content>
            <div class="text-center py-8">
              <i class="pi pi-chart-line text-6xl text-primary mb-4"></i>
              <h3 class="text-xl font-semibold mb-2">Weekly Trend</h3>
              <p class="text-surface-600 dark:text-surface-400">Analyze weekly data trends</p>
            </div>
          </template>
        </Card>
      </div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border text-center">
      <i class="pi pi-exclamation-triangle text-4xl text-red-500 mb-2"></i>
      <p class="text-surface-600 dark:text-surface-300">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import Card from 'primevue/card'
import axios from 'axios'

const props = defineProps({
  facId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['selectionChanged', 'dataFetched'])

const router = useRouter()

// State
const statisticsData = ref(null)
const loading = ref(false)
const error = ref(null)
const selectedProducts = ref([])
const availableProducts = ref([])
const filteredData = ref(null)

// Computed properties
const availableDates = computed(() => {
  if (!statisticsData.value) return []
  // Get date keys (excluding metadata keys)
  return Object.keys(statisticsData.value)
    .filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/))
    .sort((a, b) => new Date(b) - new Date(a)) // Sort descending
})

const latestDate = computed(() => {
  // Get the most recent date for current-status view
  return availableDates.value.length > 0 ? availableDates.value[0] : null
})

// Check if we have valid selections
const hasValidSelection = computed(() => {
  return selectedProducts.value.length > 0 && statisticsData.value
})

// Methods
const toggleProduct = (prodId) => {
  const index = selectedProducts.value.indexOf(prodId)
  if (index > -1) {
    selectedProducts.value.splice(index, 1)
  } else {
    selectedProducts.value.push(prodId)
  }
}

const selectAllProducts = () => {
  selectedProducts.value = [...availableProducts.value]
}

const clearAllProducts = () => {
  selectedProducts.value = []
}

// Select view (current status or trend)
const selectView = (view) => {
  console.log('selectView called with:', view)
  console.log('hasValidSelection:', hasValidSelection.value)
  console.log('selectedProducts:', selectedProducts.value)
  
  if (!hasValidSelection.value) {
    console.warn('No valid selections found, not navigating')
    return
  }
  
  // Store selections and filtered data in sessionStorage
  sessionStorage.setItem(`deviceStatistics_selectedProducts_${props.facId}`, JSON.stringify(selectedProducts.value))
  sessionStorage.setItem(`deviceStatistics_filteredData_${props.facId}`, JSON.stringify(filteredData.value))
  
  // Navigate to facility-specific sub-routes
  if (view === 'current') {
    console.log('Navigating to current status')
    router.push(`/${props.facId}/device-statistics/cd-sem/current-status`)
  } else if (view === 'trend') {
    console.log('Navigating to weekly trend')
    router.push(`/${props.facId}/device-statistics/cd-sem/weekly-trend`)
  }
}



// Fetch CD-SEM statistics data for other fabs
const fetchCdSemData = async () => {
  console.log(`[FacOthersSelection] Fetching CD-SEM data for facility: ${props.facId}`)
  loading.value = true
  statisticsData.value = null
  error.value = null

  try {
    const response = await axios.get(`/api/device-statistics/device-data`, {
      params: { 
        fac_id: props.facId
      }
    })

    console.log(`[FacOthersSelection] Received data:`, response.data)
    statisticsData.value = response.data
    
    // Extract available products (now a flat list)
    if (response.data.available_products) {
      availableProducts.value = response.data.available_products
      // Auto-select all products initially
      if (selectedProducts.value.length === 0) {
        selectedProducts.value = [...availableProducts.value]
      }
    }
    
    // Emit initial data
    emitSelectionData()
  } catch (err) {
    console.error('[FacOthersSelection] Error fetching CD-SEM data:', err)
    error.value = err.response?.data?.error || 'Failed to load CD-SEM data'
    statisticsData.value = null
  } finally {
    loading.value = false
  }
}

// Emit data when selection changes
const emitSelectionData = () => {
  if (selectedProducts.value.length > 0 && statisticsData.value) {
    // Prepare filtered data for all dates
    const filtered = {}
    
    // Add metadata
    filtered.working_devices = statisticsData.value.working_devices
    filtered.fac_id = statisticsData.value.fac_id
    
    // Filter each date's data based on selected products
    availableDates.value.forEach(dateKey => {
      const dateData = statisticsData.value[dateKey]
      if (dateData) {
        filtered[dateKey] = {
          all_rcp_info: dateData.all_rcp_info?.filter(item => selectedProducts.value.includes(item.prod_id)),
          only_normal_rcp_info: dateData.only_normal_rcp_info?.filter(item => selectedProducts.value.includes(item.prod_id)),
          mother_normal_rcp_info: dateData.mother_normal_rcp_info?.filter(item => selectedProducts.value.includes(item.prod_id)),
          only_sample_rcp_info: dateData.only_sample_rcp_info?.filter(item => selectedProducts.value.includes(item.prod_id)),
          all_summary: dateData.all_summary?.filter(item => selectedProducts.value.includes(item.prod_id)),
          only_normal_summary: dateData.only_normal_summary?.filter(item => selectedProducts.value.includes(item.prod_id)),
          mother_normal_summary: dateData.mother_normal_summary?.filter(item => selectedProducts.value.includes(item.prod_id)),
          only_sample_summary: dateData.only_sample_summary?.filter(item => selectedProducts.value.includes(item.prod_id)),
          all_recipe_list: dateData.all_recipe_list?.filter(item => selectedProducts.value.includes(item.prod_id))
        }
      }
    })
    
    // Set the filtered data for the views
    filteredData.value = filtered
    
    emit('dataFetched', {
      data: filtered,
      selectedProducts: selectedProducts.value,
      latestDate: latestDate.value,
      allDates: availableDates.value,
      fac_id: props.facId
    })
    
    emit('selectionChanged', {
      hasValidSelection: true,
      fac_id: props.facId,
      products: selectedProducts.value
    })
  }
}

// Watchers
watch(() => props.facId, (newFacId, oldFacId) => {
  console.log(`[FacOthersSelection] Facility ID changed from ${oldFacId} to ${newFacId}`)
  if (props.facId && props.facId.startsWith('M')) {
    // Reset selections when facility changes
    selectedProducts.value = []
    fetchCdSemData()
  }
}, { immediate: true })

// Watch for selection changes
watch(selectedProducts, () => {
  if (statisticsData.value) {
    emitSelectionData()
  }
}, { deep: true })

onMounted(() => {
  console.log(`[FacOthersSelection] Component mounted with facility: ${props.facId}`)
  // Fetch data on mount if facId is already set
  if (props.facId && props.facId.startsWith('M')) {
    fetchCdSemData()
  }
})
</script>

<style scoped>
/* Component-specific styles if needed */
</style>