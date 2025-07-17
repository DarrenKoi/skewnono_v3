<template>
  <div class="recipe-measurement-history bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button 
        icon="pi pi-arrow-left" 
        label="Recipe 검색으로 돌아가기"
        outlined
        size="large"
        class="mb-2"
        @click="$router.push({ name: 'recipe-search' })" 
      />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Meas. History</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">측정 기록을 확인할 수 있습니다</div>
      </div>
    </div>

    <!-- Content Display -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex flex-col gap-6">
        <!-- Selected Recipe Display -->
        <div class="flex flex-col gap-3">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">선택된 Recipe</label>
          <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-3 border">
            <p class="text-surface-700 dark:text-surface-200">
              {{ selectedRecipe || 'Recipe 검색 페이지에서 선택하세요' }}
            </p>
          </div>
        </div>

        <!-- Date Range Selection -->
        <div class="flex flex-col gap-3">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">기간 선택</label>
          <div class="flex gap-3 flex-wrap">
            <Calendar 
              v-model="dateRange" 
              selectionMode="range" 
              :manualInput="false" 
              dateFormat="yy/mm/dd"
              placeholder="날짜 범위 선택"
              showIcon
              class="w-full sm:w-auto"
            />
          </div>
        </div>

        <!-- Action Button -->
        <div class="flex pt-4">
          <Button 
            label="측정 기록 조회"
            icon="pi pi-history"
            @click="viewMeasurementHistory"
            :disabled="!selectedRecipe || !dateRange"
            :loading="isLoading"
            class="w-full sm:w-auto"
          />
        </div>

        <!-- Selected Recipe Info -->
        <div v-if="selectedRecipe" class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
          <div class="flex items-center gap-3">
            <i class="pi pi-info-circle text-primary"></i>
            <div>
              <h3 class="font-semibold text-surface-900 dark:text-surface-0">선택된 Recipe</h3>
              <p class="text-surface-700 dark:text-surface-200 mt-1">{{ selectedRecipe }}</p>
              <p v-if="dateRange && dateRange[0]" class="text-surface-600 dark:text-surface-400 text-sm mt-1">
                기간: {{ formatDate(dateRange[0]) }} ~ {{ formatDate(dateRange[1]) || '선택하세요' }}
              </p>
            </div>
          </div>
        </div>

        <!-- Results Section -->
        <div v-if="actionResult" class="mt-4">
          <Message :severity="actionResult.severity" :closable="true" @close="actionResult = null">
            {{ actionResult.message }}
          </Message>
        </div>

        <!-- Measurement History Results -->
        <div v-if="historyData" class="mt-6">
          <h3 class="text-xl font-semibold mb-4">측정 기록 결과</h3>
          
          <!-- Summary Statistics -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4 text-center">
              <p class="text-surface-600 dark:text-surface-400 text-sm">총 측정 횟수</p>
              <p class="text-2xl font-bold text-primary mt-1">{{ historyData.totalMeasurements }}</p>
            </div>
            <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4 text-center">
              <p class="text-surface-600 dark:text-surface-400 text-sm">평균값</p>
              <p class="text-2xl font-bold text-blue-500 mt-1">{{ historyData.average }}</p>
            </div>
            <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4 text-center">
              <p class="text-surface-600 dark:text-surface-400 text-sm">최대값</p>
              <p class="text-2xl font-bold text-orange-500 mt-1">{{ historyData.max }}</p>
            </div>
            <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4 text-center">
              <p class="text-surface-600 dark:text-surface-400 text-sm">최소값</p>
              <p class="text-2xl font-bold text-green-500 mt-1">{{ historyData.min }}</p>
            </div>
          </div>

          <!-- Chart -->
          <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4 mb-6">
            <div ref="chartRef" style="height: 300px; width: 100%;"></div>
          </div>

          <!-- Detailed History Table -->
          <DataTable 
            :value="historyData.records" 
            :paginator="true" 
            :rows="10"
            paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
            currentPageReportTemplate="{first} - {last} of {totalRecords}"
            :rowsPerPageOptions="[10, 25, 50]"
            class="p-datatable-sm"
          >
            <Column field="timestamp" header="측정 시간" sortable>
              <template #body="slotProps">
                {{ formatDateTime(slotProps.data.timestamp) }}
              </template>
            </Column>
            <Column field="equipment" header="장비" sortable></Column>
            <Column field="value" header="측정값" sortable>
              <template #body="slotProps">
                <span :class="getValueClass(slotProps.data.value)">
                  {{ slotProps.data.value }}
                </span>
              </template>
            </Column>
            <Column field="status" header="상태" sortable>
              <template #body="slotProps">
                <Tag :severity="slotProps.data.status === 'Pass' ? 'success' : 'danger'">
                  {{ slotProps.data.status }}
                </Tag>
              </template>
            </Column>
            <Column field="operator" header="작업자"></Column>
          </DataTable>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'

const selectedRecipe = ref(null)
const actionResult = ref(null)
const historyData = ref(null)
const isLoading = ref(false)
const dateRange = ref(null)
const chartRef = ref(null)
let chartInstance = null

// Chart option for ECharts
const chartOption = computed(() => {
  if (!historyData.value) return {}
  
  return {
    title: {
      text: '측정값 추이',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: function (params) {
        const param = params[0]
        return `${param.name}<br/>${param.seriesName}: ${param.value}`
      }
    },
    legend: {
      data: ['측정값'],
      bottom: 0
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: historyData.value.chartLabels
    },
    yAxis: {
      type: 'value',
      min: 60,
      max: 100
    },
    series: [
      {
        name: '측정값',
        type: 'line',
        stack: 'Total',
        data: historyData.value.chartValues,
        smooth: true,
        lineStyle: {
          color: '#3b82f6',
          width: 2
        },
        itemStyle: {
          color: '#3b82f6'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
              { offset: 1, color: 'rgba(59, 130, 246, 0.1)' }
            ]
          }
        }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      }
    ]
  }
})

// Initialize chart
const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value)
  }
}

// Update chart when data changes
watch(chartOption, (newOption) => {
  if (chartInstance && Object.keys(newOption).length > 0) {
    chartInstance.setOption(newOption)
  }
})

// Handle window resize
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

onMounted(() => {
  const storedRecipe = sessionStorage.getItem('selectedRecipe')
  const storedDateRange = sessionStorage.getItem('dateRange')
  
  let shouldAutoExecute = false
  
  if (storedRecipe) {
    selectedRecipe.value = storedRecipe
    sessionStorage.removeItem('selectedRecipe')
    shouldAutoExecute = true
  }
  
  if (storedDateRange) {
    try {
      const dates = JSON.parse(storedDateRange)
      dateRange.value = dates.map(dateStr => new Date(dateStr))
      sessionStorage.removeItem('dateRange')
    } catch (e) {
      console.error('Error parsing stored date range:', e)
    }
  }
  
  initChart()
  window.addEventListener('resize', handleResize)
  
  // Auto-execute if we have stored data
  if (shouldAutoExecute && dateRange.value) {
    viewMeasurementHistory()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance) {
    chartInstance.dispose()
  }
})

// Format date
const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ko-KR')
}

// Format datetime
const formatDateTime = (datetime) => {
  return new Date(datetime).toLocaleString('ko-KR')
}

// Get value class based on threshold
const getValueClass = (value) => {
  if (value >= 90) return 'text-green-600 font-semibold'
  if (value >= 80) return 'text-blue-600'
  if (value >= 70) return 'text-orange-600'
  return 'text-red-600 font-semibold'
}

// Action: View Measurement History
const viewMeasurementHistory = async () => {
  if (!selectedRecipe.value || !dateRange.value) return
  
  isLoading.value = true
  historyData.value = null
  
  actionResult.value = {
    severity: 'info',
    message: `측정 기록을 조회합니다: ${selectedRecipe.value}`
  }
  
  // Simulate API call
  setTimeout(() => {
    // Mock history data
    const mockRecords = []
    const chartLabels = []
    const chartValues = []
    
    // Generate mock data
    for (let i = 0; i < 30; i++) {
      const date = new Date()
      date.setDate(date.getDate() - i)
      const value = Math.floor(Math.random() * 30) + 70
      
      mockRecords.push({
        timestamp: date,
        equipment: `EQP_${String(Math.floor(Math.random() * 10) + 1).padStart(3, '0')}`,
        value: value,
        status: value >= 80 ? 'Pass' : 'Fail',
        operator: `OP_${String(Math.floor(Math.random() * 5) + 1).padStart(3, '0')}`
      })
      
      if (i % 3 === 0) {
        chartLabels.unshift(date.toLocaleDateString('ko-KR'))
        chartValues.unshift(value)
      }
    }
    
    historyData.value = {
      totalMeasurements: mockRecords.length,
      average: '84.5',
      max: '98.2',
      min: '71.3',
      records: mockRecords,
      chartLabels: chartLabels,
      chartValues: chartValues
    }
    
    actionResult.value = {
      severity: 'success',
      message: '측정 기록 조회가 완료되었습니다.'
    }
    
    isLoading.value = false
  }, 2000)
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>