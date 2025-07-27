<template>
  <div class="current-status bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button icon="pi pi-arrow-left" label="디바이스 통계로 돌아가기" outlined size="large" class="mb-2" @click="goBack" />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">현재 상황</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          최신 데이터 기준 파라미터 분포를 확인합니다
        </div>
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

    <!-- Loading State -->
    <div v-if="loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <ProgressSpinner />
        <p class="mt-4 text-surface-600 dark:text-surface-300">데이터를 불러오는 중...</p>
      </div>
    </div>

    <!-- No Category Selected Message -->
    <div v-if="!selectedCategory && !loading && weeklyData && Object.keys(weeklyData).length > 0"
      class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-chart-bar text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300 text-lg">위에서 카테고리를 선택하면 차트가 표시됩니다</p>
      </div>
    </div>

    <!-- Chart Loading Section -->
    <div v-if="selectedCategory && chartLoading && !loading"
      class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <ProgressSpinner />
        <p class="mt-4 text-surface-600 dark:text-surface-300">차트 데이터를 준비하는 중...</p>
      </div>
    </div>

    <!-- No Chart Data State -->
    <div
      v-if="selectedCategory && !chartLoading && !loading && (!chartData || !chartData.prodIds || chartData.prodIds.length === 0)"
      class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-inbox text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300">선택한 카테고리에 대한 데이터가 없습니다</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div v-if="selectedCategory && !chartLoading && !loading && chartReady"
      class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="mb-6">
        <h2 class="text-2xl font-semibold">Parameter Distribution - {{ categoryLabels[selectedCategory] }}</h2>
        <p class="text-surface-600 dark:text-surface-400 mt-1">
          {{ latestDate ? `기준일: ${latestDate}` : '' }}
        </p>
      </div>

      <!-- Chart Display -->
      <div>
        <!-- Combined Charts Component -->
        <CombinedChartsView ref="combinedChartsRef" :chart-data="chartData" :summary-chart-data="summaryChartData"
          :selected-category="selectedCategory" :raw-latest-data="rawLatestData"
          @product-selected="handleProductSelected" />
        <!-- Detailed Recipe Info Dialog -->
        <Dialog v-model:visible="showDetailDialog"
          :header="`${selectedProdId} - 상세 레시피 정보 (${categoryLabels[selectedCategory]})`" :style="{ width: '90vw' }"
          maximizable modal>
          <div v-if="detailedRecipeData.length > 0">
            <DataTable :value="detailedRecipeData" stripedRows :paginator="true" :rows="10">
              <Column field="prod_id" header="Product ID"></Column>
              <Column field="recipe_id" header="Recipe ID"></Column>
              <Column field="oper_desc" header="Operation"></Column>
              <Column field="para_5" header="Para 5"></Column>
              <Column field="para_9" header="Para 9"></Column>
              <Column field="para_13" header="Para 13"></Column>
              <Column field="para_16" header="Para 16"></Column>
              <Column field="para_all" header="Total"></Column>
              <Column field="skip_yn" header="Skip"></Column>
            </DataTable>
          </div>
          <div v-else class="text-center py-8">
            <i class="pi pi-info-circle text-4xl text-surface-400 mb-4"></i>
            <p class="text-surface-600">해당 제품의 상세 레시피 정보가 없습니다.</p>
          </div>
        </Dialog>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import Dialog from 'primevue/dialog'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import { useQuery } from '@tanstack/vue-query'
import { deviceStatisticsQueries } from '@/services/deviceStatisticsService'
import CombinedChartsView from './chart/CombinedChartsView.vue'

const router = useRouter()

// State
const loading = computed(() => queryLoading.value) // Use Vue Query loading state
const chartLoading = ref(false) // Loading state for chart data preparation
const chartData = ref(null)
const latestDate = ref('')
const chartReady = ref(false) // Flag to control when charts should render

// Remove pre-selection - user must select a category first
const selectedCategory = ref(null)

// Removed - now using computed property
const showDetailDialog = ref(false)
const selectedProdId = ref('')
const detailedRecipeData = ref([])

// Chart component reference
const combinedChartsRef = ref(null)
const summaryChartData = ref(null)

// DataZoom state management - Initialize with null to prevent early access
const currentZoomState = ref(null)

// Handle product selection from chart
const handleProductSelected = (productData) => {
  console.log('Product selected from chart:', productData);
  // The table is now displayed within the chart component itself
  // No additional handling needed here unless you want to do something else
}

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

// R3-specific stored selections from session storage
const facId = 'R3'
const selectedR3Options = ref(JSON.parse(sessionStorage.getItem('deviceStatistics_selectedR3Options') || '[]'))
const selectedProdIdsByCategory = ref(JSON.parse(sessionStorage.getItem('deviceStatistics_selectedProdIds') || '{}'))

// Go back to device statistics cd-sem page
const goBack = () => {
  router.push(`/${facId}/device-statistics/cd-sem`)
}


// Prepare chart data for specific category
const prepareChartDataForCategory = (latestWeekData, category) => {
  console.log('=== prepareChartDataForCategory called ===')
  console.log('Category:', category)
  console.log('latestWeekData exists:', !!latestWeekData)
  console.log('latestWeekData keys:', latestWeekData ? Object.keys(latestWeekData) : 'null')
  console.log('latestWeekData full structure:', latestWeekData)

  if (!latestWeekData) {
    console.log('ERROR: No latestWeekData provided')
    chartData.value = null
    return
  }

  // Check if the data structure has the expected keys
  if (!latestWeekData.all_rcp_info && !latestWeekData.all_summary) {
    console.log('ERROR: No recipe or summary data found in latestWeekData')
    console.log('Available keys in latestWeekData:', Object.keys(latestWeekData))
    chartData.value = null
    return
  }

  // Get all selected prod_ids from sessionStorage
  const selectedProdIdsByCategory = JSON.parse(sessionStorage.getItem('deviceStatistics_selectedProdIds') || '{}')
  const selectedProdIds = new Set()
  
  // Collect all selected prod_ids across all categories
  Object.values(selectedProdIdsByCategory).forEach(prodIds => {
    if (Array.isArray(prodIds)) {
      prodIds.forEach(id => selectedProdIds.add(id))
    }
  })
  
  console.log('Selected prod_ids for filtering:', Array.from(selectedProdIds))

  // Get the appropriate recipe info based on category
  const recipeKey = category === 'all' ? 'all_rcp_info' :
    category === 'only_normal' ? 'only_normal_rcp_info' :
      category === 'mother_normal' ? 'mother_normal_rcp_info' :
        'only_sample_rcp_info'

  console.log('Using recipe key:', recipeKey)

  let recipeData = latestWeekData[recipeKey]
  console.log('Recipe data length:', recipeData ? recipeData.length : 'null')

  // Fallback logic: if category-specific data not found, try other available data
  if (!recipeData || recipeData.length === 0) {
    console.log('No recipe data found for key:', recipeKey, '- looking for fallback data')
    const availableKeys = Object.keys(latestWeekData).filter(key => key.includes('_rcp_info'))
    console.log('Available recipe info keys:', availableKeys)

    // Try to find any available recipe data
    for (const key of availableKeys) {
      if (latestWeekData[key] && latestWeekData[key].length > 0) {
        recipeData = latestWeekData[key]
        console.log('Using fallback recipe data from key:', key, 'length:', recipeData.length)
        break
      }
    }

    if (!recipeData || recipeData.length === 0) {
      console.log('No recipe data found even with fallback')
      chartData.value = null
      return
    }
  }


  // Prepare summary chart data based on category
  const summaryKey = category === 'all' ? 'all_summary' :
    category === 'only_normal' ? 'only_normal_summary' :
      category === 'mother_normal' ? 'mother_normal_summary' :
        'only_sample_summary'

  console.log('Using summary key:', summaryKey)
  console.log('Available summary keys in latestWeekData:', Object.keys(latestWeekData).filter(key => key.includes('_summary')))

  let summaryData = null

  // Get summary data with fallback logic
  if (latestWeekData[summaryKey] && latestWeekData[summaryKey].length > 0) {
    summaryData = latestWeekData[summaryKey]
    console.log('Using category-specific summary data, length:', summaryData.length)
  } else {
    // Try to find any available summary data
    console.log('No summary data found for key:', summaryKey, '- looking for fallback summary data')
    const availableSummaryKeys = Object.keys(latestWeekData).filter(key => key.includes('_summary'))
    console.log('Available summary keys:', availableSummaryKeys)

    for (const key of availableSummaryKeys) {
      if (latestWeekData[key] && latestWeekData[key].length > 0) {
        summaryData = latestWeekData[key]
        console.log('Using fallback summary data from key:', key, 'length:', summaryData.length)
        break
      }
    }
  }

  if (!summaryData || summaryData.length === 0) {
    console.log('No summary data found even with fallback')
    chartData.value = null
    summaryChartData.value = null
    currentZoomState.value = null
    return
  }

  // Filter summary data to only include selected prod_ids
  const filteredSummary = summaryData.filter(item => selectedProdIds.has(item.prod_id))
  
  // Sort filtered summary data by para_all from highest to lowest
  const sortedSummary = [...filteredSummary].sort((a, b) => (b.para_all || 0) - (a.para_all || 0))
  
  console.log('Filtered summary data count:', filteredSummary.length, 'from original:', summaryData.length)

  // Extract data for parameter distribution chart from recipe data using percentage values
  // Group by prod_id and calculate averages of percentages
  const prodIdMap = new Map()

  // Filter recipe data to only include selected prod_ids
  const filteredRecipeData = recipeData.filter(item => selectedProdIds.has(item.prod_id))
  console.log('Filtered recipe data count:', filteredRecipeData.length, 'from original:', recipeData.length)
  
  filteredRecipeData.forEach(item => {
    const prodId = item.prod_id
    if (!prodIdMap.has(prodId)) {
      prodIdMap.set(prodId, {
        para_5_percent: [],
        para_9_percent: [],
        para_13_percent: [],
        para_16_percent: []
      })
    }

    const data = prodIdMap.get(prodId)
    data.para_5_percent.push(Number(item.para_5_percent) || 0)
    data.para_9_percent.push(Number(item.para_9_percent) || 0)
    data.para_13_percent.push(Number(item.para_13_percent) || 0)
    data.para_16_percent.push(Number(item.para_16_percent) || 0)
  })

  // Calculate averages for each prod_id
  const prodIds = Array.from(prodIdMap.keys())
  const para5Data = prodIds.map(prodId => {
    const percentages = prodIdMap.get(prodId).para_5_percent
    return percentages.reduce((sum, val) => sum + val, 0) / percentages.length
  })
  const para9Data = prodIds.map(prodId => {
    const percentages = prodIdMap.get(prodId).para_9_percent
    return percentages.reduce((sum, val) => sum + val, 0) / percentages.length
  })
  const para13Data = prodIds.map(prodId => {
    const percentages = prodIdMap.get(prodId).para_13_percent
    return percentages.reduce((sum, val) => sum + val, 0) / percentages.length
  })
  const para16Data = prodIds.map(prodId => {
    const percentages = prodIdMap.get(prodId).para_16_percent
    return percentages.reduce((sum, val) => sum + val, 0) / percentages.length
  })

  // Validate extracted data
  if (prodIds.length === 0 || prodIds.some(id => !id)) {
    console.warn('No valid product IDs found after filtering')
    chartData.value = null
    summaryChartData.value = null
    currentZoomState.value = null
    return
  }

  // Ensure all arrays have the same length
  const expectedLength = prodIds.length
  if (para5Data.length !== expectedLength || para9Data.length !== expectedLength ||
    para13Data.length !== expectedLength || para16Data.length !== expectedLength) {
    console.warn('Data arrays have mismatched lengths')
    chartData.value = null
    summaryChartData.value = null
    currentZoomState.value = null
    return
  }

  chartData.value = {
    prodIds,
    para5Data,
    para9Data,
    para13Data,
    para16Data
  }

  console.log('Chart data set:', {
    prodIdsLength: prodIds.length,
    para5Length: para5Data.length,
    para9Length: para9Data.length,
    para13Length: para13Data.length,
    para16Length: para16Data.length
  })

  // Reset zoom state when data changes - show first 5 x-axis points
  const totalItems = prodIds.length
  let endPercentage = 100

  if (totalItems > 5) {
    endPercentage = Math.max(10, Math.min(100, (5 / totalItems) * 100)) // Ensure minimum 10% visibility
  }

  // Ensure zoom state is always a valid object with proper numbers
  currentZoomState.value = {
    start: 0,
    end: Math.round(endPercentage * 100) / 100 // Round to 2 decimal places
  }

  console.log('Zoom state set:', currentZoomState.value, 'for', totalItems, 'items')

  // Validate zoom state
  if (typeof currentZoomState.value.start !== 'number' ||
    typeof currentZoomState.value.end !== 'number' ||
    isNaN(currentZoomState.value.start) ||
    isNaN(currentZoomState.value.end)) {
    console.error('Invalid zoom state created:', currentZoomState.value)
    currentZoomState.value = { start: 0, end: 100 }
  }

  // Prepare summary chart data using the same sorted summary data
  prepareSummaryChartData(sortedSummary)

  console.log('Chart preparation completed. chartData is null?', chartData.value === null)
}

// Prepare summary chart data
const prepareSummaryChartData = (summaryData) => {
  if (!summaryData || summaryData.length === 0) {
    summaryChartData.value = null
    return
  }

  // Data is already sorted, just use it directly with proper type conversion
  // Bottom chart will have dual Y-axes: availRecipe (left) and paraAll (right)
  summaryChartData.value = {
    prodIds: summaryData.map(item => String(item.prod_id || '')),
    availRecipe: summaryData.map(item => Number(item.avail_recipe) || 0), // Left Y-axis
    paraAll: summaryData.map(item => Number(item.para_all) || 0), // Right Y-axis (para_all)
    ctnDesc: summaryData.map(item => String(item.ctn_desc || `Container for ${item.prod_id || 'Unknown'}`))
  }

  console.log('Summary chart data prepared:', {
    prodIdsLength: summaryChartData.value.prodIds.length,
    availRecipeLength: summaryChartData.value.availRecipe.length,
    paraAllLength: summaryChartData.value.paraAll.length
  })
}

// Use Vue Query to fetch all device data
const { data: allDeviceData, isLoading: queryLoading } = useQuery(deviceStatisticsQueries.allDeviceData())

// Computed property to get filtered weekly data based on selected options
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

// Store raw latest data for category-based chart preparation
let rawLatestData = null

// Process data when selected options change - Simplified for CurrentStatusView
const processDeviceData = () => {
  if (!weeklyData.value || Object.keys(weeklyData.value).length === 0) {
    console.log('=== processDeviceData early return ===')
    console.log('weeklyData.value exists:', !!weeklyData.value)
    console.log('weeklyData.value keys length:', weeklyData.value ? Object.keys(weeklyData.value).length : 0)
    return
  }

  console.log('=== Processing device data ===')
  console.log('Weekly data keys:', Object.keys(weeklyData.value))

  try {
    // Get the latest date's data (CurrentStatusView only needs latest data)
    const sortedDates = Object.keys(weeklyData.value).sort().reverse()
    const latestDateStr = sortedDates[0]
    rawLatestData = weeklyData.value[latestDateStr]

    console.log('Latest date:', latestDateStr)
    console.log('Raw latest data keys:', rawLatestData ? Object.keys(rawLatestData) : 'null')
    console.log('Raw latest data sample:', rawLatestData)

    if (!rawLatestData) {
      console.error('No data found for latest date:', latestDateStr)
      return
    }

    // Store the latest date
    latestDate.value = latestDateStr

    console.log('Data processing completed, ready for category selection')
  } catch (error) {
    console.error('Error processing R3 device data:', error)
    chartData.value = null
    summaryChartData.value = null
  }
}

// Handle category selection
const onCategorySelect = async (category) => {
  console.log('=== Category selection started ===', category)

  try {
    // Set loading state for chart
    chartLoading.value = true

    // If we're switching categories (not first selection), clear chart ready state
    if (selectedCategory.value !== null) {
      chartReady.value = false
      // Give charts time to unmount gracefully
      await new Promise(resolve => setTimeout(resolve, 100))
    }

    // Clear existing chart data first to prevent stale data issues
    chartData.value = null
    summaryChartData.value = null
    currentZoomState.value = null

    // Then set the selected category
    selectedCategory.value = category

    if (rawLatestData) {
      // Small delay to ensure clean state transition
      await nextTick()

      console.log('=== Category Selection Data Debug ===')
      console.log('Preparing chart data for category:', category)
      console.log('Raw latest data keys:', Object.keys(rawLatestData))
      console.log('Raw latest data counts:', {
        all_rcp_info: rawLatestData.all_rcp_info?.length || 0,
        only_normal_rcp_info: rawLatestData.only_normal_rcp_info?.length || 0,
        mother_normal_rcp_info: rawLatestData.mother_normal_rcp_info?.length || 0,
        only_sample_rcp_info: rawLatestData.only_sample_rcp_info?.length || 0,
        all_summary: rawLatestData.all_summary?.length || 0,
        only_normal_summary: rawLatestData.only_normal_summary?.length || 0,
        mother_normal_summary: rawLatestData.mother_normal_summary?.length || 0,
        only_sample_summary: rawLatestData.only_sample_summary?.length || 0
      })

      // Prepare chart data using raw data directly
      prepareChartDataForCategory(rawLatestData, selectedCategory.value)

      // Wait for data to be fully prepared
      await nextTick()

      // Additional delay to ensure data is stable
      await new Promise(resolve => setTimeout(resolve, 50))

      // Validate that all required data is ready before marking as ready
      if (chartData.value &&
        chartData.value.prodIds &&
        chartData.value.prodIds.length > 0 &&
        currentZoomState.value &&
        typeof currentZoomState.value.start === 'number' &&
        typeof currentZoomState.value.end === 'number') {
        chartReady.value = true
        console.log('Chart marked as ready')
      } else {
        console.log('Chart data validation failed:', {
          hasChartData: !!chartData.value,
          hasProdIds: chartData.value?.prodIds?.length > 0,
          hasZoomState: !!currentZoomState.value,
          zoomState: currentZoomState.value
        })
      }
    }
  } catch (error) {
    console.error('Error in category selection:', error)
    chartReady.value = false
  } finally {
    // Clear loading state
    chartLoading.value = false
  }
}

// Watch for data changes and process when loaded
watch(allDeviceData, (newData) => {
  if (newData) {
    console.log('=== Device data loaded ===')
    console.log('All device data keys:', Object.keys(newData))
    console.log('All device data structure:', {
      totalKeys: Object.keys(newData).length,
      hasWorkingDevices: !!newData.working_devices,
      hasDeviceOptions: !!newData.device_options,
      dateKeys: Object.keys(newData).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/)),
      firstDateSample: (() => {
        const dateKeys = Object.keys(newData).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/))
        if (dateKeys.length > 0) {
          const firstDate = dateKeys[0]
          return {
            date: firstDate,
            keys: Object.keys(newData[firstDate] || {}),
            sampleData: newData[firstDate]
          }
        }
        return null
      })()
    })
    processDeviceData()
  }
})

// Watch for selected options changes
watch([selectedR3Options, selectedProdIdsByCategory], () => {
  if (allDeviceData.value) {
    processDeviceData()
  }
}, { deep: true })

onMounted(() => {
  console.log('=== Component mounted ===')
  console.log('Loading state:', loading.value)
  console.log('Component mounted - no category selected yet')

  // Check if we have valid R3 selections
  if (selectedR3Options.value.length === 0) {
    console.warn('No valid R3 selections found, redirecting back')
    // No valid R3 selections, redirect back
    goBack()
    return
  }

  // Process data if already loaded
  if (allDeviceData.value) {
    processDeviceData()
  }
})

onUnmounted(() => {
  // Component cleanup if needed
})


</script>

<style scoped>
/* Page-specific styles if needed */
</style>
