<template>
  <div class="weekly-trend bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button icon="pi pi-arrow-left" label="디바이스 통계로 돌아가기" outlined size="large" class="mb-2" @click="goBack" />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">주별 트렌드</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          주별 데이터 변화 추이를 분석합니다
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-spin pi-spinner text-4xl text-primary mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300">데이터를 불러오는 중...</p>
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
        <p class="text-surface-600 dark:text-surface-300 text-lg">위에서 카테고리를 선택하면 차트가 표시됩니다</p>
      </div>
    </div>

    <!-- Main Chart Section -->
    <div v-if="selectedCategory && !loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-2xl font-semibold">Weekly Trend Analysis</h2>
          <p class="text-surface-600 dark:text-surface-400 mt-1">
            {{ categoryLabels[selectedCategory] }} - {{ totalSelectedProducts }} products selected
          </p>
        </div>
      </div>

      <!-- Selected Category Display -->
      <div class="mb-4">
        <span class="text-sm font-medium text-surface-600 dark:text-surface-400">Selected Category: </span>
        <span
          class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-primary-100 text-primary-800 dark:bg-primary-900/20 dark:text-primary-300">
          {{ categoryLabels[selectedCategory] }}
        </span>
      </div>

      <!-- Chart Component -->
      <WeeklyTrendChart :weekly-data="weeklyData" :selected-category="selectedCategory"
        :selected-prod-ids="selectedProdIds" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import Button from 'primevue/button'
import { deviceStatisticsQueries } from '@/services/deviceStatisticsService'
import WeeklyTrendChart from './chart/WeeklyTrendChart.vue'

const router = useRouter()

// State
const selectedCategory = ref(null) // No default selection - user must choose
const loading = computed(() => queryLoading.value)

// R3-specific stored selections from session storage
const facId = 'R3'
const selectedR3Options = ref(JSON.parse(sessionStorage.getItem('deviceStatistics_selectedR3Options') || '[]'))
const selectedProdIdsByCategory = ref(JSON.parse(sessionStorage.getItem('deviceStatistics_selectedProdIds') || '{}'))

// Categories for filtering
const categories = ref([
  { key: 'all', label: 'All' },
  { key: 'only_normal', label: 'Only Normal' },
  { key: 'mother_normal', label: 'Mother Normal' },
  { key: 'only_sample', label: 'Only Sample' }
])

// Category labels for display
const categoryLabels = {
  'all': 'All Categories',
  'only_normal': 'Only Normal',
  'mother_normal': 'Mother Normal',
  'only_sample': 'Only Sample'
}

// Use Vue Query to fetch all device data
const { data: allDeviceData, isLoading: queryLoading, error: dataError } = useQuery(
  deviceStatisticsQueries.allDeviceData()
)

// Computed property to get filtered weekly data based on selected options
const weeklyData = computed(() => {
  if (!allDeviceData.value) return {}

  // Extract date-based data, excluding special keys
  const dateKeys = Object.keys(allDeviceData.value).filter(key =>
    key.match(/^\d{4}-\d{2}-\d{2}$/) // Only date keys in YYYY-MM-DD format
  )

  console.log('[WeeklyTrendView] weeklyData computed:', {
    rawDataKeys: Object.keys(allDeviceData.value),
    filteredDateKeys: dateKeys,
    dateKeysCount: dateKeys.length
  })

  const weeklyDataObj = {}
  dateKeys.forEach(dateKey => {
    weeklyDataObj[dateKey] = allDeviceData.value[dateKey]
  })

  console.log('[WeeklyTrendView] weeklyDataObj created:', {
    weeklyDataKeys: Object.keys(weeklyDataObj),
    weeklyDataCount: Object.keys(weeklyDataObj).length
  })

  return weeklyDataObj
})

// Get selected product IDs for the selected category
const selectedProdIds = computed(() => {
  if (!selectedCategory.value) return []
  
  // For 'all' category, aggregate all selected prod IDs from all categories
  if (selectedCategory.value === 'all') {
    const allProdIds = new Set()
    selectedR3Options.value.forEach(category => {
      const prodIds = selectedProdIdsByCategory.value[category] || []
      prodIds.forEach(id => allProdIds.add(id))
    })
    return Array.from(allProdIds)
  }
  
  // For specific categories, we need to get prod IDs from the original selection
  // that match the category filter (only_normal, mother_normal, only_sample)
  const allSelectedProdIds = new Set()
  selectedR3Options.value.forEach(category => {
    const prodIds = selectedProdIdsByCategory.value[category] || []
    prodIds.forEach(id => allSelectedProdIds.add(id))
  })
  
  // Return all selected prod IDs - the filtering by category happens in the chart component
  return Array.from(allSelectedProdIds)
})

// Total count of selected products
const totalSelectedProducts = computed(() => selectedProdIds.value.length)

// Handle category selection (single selection like CurrentStatusView)
const onCategorySelect = (category) => {
  selectedCategory.value = category
  console.log('[WeeklyTrendView] Category selected:', category)
  console.log('[WeeklyTrendView] Selected R3 options:', selectedR3Options.value)
  console.log('[WeeklyTrendView] Product IDs by category:', selectedProdIdsByCategory.value)
  console.log('[WeeklyTrendView] Computed selected product IDs:', selectedProdIds.value)
  console.log('[WeeklyTrendView] Total selected products:', selectedProdIds.value.length)
}

// Go back to device statistics cd-sem page
const goBack = () => {
  router.push(`/${facId}/device-statistics/cd-sem`)
}

// Check if we have valid R3 selections
onMounted(() => {
  console.log('=== WeeklyTrendView mounted ===')
  console.log('Selected R3 options:', selectedR3Options.value)
  console.log('Selected prod IDs by category:', selectedProdIdsByCategory.value)

  if (selectedR3Options.value.length === 0) {
    console.warn('No valid R3 selections found, redirecting back')
    goBack()
    return
  }
})

// Watch for data changes and log
watch(allDeviceData, (newData) => {
  if (newData) {
    const dateKeys = Object.keys(newData).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/))
    console.log('[WeeklyTrendView] All device data received:', {
      hasData: !!newData,
      dateKeys: dateKeys,
      dateKeysCount: dateKeys.length,
      totalKeys: Object.keys(newData).length,
      allKeys: Object.keys(newData),
      firstDateSample: dateKeys.length > 0 ? {
        date: dateKeys[0],
        keys: Object.keys(newData[dateKeys[0]] || {}),
        summaryKeysCount: Object.keys(newData[dateKeys[0]] || {}).filter(key => key.includes('_summary')).length,
        rawDataStructure: newData[dateKeys[0]] // Show the actual data structure for the first date
      } : 'No date keys found'
    })

    // Print raw data for all dates to console
    console.log('[WeeklyTrendView] Raw weekly data for all dates:', newData)

    // For each date, print the nested structure and values
    dateKeys.forEach(dateKey => {
      const dateData = newData[dateKey]
      console.log(`[WeeklyTrendView] Raw data for ${dateKey}:`, {
        fullStructure: dateData,
        keys: Object.keys(dateData || {}),
        summaryKeys: Object.keys(dateData || {}).filter(key => key.includes('_summary')),
        summaryKeysWithData: Object.keys(dateData || {}).filter(key => key.includes('_summary')).map(summaryKey => ({
          key: summaryKey,
          dataLength: Array.isArray(dateData[summaryKey]) ? dateData[summaryKey].length : 'not array',
          sampleData: Array.isArray(dateData[summaryKey]) && dateData[summaryKey].length > 0 ? dateData[summaryKey][0] : 'no data'
        }))
      })
    })
  }
}, { immediate: true })

// Watch for data error
watch(dataError, (error) => {
  if (error) {
    console.error('[WeeklyTrendView] Error fetching data:', error)
  }
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>
