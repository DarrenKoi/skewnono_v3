<template>
  <div class="weekly-trend bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button icon="pi pi-arrow-left" label="디바이스 통계로 돌아가기" outlined size="large" class="mb-2" @click="goBack" />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">주간 추이</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          {{ facId }} 시설의 주별 데이터 변화 추이를 분석합니다
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-spin pi-spinner text-4xl text-primary"></i>
        <p class="mt-4 text-surface-600 dark:text-surface-300">데이터를 불러오는 중...</p>
      </div>
    </div>

    <!-- Category Selection Section -->
    <div v-if="!loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="mb-4">
        <h2 class="text-xl font-semibold mb-2">카테고리 선택</h2>
        <div class="flex flex-wrap gap-2">
          <Button v-for="category in categories" :key="category.key" @click="onCategorySelect(category.key)"
            :label="category.label" :severity="selectedCategory === category.key ? 'primary' : 'secondary'"
            :outlined="selectedCategory !== category.key" size="small" class="px-4 py-2" />
        </div>
      </div>
    </div>

    <!-- No Category Selected Message -->
    <div v-if="!selectedCategory && !loading && weeklyData && Object.keys(weeklyData).length > 0"
      class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-chart-line text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300 text-lg">위에서 카테고리를 선택하면 주간 추이가 표시됩니다</p>
      </div>
    </div>

    <!-- Main Chart Section -->
    <div v-if="selectedCategory && !loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <!-- Chart Component -->
      <WeeklyTrendChart 
        :weekly-data="weeklyData" 
        :selected-category="selectedCategory"
        :selected-prod-ids="selectedProducts" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'
import { deviceStatisticsQueries } from '@/services/deviceStatisticsService'
import { useQuery } from '@tanstack/vue-query'
import WeeklyTrendChart from '../facR3/chart/WeeklyTrendChart.vue'

const router = useRouter()
const route = useRoute()

// Get facility ID from route params
const facId = computed(() => route.params.fac_id || 'M1')

// State
const selectedCategory = ref(null)
const selectedProducts = ref([])

// Use Vue Query to fetch device data for this facility
const { data: allDeviceData, isLoading: loading } = useQuery(deviceStatisticsQueries.allDeviceData(facId.value))

// Categories for filtering
const categories = ref([
  { key: 'all', label: '전체' },
  { key: 'only_normal', label: '일반만' },
  { key: 'mother_normal', label: '마더 일반' },
  { key: 'only_sample', label: '샘플만' }
])

// Computed property to get weekly data from the device data
const weeklyData = computed(() => {
  if (!allDeviceData.value) return {}

  // Extract date-based data, excluding special keys
  const dateKeys = Object.keys(allDeviceData.value).filter(key =>
    key.match(/^\d{4}-\d{2}-\d{2}$/) // Only date keys in YYYY-MM-DD format
  )

  const weeklyDataObj = {}
  dateKeys.forEach(dateKey => {
    weeklyDataObj[dateKey] = allDeviceData.value[dateKey]
  })

  return weeklyDataObj
})

// Get facility selections from sessionStorage
const getStoredSelections = () => {
  const storedProducts = sessionStorage.getItem(`deviceStatistics_selectedProducts_${facId.value}`)
  
  if (storedProducts) {
    selectedProducts.value = JSON.parse(storedProducts)
    return true
  }
  return false
}

// Go back to device statistics
const goBack = () => {
  router.push(`/${facId.value}/device-statistics/cd-sem`)
}

// Handle category selection
const onCategorySelect = (category) => {
  selectedCategory.value = category
  console.log('[WeeklyTrendView] Category selected:', category)
  console.log('[WeeklyTrendView] Selected products:', selectedProducts.value)
  console.log('[WeeklyTrendView] Weekly data keys:', Object.keys(weeklyData.value))
}

// Watch for Vue Query data changes
watch(allDeviceData, (newData) => {
  if (newData) {
    console.log('[FacOthers WeeklyTrend] Device data loaded:', newData)
    
    // If no stored selections, auto-select all products
    if (!selectedProducts.value.length && newData.available_products) {
      selectedProducts.value = [...newData.available_products]
    }
  }
})

onMounted(() => {
  console.log('[FacOthers WeeklyTrend] Component mounted')
  
  // Try to get stored selections first
  if (!getStoredSelections()) {
    console.log('No stored selections found, will use fresh data when loaded')
  }
  
  // If no valid selections, redirect back
  if (!selectedProducts.value.length && !allDeviceData.value) {
    console.warn('No product selections found, redirecting back')
    goBack()
  }
})
</script>

<style scoped>
/* Component-specific styles if needed */
</style>