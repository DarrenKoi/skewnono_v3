<template>
  <div class="recipe-measurement-history bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="flex items-center gap-4">
        <Button 
          icon="pi pi-arrow-left" 
          rounded 
          text 
          @click="goBack"
          v-tooltip.right="'이전 페이지로'"
        />
        <div>
          <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">HV-SEM 측정 기록</div>
          <div class="text-surface-500 dark:text-surface-300 text-lg mt-1">Recipe의 측정 기록을 조회합니다</div>
        </div>
      </div>
    </div>

    <!-- Search Parameters Card -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold">검색 조건</h3>
        <Button 
          label="검색" 
          icon="pi pi-search" 
          @click="searchMeasurements"
          :loading="searching"
        />
      </div>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="text-sm text-surface-600 dark:text-surface-400 mb-2 block">Recipe</label>
          <p class="text-surface-900 dark:text-surface-0 font-medium">{{ selectedRecipe }}</p>
        </div>
        <div>
          <label class="text-sm text-surface-600 dark:text-surface-400 mb-2 block">시작일</label>
          <p class="text-surface-900 dark:text-surface-0 font-medium">{{ formatDate(dateRange[0]) }}</p>
        </div>
        <div>
          <label class="text-sm text-surface-600 dark:text-surface-400 mb-2 block">종료일</label>
          <p class="text-surface-900 dark:text-surface-0 font-medium">{{ formatDate(dateRange[1]) }}</p>
        </div>
      </div>
    </div>

    <!-- Summary Statistics -->
    <div v-if="searchPerformed" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-4 shadow-sm border">
        <div class="flex items-center gap-3">
          <i class="pi pi-chart-bar text-2xl text-blue-500"></i>
          <div>
            <p class="text-sm text-surface-600 dark:text-surface-400">총 측정 수</p>
            <p class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ summaryStats.totalMeasurements }}</p>
          </div>
        </div>
      </div>
      
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-4 shadow-sm border">
        <div class="flex items-center gap-3">
          <i class="pi pi-check-circle text-2xl text-green-500"></i>
          <div>
            <p class="text-sm text-surface-600 dark:text-surface-400">성공률</p>
            <p class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ summaryStats.successRate }}%</p>
          </div>
        </div>
      </div>
      
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-4 shadow-sm border">
        <div class="flex items-center gap-3">
          <i class="pi pi-clock text-2xl text-orange-500"></i>
          <div>
            <p class="text-sm text-surface-600 dark:text-surface-400">평균 시간</p>
            <p class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ summaryStats.avgTime }}s</p>
          </div>
        </div>
      </div>
      
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-4 shadow-sm border">
        <div class="flex items-center gap-3">
          <i class="pi pi-desktop text-2xl text-purple-500"></i>
          <div>
            <p class="text-sm text-surface-600 dark:text-surface-400">사용 장비</p>
            <p class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ summaryStats.equipmentCount }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Measurement History Table -->
    <div v-if="searchPerformed" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold">측정 기록</h3>
        <div class="flex gap-2">
          <Button 
            label="Export CSV" 
            icon="pi pi-download" 
            severity="secondary"
            size="small"
            @click="exportToCsv"
          />
          <Button 
            label="Chart View" 
            icon="pi pi-chart-line" 
            severity="secondary"
            size="small"
            @click="showChart = !showChart"
          />
        </div>
      </div>
      
      <!-- Chart View Toggle -->
      <div v-if="showChart" class="mb-6 bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
        <div ref="chartRef" style="height: 400px; width: 100%;"></div>
      </div>
      
      <DataTable 
        :value="measurementHistory" 
        :paginator="true" 
        :rows="15"
        :rowsPerPageOptions="[15, 30, 50]"
        paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} measurements"
        responsiveLayout="scroll"
        :loading="loading"
        :globalFilterFields="['equipmentId', 'waferLot', 'status']"
      >
        <Column field="measurementId" header="측정 ID" :sortable="true" />
        <Column field="timestamp" header="측정 시간" :sortable="true" />
        <Column field="equipmentId" header="장비 ID" :sortable="true" />
        <Column field="waferLot" header="Wafer Lot" :sortable="true" />
        <Column field="measurementTime" header="측정 시간(s)" :sortable="true" />
        <Column field="beamVoltage" header="Beam Voltage (kV)" :sortable="true" />
        <Column field="magnification" header="배율" :sortable="true" />
        <Column field="status" header="상태">
          <template #body="slotProps">
            <Tag 
              :value="slotProps.data.status" 
              :severity="getStatusSeverity(slotProps.data.status)"
            />
          </template>
        </Column>
        <Column header="Actions">
          <template #body="slotProps">
            <Button 
              icon="pi pi-eye" 
              size="small" 
              text
              v-tooltip.top="'상세 보기'"
              @click="viewDetails(slotProps.data)"
            />
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import * as echarts from 'echarts'

const router = useRouter()

// Reactive data
const selectedRecipe = ref('')
const dateRange = ref([])
const loading = ref(false)
const searching = ref(false)
const searchPerformed = ref(false)
const showChart = ref(false)
const chartRef = ref(null)
let chartInstance = null

// Sample data
const measurementHistory = ref([])
const summaryStats = ref({
  totalMeasurements: 0,
  successRate: 0,
  avgTime: 0,
  equipmentCount: 0
})

// Methods
const goBack = () => {
  router.back()
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('ko-KR')
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'Success':
      return 'success'
    case 'Warning':
      return 'warning'
    case 'Failed':
      return 'danger'
    default:
      return 'info'
  }
}

const searchMeasurements = async () => {
  searching.value = true
  loading.value = true
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  // Generate sample measurement data
  const sampleData = []
  const equipments = ['HV-001', 'HV-002', 'HV-003', 'HV-004']
  const statuses = ['Success', 'Warning', 'Failed']
  const waferLots = ['LOT001', 'LOT002', 'LOT003', 'LOT004', 'LOT005']
  
  for (let i = 1; i <= 50; i++) {
    const timestamp = new Date(dateRange.value[0].getTime() + Math.random() * (dateRange.value[1].getTime() - dateRange.value[0].getTime()))
    sampleData.push({
      measurementId: `MEAS_${String(i).padStart(4, '0')}`,
      timestamp: timestamp.toLocaleString('ko-KR'),
      equipmentId: equipments[Math.floor(Math.random() * equipments.length)],
      waferLot: waferLots[Math.floor(Math.random() * waferLots.length)],
      measurementTime: (Math.random() * 120 + 30).toFixed(1),
      beamVoltage: (Math.random() * 20 + 20).toFixed(1),
      magnification: Math.floor(Math.random() * 90000 + 10000),
      status: statuses[Math.floor(Math.random() * statuses.length)]
    })
  }
  
  measurementHistory.value = sampleData
  
  // Calculate summary statistics
  const total = sampleData.length
  const successful = sampleData.filter(item => item.status === 'Success').length
  const avgTime = sampleData.reduce((sum, item) => sum + parseFloat(item.measurementTime), 0) / total
  const uniqueEquipments = new Set(sampleData.map(item => item.equipmentId)).size
  
  summaryStats.value = {
    totalMeasurements: total,
    successRate: Math.round((successful / total) * 100),
    avgTime: avgTime.toFixed(1),
    equipmentCount: uniqueEquipments
  }
  
  searching.value = false
  loading.value = false
  searchPerformed.value = true
}

const viewDetails = (measurement) => {
  console.log('Viewing details for:', measurement)
  // In real implementation, this would open a detail dialog or navigate to detail page
}

const exportToCsv = () => {
  console.log('Exporting to CSV...')
  // In real implementation, this would generate and download CSV file
}

const initChart = async () => {
  if (!chartRef.value || !showChart.value) return
  
  await nextTick()
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  
  // Process data for chart
  const equipmentCounts = {}
  measurementHistory.value.forEach(item => {
    equipmentCounts[item.equipmentId] = (equipmentCounts[item.equipmentId] || 0) + 1
  })
  
  const option = {
    title: {
      text: '장비별 측정 횟수',
      left: 'center'
    },
    tooltip: {
      trigger: 'item'
    },
    xAxis: {
      type: 'category',
      data: Object.keys(equipmentCounts)
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: Object.values(equipmentCounts),
      type: 'bar',
      itemStyle: {
        color: '#3b82f6'
      }
    }]
  }
  
  chartInstance.setOption(option)
}

// Load recipe data on mount
onMounted(() => {
  // Get selected recipe and date range from sessionStorage
  selectedRecipe.value = sessionStorage.getItem('selectedRecipe') || 'HV_RECIPE_001_STANDARD'
  
  const storedDateRange = sessionStorage.getItem('dateRange')
  if (storedDateRange) {
    const parsedRange = JSON.parse(storedDateRange)
    dateRange.value = parsedRange.map(date => new Date(date))
  } else {
    // Default to last month
    const today = new Date()
    const oneMonthAgo = new Date()
    oneMonthAgo.setMonth(today.getMonth() - 1)
    dateRange.value = [oneMonthAgo, today]
  }
})

// Watch for chart visibility change
watch(showChart, (newValue) => {
  if (newValue) {
    nextTick(() => initChart())
  } else if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})

// Cleanup on unmount
onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>