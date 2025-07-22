<template>
  <div>
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <h3 class="text-xl font-semibold mb-4">디바이스 카테고리 선택</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <!-- Category Cards -->
        <div v-for="device in r3DevicesData" :key="device.category"
          class="border rounded-lg p-4 transition-all duration-200 cursor-pointer" :class="{
            'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-md': selectedR3Options.includes(device.category),
            'border-surface-300 dark:border-surface-600 hover:border-primary-300 hover:shadow-sm': !selectedR3Options.includes(device.category)
          }" @click="toggleR3Option(device.category)">
          <!-- Category Header -->
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-surface-900 dark:text-surface-0 font-semibold text-lg">{{ device.category }}</h4>
            <Badge v-if="selectedR3Options.includes(device.category) && selectedProdIdsByCategory[device.category]"
              :value="`${selectedProdIdsByCategory[device.category].length}/${device.prod_ids.length}`"
              :severity="selectedProdIdsByCategory[device.category].length === device.prod_ids.length ? 'success' : 'info'" />
          </div>

          <!-- Product IDs Summary -->
          <div class="text-sm text-surface-600 dark:text-surface-400">
            <div class="mb-2">{{ device.prod_ids.length }} Product IDs</div>
            <div v-if="selectedR3Options.includes(device.category)" class="flex flex-wrap gap-1">
              <Badge v-for="prodId in device.prod_ids.slice(0, 3)" :key="prodId" :value="prodId" size="small"
                :severity="isProdIdSelected(device.category, prodId) ? 'primary' : 'secondary'" />
              <Badge v-if="device.prod_ids.length > 3" :value="`+${device.prod_ids.length - 3} more`" size="small"
                severity="secondary" />
            </div>
          </div>

          <!-- Edit Button -->
          <Button v-if="selectedR3Options.includes(device.category)" label="Edit Selection" size="small" outlined
            class="w-full mt-3" @click.stop="showProdIdDialog(device)" />
        </div>
      </div>

      <!-- Product ID Selection Dialog -->
      <Dialog v-model:visible="prodIdDialogVisible" :header="`Select Product IDs for ${currentEditingCategory}`"
        :style="{ width: '50rem' }" :breakpoints="{ '1199px': '75vw', '575px': '90vw' }" modal>
        <div v-if="currentEditingDevice">
          <!-- Quick Actions -->
          <div class="flex gap-2 mb-4">
            <Button label="Select All" size="small"
              @click="selectAllProdIds(currentEditingCategory, currentEditingDevice.prod_ids)" />
            <Button label="Clear All" size="small" severity="secondary" @click="clearProdIds(currentEditingCategory)" />
            <div class="ml-auto text-sm text-surface-600 dark:text-surface-400 flex items-center">
              Selected: {{ selectedProdIdsByCategory[currentEditingCategory]?.length || 0 }} / {{
                currentEditingDevice.prod_ids.length }}
            </div>
          </div>

          <!-- Product IDs Grid -->
          <div class="grid grid-cols-4 md:grid-cols-6 gap-2 max-h-96 overflow-y-auto">
            <div v-for="prodId in currentEditingDevice.prod_ids" :key="prodId"
              class="p-2 border rounded cursor-pointer transition-all text-center" :class="{
                'border-primary bg-primary-100 dark:bg-primary-800/30': isProdIdSelected(currentEditingCategory, prodId),
                'border-surface-200 dark:border-surface-700 hover:border-primary/50': !isProdIdSelected(currentEditingCategory, prodId)
              }" @click="toggleProdId(currentEditingCategory, prodId)">
              <span class="text-sm">{{ prodId }}</span>
            </div>
          </div>
        </div>

        <template #footer>
          <Button label="Done" @click="prodIdDialogVisible = false" />
        </template>
      </Dialog>
    </div>

    <!-- Content Display for R3 -->
    <div v-if="hasValidSelection && !currentView" class="mt-8">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- 현재 상황 Card -->
        <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="selectView('current')">
          <template #content>
            <div class="text-center py-8">
              <i class="pi pi-chart-bar text-6xl text-primary mb-4"></i>
              <h3 class="text-xl font-semibold mb-2">현재 상황</h3>
              <p class="text-surface-600 dark:text-surface-400">최신 데이터 기준 파라미터 분포 확인</p>
            </div>
          </template>
        </Card>

        <!-- 주별 트렌드 Card -->
        <Card class="cursor-pointer hover:shadow-lg transition-shadow" @click="selectView('trend')">
          <template #content>
            <div class="text-center py-8">
              <i class="pi pi-chart-line text-6xl text-primary mb-4"></i>
              <h3 class="text-xl font-semibold mb-2">주별 트렌드</h3>
              <p class="text-surface-600 dark:text-surface-400">주별 데이터 변화 추이 분석</p>
            </div>
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import Badge from 'primevue/badge'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import { deviceStatisticsQueries } from '@/services/deviceStatisticsService'

const props = defineProps({
  facId: {
    type: String,
    required: true
  }
})

// Log initial mount
onMounted(() => {
  console.log('[FacR3Selection] Component mounted with facId:', props.facId)
})

const emit = defineEmits(['selectionChanged', 'dataFetched'])

const router = useRouter()

// State for selections
const selectedR3Options = ref([]) // Selected categories
const selectedProdIdsByCategory = ref({}) // Selected prod_ids per category
const r3Options = ref([])
const statisticsData = ref(null)

// Dialog state
const prodIdDialogVisible = ref(false)
const currentEditingCategory = ref('')
const currentEditingDevice = ref(null)

// View state
const currentView = ref(null) // 'current' or 'trend'

// Use vue-query to fetch all device data at once
const { data: allDeviceData, isLoading: dataLoading, error: dataError } = useQuery(
  deviceStatisticsQueries.allDeviceData()
)

// Add error handling
watch(dataError, (error) => {
  if (error) {
    console.error('[FacR3Selection] Error fetching data:', error)
  }
})

// Watch for data changes and log
watch(allDeviceData, (newData) => {
  if (newData) {
    console.log('[FacR3Selection] All device data received:', {
      hasData: !!newData,
      keys: Object.keys(newData),
      workingDevicesCount: newData.working_devices ? Object.keys(newData.working_devices).length : 0,
      deviceOptions: newData.device_options,
      dateCount: Object.keys(newData).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/)).length
    })
  }
}, { immediate: true })

// Computed property for devices data from the all-in-one response
const r3DevicesData = computed(() => {
  if (!allDeviceData.value?.device_options?.devices) {
    console.log('[FacR3Selection] No device options found in data')
    return null
  }
  console.log('[FacR3Selection] Device options extracted:', allDeviceData.value.device_options.devices)
  return allDeviceData.value.device_options.devices
})

// Computed property for the full statistics data
const fullStatisticsData = computed(() => {
  if (!allDeviceData.value) return null

  // Extract date-based data
  const dateKeys = Object.keys(allDeviceData.value).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/))
  const weeklyData = {}

  dateKeys.forEach(date => {
    weeklyData[date] = allDeviceData.value[date]
  })

  return {
    working_devices: allDeviceData.value.working_devices,
    device_options: allDeviceData.value.device_options,
    weekly_data: weeklyData,
    dateKeys: dateKeys.sort()
  }
})

// Computed property to check if we have valid prod_id selections
const hasValidSelection = computed(() => {
  return selectedR3Options.value.some(category =>
    selectedProdIdsByCategory.value[category] &&
    selectedProdIdsByCategory.value[category].length > 0
  )
})

// Toggle R3 option selection
const toggleR3Option = (option) => {
  const index = selectedR3Options.value.indexOf(option)
  if (index > -1) {
    // Remove category and its prod_ids
    selectedR3Options.value.splice(index, 1)
    delete selectedProdIdsByCategory.value[option]
  } else {
    // Add category and initialize with all prod_ids selected
    selectedR3Options.value.push(option)
    const device = r3DevicesData.value.find(d => d.category === option)
    if (device) {
      selectedProdIdsByCategory.value[option] = [...device.prod_ids]
    }
  }
  emitSelectionChanged()
}

// Check if a prod_id is selected
const isProdIdSelected = (category, prodId) => {
  return selectedProdIdsByCategory.value[category]?.includes(prodId) || false
}

// Toggle individual prod_id selection
const toggleProdId = (category, prodId) => {
  if (!selectedProdIdsByCategory.value[category]) {
    selectedProdIdsByCategory.value[category] = []
  }

  const index = selectedProdIdsByCategory.value[category].indexOf(prodId)
  if (index > -1) {
    selectedProdIdsByCategory.value[category].splice(index, 1)
  } else {
    selectedProdIdsByCategory.value[category].push(prodId)
  }
  emitSelectionChanged()
}

// Select all prod_ids for a category
const selectAllProdIds = (category, prodIds) => {
  selectedProdIdsByCategory.value[category] = [...prodIds]
  emitSelectionChanged()
}

// Clear all prod_ids for a category
const clearProdIds = (category) => {
  selectedProdIdsByCategory.value[category] = []
  emitSelectionChanged()
}

// Show product ID selection dialog
const showProdIdDialog = (device) => {
  currentEditingCategory.value = device.category
  currentEditingDevice.value = device
  prodIdDialogVisible.value = true
}

// Emit selection changed event
const emitSelectionChanged = () => {
  emit('selectionChanged', {
    selectedR3Options: selectedR3Options.value,
    selectedProdIdsByCategory: selectedProdIdsByCategory.value,
    hasValidSelection: hasValidSelection.value
  })
}

// Select view (current status or trend)
const selectView = (view) => {
  console.log('selectView called with:', view)
  console.log('hasValidSelection:', hasValidSelection.value)
  console.log('selectedR3Options:', selectedR3Options.value)
  console.log('selectedProdIdsByCategory:', selectedProdIdsByCategory.value)

  // Check if we have valid selections before navigating
  if (!hasValidSelection.value) {
    console.warn('No valid selections found, not navigating')
    return
  }

  // Store current selections and filtered data in session storage
  sessionStorage.setItem('deviceStatistics_selectedR3Options', JSON.stringify(selectedR3Options.value))
  sessionStorage.setItem('deviceStatistics_selectedProdIds', JSON.stringify(selectedProdIdsByCategory.value))
  sessionStorage.setItem('deviceStatistics_facId', props.facId)

  // Store the filtered statistics data for use in sub-routes
  if (statisticsData.value) {
    sessionStorage.setItem('deviceStatistics_filteredData', JSON.stringify(statisticsData.value))
    console.log('[FacR3Selection] Stored filtered data in session storage')
  }

  // Navigate to R3-specific sub-routes
  if (view === 'current') {
    console.log('Navigating to current status')
    router.push('/R3/device-statistics/cd-sem/current-status')
  } else if (view === 'trend') {
    console.log('Navigating to weekly trend')
    router.push('/R3/device-statistics/cd-sem/weekly-trend')
  }
}

// Update r3Options when device data changes
watch(r3DevicesData, (newData) => {
  if (newData) {
    r3Options.value = newData.map(d => d.category)
    console.log('[FacR3Selection] R3 options updated:', r3Options.value)
  }
}, { immediate: true })

// Computed filtered data based on selections
const filteredStatisticsData = computed(() => {
  if (!fullStatisticsData.value || !hasValidSelection.value) return null

  console.log('[FacR3Selection] Filtering data for selections:', {
    selectedCategories: selectedR3Options.value,
    selectedProdIds: selectedProdIdsByCategory.value
  })

  // Get all selected prod_ids
  const selectedProdIds = new Set()
  selectedR3Options.value.forEach(category => {
    const prodIds = selectedProdIdsByCategory.value[category] || []
    prodIds.forEach(id => selectedProdIds.add(id))
  })

  // Filter the weekly data based on selected prod_ids
  const filteredWeeklyData = {}

  Object.entries(fullStatisticsData.value.weekly_data).forEach(([date, dateData]) => {
    filteredWeeklyData[date] = {
      all_rcp_info: dateData.all_rcp_info?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      only_normal_rcp_info: dateData.only_normal_rcp_info?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      mother_normal_rcp_info: dateData.mother_normal_rcp_info?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      only_sample_rcp_info: dateData.only_sample_rcp_info?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      all_summary: dateData.all_summary?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      only_normal_summary: dateData.only_normal_summary?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      mother_normal_summary: dateData.mother_normal_summary?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      only_sample_summary: dateData.only_sample_summary?.filter(item => selectedProdIds.has(item.prod_id)) || [],
      all_recipe_list: dateData.all_recipe_list?.filter(item => selectedProdIds.has(item.prod_id)) || []
    }
  })

  return {
    working_devices: fullStatisticsData.value.working_devices,
    device_options: fullStatisticsData.value.device_options,
    weekly_data: filteredWeeklyData,
    selectedProdIds: Array.from(selectedProdIds)
  }
})

// Process filtered data for statistics
const processFilteredData = () => {
  if (!filteredStatisticsData.value) return null

  const dateKeys = Object.keys(filteredStatisticsData.value.weekly_data).sort().reverse()
  if (dateKeys.length === 0) return null

  // Get the most recent week's data for statistics
  const latestDate = dateKeys[0]
  const latestData = filteredStatisticsData.value.weekly_data[latestDate]

  const stats = {
    data: latestData.all_rcp_info || [],
    totalCount: latestData.all_rcp_info?.length || 0,
    activeCount: latestData.all_rcp_info?.filter(item => item.skip_yn === 'No').length || 0,
    warningCount: latestData.all_rcp_info?.filter(item => item.para_all < 600).length || 0,
    errorCount: latestData.all_rcp_info?.filter(item => item.skip_yn === 'Yes').length || 0,
    weeklyData: filteredStatisticsData.value.weekly_data,
    working_devices: filteredStatisticsData.value.working_devices,
    device_options: filteredStatisticsData.value.device_options
  }

  console.log('[FacR3Selection] Processed statistics:', {
    latestDate,
    totalCount: stats.totalCount,
    weekCount: dateKeys.length,
    selectedProdIds: filteredStatisticsData.value.selectedProdIds
  })

  return stats
}

// Update statistics when filtered data changes
watch(filteredStatisticsData, (newData) => {
  if (newData) {
    statisticsData.value = processFilteredData()
    emit('dataFetched', statisticsData.value)
  }
}, { immediate: true })

// Reset selections when facId changes
watch(() => props.facId, () => {
  selectedR3Options.value = []
  selectedProdIdsByCategory.value = {}
  statisticsData.value = null
  currentView.value = null
}, { immediate: true })
</script>

<style scoped>
/* Component-specific styles if needed */
</style>
