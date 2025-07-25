<template>
  <div>
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <h3 class="text-xl font-semibold mb-4">디바이스 선택</h3>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <div v-for="device in deviceOptions" :key="device"
          class="p-3 border rounded-lg cursor-pointer transition-all duration-200" :class="{
            'border-primary bg-primary-50 dark:bg-primary-900/20': selectedDevice === device,
            'border-surface-300 dark:border-surface-600': selectedDevice !== device
          }" @click="selectDevice(device)">
          <div class="flex items-center">
            <RadioButton v-model="selectedDevice" :value="device" class="mr-2" />
            <label class="text-surface-900 dark:text-surface-0 cursor-pointer">{{ device }}</label>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Display for Non-R3 -->
    <div v-if="hasValidSelection" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <!-- Statistics Summary -->
      <div v-if="statisticsData" class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-primary-50 dark:bg-primary-900/20 rounded-lg p-4">
          <div class="text-2xl font-bold text-primary">{{ statisticsData.totalCount }}</div>
          <div class="text-sm text-surface-600 dark:text-surface-400">Total Items</div>
        </div>
        <div class="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ statisticsData.activeCount }}</div>
          <div class="text-sm text-surface-600 dark:text-surface-400">Active</div>
        </div>
        <div class="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-4">
          <div class="text-2xl font-bold text-yellow-600 dark:text-yellow-400">{{ statisticsData.warningCount }}</div>
          <div class="text-sm text-surface-600 dark:text-surface-400">Warnings</div>
        </div>
        <div class="bg-red-50 dark:bg-red-900/20 rounded-lg p-4">
          <div class="text-2xl font-bold text-red-600 dark:text-red-400">{{ statisticsData.errorCount }}</div>
          <div class="text-sm text-surface-600 dark:text-surface-400">Errors</div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-else-if="loading" class="text-center py-12">
        <i class="pi pi-spin pi-spinner text-4xl text-primary"></i>
        <p class="mt-2 text-surface-600 dark:text-surface-400">Loading device data...</p>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <p class="text-surface-600 dark:text-surface-300">Select a device to view statistics</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import RadioButton from 'primevue/radiobutton'
import axios from 'axios'

const props = defineProps({
  facId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['selectionChanged', 'dataFetched'])

// State for selections
const selectedDevice = ref('')
const deviceOptions = ref([])
const statisticsData = ref(null)
const loading = ref(false)

// Computed property to check if valid selection is made
const hasValidSelection = computed(() => {
  return selectedDevice.value !== ''
})

// Select device
const selectDevice = (device) => {
  selectedDevice.value = device
  emitSelectionChanged()
}

// Emit selection changed event
const emitSelectionChanged = () => {
  emit('selectionChanged', {
    selectedDevice: selectedDevice.value,
    hasValidSelection: hasValidSelection.value
  })
}

// Fetch device options based on fac_id
const fetchDeviceOptions = async () => {
  try {
    const response = await axios.get(`/api/device-statistics/device-options`, {
      params: { fac_id: props.facId }
    })

    deviceOptions.value = response.data.options
  } catch (error) {
    console.error('Error fetching device options:', error)
  }
}

// Fetch device statistics data
const fetchDeviceData = async () => {
  if (!hasValidSelection.value) return

  loading.value = true
  statisticsData.value = null

  try {
    const response = await axios.get(`/api/device-statistics/device-data`, {
      params: { fac_id: props.facId, option: selectedDevice.value }
    })

    const data = response.data.data || []
    statisticsData.value = {
      data: data,
      totalCount: data.length,
      activeCount: data.filter(item => item.skip_yn === 'No').length,
      warningCount: data.filter(item => item.para_all < 600).length,
      errorCount: data.filter(item => item.skip_yn === 'Yes').length
    }
    
    // Only emit the essential data, not the display counts
    emit('dataFetched', {
      data: data,
      selectedDevice: selectedDevice.value
    })
  } catch (error) {
    console.error('Error fetching device data:', error)
    statisticsData.value = null
    emit('dataFetched', null)
  } finally {
    loading.value = false
  }
}

// Watch for selection changes to auto-fetch data
watch(selectedDevice, () => {
  if (hasValidSelection.value) {
    fetchDeviceData()
  }
})

// Reset selections when facId changes
watch(() => props.facId, () => {
  selectedDevice.value = ''
  statisticsData.value = null
  fetchDeviceOptions()
}, { immediate: true })

onMounted(() => {
  fetchDeviceOptions()
})
</script>

<style scoped>
/* Component-specific styles if needed */
</style>