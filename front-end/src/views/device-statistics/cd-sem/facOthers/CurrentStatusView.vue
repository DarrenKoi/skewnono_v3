<template>
  <div class="current-status bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button icon="pi pi-arrow-left" label="Back to Device Statistics" outlined size="large" class="mb-2" @click="goBack" />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Current Status</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          View parameter distribution based on latest data for facility {{ facId }}
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-spin pi-spinner text-4xl text-primary"></i>
        <p class="mt-4 text-surface-600 dark:text-surface-300">Loading data...</p>
      </div>
    </div>

    <!-- Category Selection Section -->
    <div v-if="!loading" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="mb-4">
        <h2 class="text-xl font-semibold mb-2">Category Selection</h2>
        <div class="flex flex-wrap gap-2">
          <Button v-for="category in categories" :key="category.key" @click="onCategorySelect(category.key)"
            :label="category.label" :severity="selectedCategory === category.key ? 'primary' : 'secondary'"
            :outlined="selectedCategory !== category.key" size="small" class="px-4 py-2" />
        </div>
      </div>
    </div>

    <!-- No Category Selected Message -->
    <div v-if="!selectedCategory && !loading && statisticsData"
      class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="text-center py-12">
        <i class="pi pi-chart-bar text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300 text-lg">Select a category above to view charts</p>
      </div>
    </div>

    <!-- Charts Section -->
    <div v-if="selectedCategory && !loading && chartReady"
      class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="mb-6">
        <h2 class="text-2xl font-semibold">Parameter Distribution - {{ categoryLabels[selectedCategory] }}</h2>
        <p class="text-surface-600 dark:text-surface-400 mt-1">
          {{ latestDate ? `Date: ${latestDate}` : '' }}
        </p>
      </div>

      <!-- Chart Display -->
      <div>
        <CombinedChartsView 
          :chart-data="chartData" 
          :summary-chart-data="summaryChartData"
          :selected-category="selectedCategory" 
          :raw-latest-data="rawLatestData"
          @product-selected="handleProductSelected" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'
import { deviceStatisticsQueries } from '@/services/deviceStatisticsService'
import { useQuery } from '@tanstack/vue-query'
import CombinedChartsView from '../facR3/chart/CombinedChartsView.vue'

const router = useRouter()
const route = useRoute()

// Get facility ID from route params
const facId = computed(() => route.params.fac_id || 'M1')

// State
const selectedCategory = ref(null)
const chartData = ref(null)
const summaryChartData = ref(null)
const rawLatestData = ref(null)
const chartReady = ref(false)
const statisticsData = ref(null)
const selectedProducts = ref([])
const latestDate = ref('')

// Use Vue Query to fetch device data for this facility
const { data: allDeviceData, isLoading: loading } = useQuery(deviceStatisticsQueries.allDeviceData(facId.value))

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

// Get facility selections from sessionStorage
const getStoredSelections = () => {
  const storedProducts = sessionStorage.getItem(`deviceStatistics_selectedProducts_${facId.value}`)
  const storedData = sessionStorage.getItem(`deviceStatistics_filteredData_${facId.value}`)
  
  if (storedProducts && storedData) {
    selectedProducts.value = JSON.parse(storedProducts)
    statisticsData.value = JSON.parse(storedData)
    
    // Get latest date
    const dateKeys = Object.keys(statisticsData.value).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/))
    if (dateKeys.length > 0) {
      latestDate.value = dateKeys.sort((a, b) => new Date(b) - new Date(a))[0]
    }
    
    return true
  }
  return false
}

// Go back to device statistics
const goBack = () => {
  router.push(`/${facId.value}/device-statistics/cd-sem`)
}

// Handle product selection from chart
const handleProductSelected = (productData) => {
  console.log('Product selected from chart:', productData)
}

// Prepare chart data for specific category
const prepareChartDataForCategory = (latestWeekData, category) => {
  console.log('Preparing chart data for category:', category)
  
  if (!latestWeekData) {
    chartData.value = null
    chartReady.value = false
    return
  }

  // Get the appropriate recipe info based on category
  const recipeKey = category === 'all' ? 'all_rcp_info' :
    category === 'only_normal' ? 'only_normal_rcp_info' :
      category === 'mother_normal' ? 'mother_normal_rcp_info' :
        'only_sample_rcp_info'

  const summaryKey = category === 'all' ? 'all_summary' :
    category === 'only_normal' ? 'only_normal_summary' :
      category === 'mother_normal' ? 'mother_normal_summary' :
        'only_sample_summary'

  const recipeData = latestWeekData[recipeKey] || []
  const summaryData = latestWeekData[summaryKey] || []

  if (recipeData.length === 0 || summaryData.length === 0) {
    chartData.value = null
    summaryChartData.value = null
    chartReady.value = false
    return
  }

  // Sort summary data by para_all from highest to lowest
  const sortedSummary = [...summaryData].sort((a, b) => (b.para_all || 0) - (a.para_all || 0))

  // Group recipe data by prod_id and calculate averages of percentages
  const prodIdMap = new Map()
  
  recipeData.forEach(item => {
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

  // Calculate averages for each prod_id (following sort order from summary)
  const prodIds = sortedSummary.map(item => item.prod_id).filter(id => prodIdMap.has(id))
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

  chartData.value = {
    prodIds,
    para5Data,
    para9Data,
    para13Data,
    para16Data
  }

  // Prepare summary chart data
  summaryChartData.value = {
    prodIds: sortedSummary.map(item => String(item.prod_id || '')),
    availRecipe: sortedSummary.map(item => Number(item.avail_recipe) || 0),
    paraAll: sortedSummary.map(item => Number(item.para_all) || 0),
    ctnDesc: sortedSummary.map(item => String(item.ctn_desc || `Container for ${item.prod_id || 'Unknown'}`))
  }

  chartReady.value = true
}

// Handle category selection
const onCategorySelect = (category) => {
  selectedCategory.value = category
  chartReady.value = false
  
  if (statisticsData.value && latestDate.value) {
    const latestData = statisticsData.value[latestDate.value]
    if (latestData) {
      rawLatestData.value = latestData
      prepareChartDataForCategory(latestData, category)
    }
  }
}

// Watch for Vue Query data changes
watch(allDeviceData, (newData) => {
  if (newData) {
    console.log('[FacOthers CurrentStatus] Device data loaded:', newData)
    
    // If no stored selections, use the fresh data
    if (!statisticsData.value) {
      statisticsData.value = newData
      
      // Auto-select all products
      if (newData.available_products) {
        selectedProducts.value = [...newData.available_products]
      }
      
      // Get latest date
      const dateKeys = Object.keys(newData).filter(key => key.match(/^\d{4}-\d{2}-\d{2}$/))
      if (dateKeys.length > 0) {
        latestDate.value = dateKeys.sort((a, b) => new Date(b) - new Date(a))[0]
      }
    }
  }
})

onMounted(() => {
  console.log('[FacOthers CurrentStatus] Component mounted')
  
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