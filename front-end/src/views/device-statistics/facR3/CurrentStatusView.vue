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
          :selected-category="selectedCategory" :current-zoom-state="currentZoomState"
          @zoom-change="handleZoomChange" />
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
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'
import Dialog from 'primevue/dialog'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import axios from 'axios'
import CombinedChartsView from './chart/CombinedChartsView.vue'

const router = useRouter()

// State
const loading = ref(true) // Start with loading true
const chartLoading = ref(false) // Loading state for chart data preparation
const chartData = ref(null)
const latestDate = ref('')
const chartReady = ref(false) // Flag to control when charts should render

// Remove pre-selection - user must select a category first
const selectedCategory = ref(null)

const weeklyData = ref({})
const showDetailDialog = ref(false)
const selectedProdId = ref('')
const detailedRecipeData = ref([])

// Chart component reference
const combinedChartsRef = ref(null)
const summaryChartData = ref(null)

// DataZoom state management - Initialize with null to prevent early access
const currentZoomState = ref(null)

// Handle zoom change from charts
const handleZoomChange = ({ start, end }) => {
  currentZoomState.value = { start, end }
  // Note: Zoom synchronization is now handled internally within CombinedChartsView
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
const selectedR3Options = JSON.parse(sessionStorage.getItem('deviceStatistics_selectedR3Options') || '[]')
const selectedProdIdsByCategory = JSON.parse(sessionStorage.getItem('deviceStatistics_selectedProdIds') || '{}')

// Go back to device statistics main page
const goBack = () => {
  router.push(`/${facId}/device-statistics`)
}

// Prepare chart data from the weekly data
const prepareChartData = (weeklyDataInput) => {
  if (!weeklyDataInput || Object.keys(weeklyDataInput).length === 0) {
    chartData.value = null
    return
  }

  // Store the weekly data
  weeklyData.value = weeklyDataInput

  // Get the latest date
  const sortedDates = Object.keys(weeklyDataInput).sort().reverse()
  latestDate.value = sortedDates[0]

  // Don't prepare chart data yet if no category is selected
  if (!selectedCategory.value) {
    console.log('No category selected yet, waiting for user selection')
    return
  }

  const latestWeekData = weeklyDataInput[latestDate.value]

  console.log('Selected category:', selectedCategory.value)
  console.log('Latest week data keys:', Object.keys(latestWeekData))
  console.log('Latest week rcp_info keys:', latestWeekData.rcp_info ? Object.keys(latestWeekData.rcp_info) : 'no rcp_info')

  // Prepare chart data based on selected category
  prepareChartDataForCategory(latestWeekData, selectedCategory.value)
}

// Prepare chart data for specific category
const prepareChartDataForCategory = (latestWeekData, category) => {
  console.log('prepareChartDataForCategory called with category:', category)

  if (!latestWeekData || !latestWeekData.rcp_info) {
    console.log('No latestWeekData or rcp_info')
    chartData.value = null
    return
  }

  // Get the appropriate recipe info based on category with fallback
  const recipeKey = category === 'all' ? 'all_rcp_info' :
    category === 'only_normal' ? 'only_normal_rcp_info' :
      category === 'mother_normal' ? 'mother_normal_rcp_info' :
        'only_sample_rcp_info'

  console.log('Using recipe key:', recipeKey)

  let recipeData = latestWeekData.rcp_info[recipeKey]
  console.log('Recipe data length:', recipeData ? recipeData.length : 'null')

  // Fallback logic: if category-specific data not found, try other available data
  if (!recipeData || recipeData.length === 0) {
    console.log('No recipe data found for key:', recipeKey, '- looking for fallback data')
    const availableKeys = Object.keys(latestWeekData.rcp_info)
    console.log('Available rcp_info keys:', availableKeys)

    // Try to find any available recipe data
    for (const key of availableKeys) {
      if (latestWeekData.rcp_info[key] && latestWeekData.rcp_info[key].length > 0) {
        recipeData = latestWeekData.rcp_info[key]
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
  console.log('Available summary_by_category keys:', latestWeekData.summary_by_category ? Object.keys(latestWeekData.summary_by_category) : 'no summary_by_category')

  let summaryData = null

  // Get summary data with fallback logic
  if (latestWeekData.summary_by_category &&
    latestWeekData.summary_by_category[summaryKey] &&
    latestWeekData.summary_by_category[summaryKey].length > 0) {
    summaryData = latestWeekData.summary_by_category[summaryKey]
    console.log('Using category-specific summary data, length:', summaryData.length)
  } else if (latestWeekData.summary && latestWeekData.summary.length > 0) {
    // Fallback to general summary if category-specific not available
    summaryData = latestWeekData.summary
    console.log('Using general summary data, length:', summaryData.length)
  } else {
    // Try to find any available summary data
    console.log('No summary data found for key:', summaryKey, '- looking for fallback summary data')
    if (latestWeekData.summary_by_category) {
      const availableSummaryKeys = Object.keys(latestWeekData.summary_by_category)
      console.log('Available summary_by_category keys:', availableSummaryKeys)

      for (const key of availableSummaryKeys) {
        if (latestWeekData.summary_by_category[key] && latestWeekData.summary_by_category[key].length > 0) {
          summaryData = latestWeekData.summary_by_category[key]
          console.log('Using fallback summary data from key:', key, 'length:', summaryData.length)
          break
        }
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

  // Sort summary data by para_all from highest to lowest
  const sortedSummary = [...summaryData].sort((a, b) => (b.para_all || 0) - (a.para_all || 0))

  // Extract data for parameter distribution chart from summary
  const prodIds = sortedSummary.map(item => String(item.prod_id || ''))
  const para5Data = sortedSummary.map(item => Number(item.para_5) || 0)
  const para9Data = sortedSummary.map(item => Number(item.para_9) || 0)
  const para13Data = sortedSummary.map(item => Number(item.para_13) || 0)
  const para16Data = sortedSummary.map(item => Number(item.para_16) || 0)

  // Validate extracted data
  if (prodIds.length === 0 || prodIds.some(id => !id)) {
    console.warn('No valid product IDs found in summary data')
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
  summaryChartData.value = {
    prodIds: summaryData.map(item => String(item.prod_id || '')),
    paraAll: summaryData.map(item => Number(item.para_all) || 0),
    availRecipe: summaryData.map(item => Number(item.avail_recipe) || 0),
    ctnDesc: summaryData.map(item => String(item.ctn_desc || `Container for ${item.prod_id || 'Unknown'}`))
  }

  console.log('Summary chart data prepared:', {
    prodIdsLength: summaryChartData.value.prodIds.length,
    paraAllLength: summaryChartData.value.paraAll.length,
    availRecipeLength: summaryChartData.value.availRecipe.length
  })
}

// Fetch R3-specific data
const fetchData = async () => {
  loading.value = true
  console.log('=== Starting fetchData ===')
  console.log('Selected R3 options:', selectedR3Options)
  console.log('Selected prod IDs by category:', selectedProdIdsByCategory)

  try {
    // R3-specific data fetching with selected options and prod_ids
    const filteredOptions = selectedR3Options
      .filter(option => selectedProdIdsByCategory[option]?.length > 0)

    console.log('Filtered options to fetch:', filteredOptions)

    if (filteredOptions.length === 0) {
      console.warn('No valid options to fetch data for')
      chartData.value = null
      summaryChartData.value = null
      loading.value = false
      return
    }

    const promises = filteredOptions.map(option =>
      axios.get(`/api/device-statistics/device-data`, {
        params: {
          fac_id: facId,
          option,
          'prod_ids[]': selectedProdIdsByCategory[option]
        },
        paramsSerializer: params => {
          // Custom serializer to handle array parameters
          const searchParams = new URLSearchParams()
          searchParams.append('fac_id', params.fac_id)
          searchParams.append('option', params.option)
          params['prod_ids[]'].forEach(id => searchParams.append('prod_ids[]', id))
          return searchParams.toString()
        }
      })
    )

    const responses = await Promise.all(promises)
    console.log('API responses received:', responses.length)

    // Log the raw responses for debugging
    responses.forEach((response, index) => {
      console.log(`Response ${index}:`, {
        status: response.status,
        hasWeeklyData: !!response.data?.weekly_data,
        weeklyDataKeys: response.data?.weekly_data ? Object.keys(response.data.weekly_data) : []
      })
    })

    // Combine weekly data
    const combinedWeeklyData = {}

    responses.forEach((response) => {
      if (response.data.weekly_data) {
        Object.entries(response.data.weekly_data).forEach(([weekDate, weekData]) => {
          if (!combinedWeeklyData[weekDate]) {
            combinedWeeklyData[weekDate] = {
              rcp_info: {
                all_rcp_info: [],
                only_normal_rcp_info: [],
                mother_normal_rcp_info: [],
                only_sample_rcp_info: []
              },
              summary: [],
              summary_by_category: {
                all_summary: [],
                only_normal_summary: [],
                mother_normal_summary: [],
                only_sample_summary: []
              },
              all_recipe_list: []
            }
          }

          // Combine rcp_info data
          if (weekData.rcp_info) {
            Object.keys(weekData.rcp_info).forEach(key => {
              if (weekData.rcp_info[key] && Array.isArray(weekData.rcp_info[key])) {
                // Initialize the array if it doesn't exist
                if (!combinedWeeklyData[weekDate].rcp_info[key]) {
                  combinedWeeklyData[weekDate].rcp_info[key] = []
                }
                combinedWeeklyData[weekDate].rcp_info[key].push(...weekData.rcp_info[key])
              }
            })
          }

          // Combine summary data
          if (weekData.summary && Array.isArray(weekData.summary)) {
            combinedWeeklyData[weekDate].summary.push(...weekData.summary)
          }

          // Combine summary_by_category data
          if (weekData.summary_by_category) {

            // Ensure summary_by_category exists in combined data
            if (!combinedWeeklyData[weekDate].summary_by_category) {
              combinedWeeklyData[weekDate].summary_by_category = {
                all_summary: [],
                only_normal_summary: [],
                mother_normal_summary: [],
                only_sample_summary: []
              }
            }

            Object.keys(weekData.summary_by_category).forEach(categoryKey => {
              if (weekData.summary_by_category[categoryKey] && Array.isArray(weekData.summary_by_category[categoryKey])) {
                // Initialize the category array if it doesn't exist
                if (!combinedWeeklyData[weekDate].summary_by_category[categoryKey]) {
                  combinedWeeklyData[weekDate].summary_by_category[categoryKey] = []
                }
                combinedWeeklyData[weekDate].summary_by_category[categoryKey].push(...weekData.summary_by_category[categoryKey])
              }
            })
          }

          // Combine all_recipe_list data
          if (weekData.all_recipe_list && Array.isArray(weekData.all_recipe_list)) {
            combinedWeeklyData[weekDate].all_recipe_list.push(...weekData.all_recipe_list)
          }
        })
      }
    })


    // Data combination completed
    console.log('Combined weekly data:', {
      hasData: Object.keys(combinedWeeklyData).length > 0,
      dates: Object.keys(combinedWeeklyData),
      firstDateStructure: Object.keys(combinedWeeklyData).length > 0 ?
        Object.keys(combinedWeeklyData[Object.keys(combinedWeeklyData)[0]]) : []
    })

    // Prepare chart data
    prepareChartData(combinedWeeklyData)
  } catch (error) {
    console.error('Error fetching R3 device data:', error)
    chartData.value = null
    summaryChartData.value = null
  } finally {
    loading.value = false
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

    if (weeklyData.value && Object.keys(weeklyData.value).length > 0) {
      // Small delay to ensure clean state transition
      await nextTick()

      const sortedDates = Object.keys(weeklyData.value).sort().reverse()
      const latestWeekData = weeklyData.value[sortedDates[0]]

      console.log('Preparing chart data for category:', category)

      // Prepare chart data
      prepareChartDataForCategory(latestWeekData, selectedCategory.value)

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

onMounted(() => {
  console.log('=== Component mounted ===')
  console.log('Loading state:', loading.value)
  console.log('Component mounted - no category selected yet')

  // Check if we have valid R3 selections
  if (selectedR3Options.length === 0) {
    console.warn('No valid R3 selections found, redirecting back')
    // No valid R3 selections, redirect back
    goBack()
    return
  }

  fetchData()
})

onUnmounted(() => {
  // Component cleanup if needed
})


</script>

<style scoped>
/* Page-specific styles if needed */
</style>
