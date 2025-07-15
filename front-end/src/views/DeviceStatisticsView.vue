<template>
  <div class="device-statistics bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">디바이스 통계</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">
        {{ facId }} 시설의 디바이스 상태 및 통계 정보를 확인하세요
      </div>
    </div>
    
    <!-- R3 Facility - Multiple Selection -->
    <div v-if="facId === 'R3'" class="mb-8">
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
        <h3 class="text-xl font-semibold mb-4">디바이스 카테고리 선택</h3>
        <div class="flex flex-wrap gap-3">
          <div
            v-for="option in r3Options"
            :key="option"
            class="flex items-center p-3 border rounded-lg cursor-pointer transition-all duration-200"
            :class="{
              'border-primary bg-primary-50 dark:bg-primary-900/20': selectedR3Options.includes(option),
              'border-surface-300 dark:border-surface-600': !selectedR3Options.includes(option)
            }"
            @click="toggleR3Option(option)"
          >
            <Checkbox 
              v-model="selectedR3Options" 
              :value="option" 
              class="mr-2"
            />
            <label class="text-surface-900 dark:text-surface-0 cursor-pointer">{{ option }}</label>
          </div>
        </div>
      </div>
    </div>

    <!-- Non-R3 Facility - Single Selection -->
    <div v-else class="mb-8">
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
        <h3 class="text-xl font-semibold mb-4">디바이스 선택</h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="device in deviceOptions"
            :key="device"
            class="p-3 border rounded-lg cursor-pointer transition-all duration-200"
            :class="{
              'border-primary bg-primary-50 dark:bg-primary-900/20': selectedDevice === device,
              'border-surface-300 dark:border-surface-600': selectedDevice !== device
            }"
            @click="selectedDevice = device"
          >
            <div class="flex items-center">
              <RadioButton 
                v-model="selectedDevice" 
                :value="device" 
                class="mr-2"
              />
              <label class="text-surface-900 dark:text-surface-0 cursor-pointer">{{ device }}</label>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Display -->
    <div v-if="hasValidSelection" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold">
          {{ facId === 'R3' ? `선택된 카테고리: ${selectedR3Options.join(', ')}` : `선택된 디바이스: ${selectedDevice}` }}
        </h2>
        <Button @click="fetchDeviceData" :loading="loading" label="데이터 새로고침" icon="pi pi-refresh" />
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6" v-if="statisticsData">
        <Card>
          <template #content>
            <div class="flex flex-col items-center">
              <div class="text-3xl font-bold text-primary">{{ statisticsData.totalCount || 0 }}</div>
              <div class="text-sm text-surface-600 dark:text-surface-300">전체 항목</div>
            </div>
          </template>
        </Card>
        <Card>
          <template #content>
            <div class="flex flex-col items-center">
              <div class="text-3xl font-bold text-green-500">{{ statisticsData.activeCount || 0 }}</div>
              <div class="text-sm text-surface-600 dark:text-surface-300">활성 항목</div>
            </div>
          </template>
        </Card>
        <Card>
          <template #content>
            <div class="flex flex-col items-center">
              <div class="text-3xl font-bold text-yellow-500">{{ statisticsData.warningCount || 0 }}</div>
              <div class="text-sm text-surface-600 dark:text-surface-300">경고</div>
            </div>
          </template>
        </Card>
        <Card>
          <template #content>
            <div class="flex flex-col items-center">
              <div class="text-3xl font-bold text-red-500">{{ statisticsData.errorCount || 0 }}</div>
              <div class="text-sm text-surface-600 dark:text-surface-300">오류</div>
            </div>
          </template>
        </Card>
      </div>

      <!-- Data Table -->
      <div v-if="statisticsData && statisticsData.data" class="mt-6">
        <h3 class="text-lg font-semibold mb-4">상세 데이터</h3>
        <DataTable :value="statisticsData.data" stripedRows paginator :rows="10">
          <Column field="prod_id" header="제품 ID"></Column>
          <Column field="oper_id" header="작업 ID"></Column>
          <Column field="oper_desc" header="작업 설명"></Column>
          <Column field="eqp_id" header="장비 ID"></Column>
          <Column field="para_all" header="전체 파라미터">
            <template #body="{ data }">
              <Badge :value="data.para_all" severity="info" />
            </template>
          </Column>
          <Column field="skip_yn" header="스킵 여부">
            <template #body="{ data }">
              <Badge 
                :value="data.skip_yn" 
                :severity="data.skip_yn === 'Yes' ? 'warning' : 'success'"
              />
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- No Data State -->
      <div v-else-if="!loading" class="text-center py-12">
        <i class="pi pi-inbox text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300">선택된 항목에 대한 데이터가 없습니다</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <ProgressSpinner />
        <p class="mt-4 text-surface-600 dark:text-surface-300">데이터를 불러오는 중...</p>
      </div>
    </div>

    <!-- No Selection State -->
    <div v-else class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-info-circle text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300">
          {{ facId === 'R3' ? '카테고리를 선택해주세요' : '디바이스를 선택해주세요' }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Badge from 'primevue/badge'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Checkbox from 'primevue/checkbox'
import RadioButton from 'primevue/radiobutton'
import ProgressSpinner from 'primevue/progressspinner'
import axios from 'axios'

const route = useRoute()

// Get fac_id from route params or query
const facId = computed(() => route.params.facId || route.query.fac_id || 'R3')

// State for selections
const selectedR3Options = ref([])
const selectedDevice = ref('')
const r3Options = ref([])
const deviceOptions = ref([])
const statisticsData = ref(null)
const loading = ref(false)

// Computed property to check if valid selection is made
const hasValidSelection = computed(() => {
  if (facId.value === 'R3') {
    return selectedR3Options.value.length > 0
  } else {
    return selectedDevice.value !== ''
  }
})

// Toggle R3 option selection
const toggleR3Option = (option) => {
  const index = selectedR3Options.value.indexOf(option)
  if (index > -1) {
    selectedR3Options.value.splice(index, 1)
  } else {
    selectedR3Options.value.push(option)
  }
}

// Fetch device options based on fac_id
const fetchDeviceOptions = async () => {
  try {
    const response = await axios.get(`/api/device-statistics/device-options`, {
      params: { fac_id: facId.value }
    })
    
    if (facId.value === 'R3') {
      r3Options.value = response.data.options
    } else {
      deviceOptions.value = response.data.options
    }
  } catch (error) {
    console.error('Error fetching device options:', error)
    // Fallback to dummy data
    if (facId.value === 'R3') {
      r3Options.value = ['DRAM', 'NAND', 'NM']
    } else {
      deviceOptions.value = [
        'DEV-Alpha-001', 'DEV-Beta-002', 'DEV-Gamma-003', 'DEV-Delta-004',
        'DEV-Epsilon-005', 'DEV-Zeta-006', 'DEV-Eta-007', 'DEV-Theta-008',
        'DEV-Iota-009', 'DEV-Kappa-010'
      ]
    }
  }
}

// Fetch device statistics data
const fetchDeviceData = async () => {
  if (!hasValidSelection.value) return
  
  loading.value = true
  statisticsData.value = null
  
  try {
    if (facId.value === 'R3') {
      // For R3, fetch data for each selected option
      const promises = selectedR3Options.value.map(option =>
        axios.get(`/api/device-statistics/device-data`, {
          params: { fac_id: facId.value, option }
        })
      )
      
      const responses = await Promise.all(promises)
      
      // Combine data from all selected options
      const combinedData = {
        data: [],
        totalCount: 0,
        activeCount: 0,
        warningCount: 0,
        errorCount: 0
      }
      
      responses.forEach(response => {
        if (response.data.data) {
          combinedData.data.push(...response.data.data)
          combinedData.totalCount += response.data.data.length
          // Calculate other stats based on your data structure
          combinedData.activeCount += response.data.data.filter(item => item.skip_yn === 'No').length
          combinedData.warningCount += response.data.data.filter(item => item.para_all < 600).length
          combinedData.errorCount += response.data.data.filter(item => item.skip_yn === 'Yes').length
        }
      })
      
      statisticsData.value = combinedData
    } else {
      // For non-R3, fetch data for selected device
      const response = await axios.get(`/api/device-statistics/device-data`, {
        params: { fac_id: facId.value, option: selectedDevice.value }
      })
      
      const data = response.data.data || []
      statisticsData.value = {
        data: data,
        totalCount: data.length,
        activeCount: data.filter(item => item.skip_yn === 'No').length,
        warningCount: data.filter(item => item.para_all < 600).length,
        errorCount: data.filter(item => item.skip_yn === 'Yes').length
      }
    }
  } catch (error) {
    console.error('Error fetching device data:', error)
    statisticsData.value = null
  } finally {
    loading.value = false
  }
}

// Watch for selection changes to auto-fetch data
watch([selectedR3Options, selectedDevice], () => {
  if (hasValidSelection.value) {
    fetchDeviceData()
  }
}, { deep: true })

// Watch for fac_id changes to reset selections and fetch options
watch(facId, () => {
  selectedR3Options.value = []
  selectedDevice.value = ''
  statisticsData.value = null
  fetchDeviceOptions()
}, { immediate: true })

onMounted(() => {
  fetchDeviceOptions()
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>