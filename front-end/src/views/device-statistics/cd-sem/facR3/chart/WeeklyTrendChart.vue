<template>
  <div class="weekly-trend-chart">
    <!-- Options Selection Card -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <h3 class="text-lg font-semibold mb-4">Chart Options</h3>
      
      <!-- Y-axis Parameter Selection -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-surface-700 dark:text-surface-300 mb-2">
          Select Y-axis Parameter
        </label>
        <div class="flex flex-wrap gap-2">
          <Button 
            v-for="param in parameterOptions" 
            :key="param.key"
            :label="param.label"
            :severity="selectedParameter === param.key ? 'primary' : 'secondary'"
            :outlined="selectedParameter !== param.key"
            size="small"
            @click="selectParameter(param.key)"
          />
        </div>
      </div>

      <!-- Product ID Selection -->
      <div class="mb-4">
        <div class="flex items-center justify-between mb-2">
          <label class="block text-sm font-medium text-surface-700 dark:text-surface-300">
            Select Product IDs
          </label>
          <div class="flex gap-2">
            <Button 
              label="Select All" 
              size="small" 
              text
              @click="selectAllProducts"
            />
            <Button 
              label="Clear All" 
              size="small" 
              text
              severity="secondary"
              @click="clearAllProducts"
            />
          </div>
        </div>
        
        <!-- Search Input -->
        <InputText 
          v-model="productSearchQuery"
          placeholder="Search product IDs..."
          class="w-full mb-3"
        />
        
        <!-- Product ID Grid with Scroll -->
        <div class="border rounded-lg p-3 max-h-48 overflow-y-auto">
          <div class="grid grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-2">
            <div
              v-for="prodId in filteredProductIds"
              :key="prodId"
              class="p-2 border rounded cursor-pointer transition-all text-center text-sm"
              :class="{
                'border-primary bg-primary-100 dark:bg-primary-800/30': selectedProductIds.includes(prodId),
                'border-surface-200 dark:border-surface-700 hover:border-primary/50': !selectedProductIds.includes(prodId)
              }"
              @click="toggleProductId(prodId)"
            >
              {{ prodId }}
            </div>
          </div>
          <div v-if="filteredProductIds.length === 0" class="text-center py-4 text-surface-500">
            No products match your search
          </div>
        </div>
        
        <div class="mt-2 text-sm text-surface-600 dark:text-surface-400">
          Selected: {{ selectedProductIds.length }} / {{ availableProductIds.length }} products
        </div>
      </div>
    </div>

    <!-- Chart or Message Display -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <!-- Chart Header - Always show when parameter is selected -->
      <div v-if="selectedParameter" class="mb-4">
        <h3 class="text-xl font-semibold">{{ getParameterLabel(selectedParameter) }} - Time Series Analysis</h3>
        <p class="text-surface-600 dark:text-surface-400 mt-1">
          <span v-if="selectedProductIds.length > 0">
            Showing {{ selectedProductIds.length }} products over {{ dateRange.length }} time periods
          </span>
          <span v-else class="text-warning-600 dark:text-warning-400">
            Please select at least one product ID to display data
          </span>
        </p>
      </div>
      
      <!-- ECharts Container - Always rendered when parameter is selected -->
      <div v-if="selectedParameter" ref="chartRef" style="height: 600px; width: 100%;"></div>

      <!-- No Parameter Selected Message -->
      <div v-if="!selectedParameter" class="text-center py-12">
        <i class="pi pi-chart-line text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300 text-lg">
          Please select a parameter to display
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import { 
  GridComponent, 
  TooltipComponent, 
  LegendComponent,
  DataZoomComponent,
  TitleComponent,
  ToolboxComponent,
  MarkLineComponent,
  MarkPointComponent
} from 'echarts/components'
import * as echarts from 'echarts'

// Register ECharts components
use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  TitleComponent,
  ToolboxComponent,
  MarkLineComponent,
  MarkPointComponent
])

const props = defineProps({
  weeklyData: {
    type: Object,
    required: true
  },
  selectedCategory: {
    type: String,
    required: true
  },
  selectedProdIds: {
    type: Array,
    default: () => []
  }
})

// Chart instance
const chartRef = ref(null)
let chartInstance = null

// State
const selectedParameter = ref('para_all') // Default to total parameters
const selectedProductIds = ref([])
const productSearchQuery = ref('')

// Parameter options for Y-axis
const parameterOptions = ref([
  { key: 'para_5', label: 'Para 5' },
  { key: 'para_9', label: 'Para 9' },
  { key: 'para_13', label: 'Para 13' },
  { key: 'para_16', label: 'Para 16' },
  { key: 'para_all', label: 'Total Parameters' },
  { key: 'avail_recipe', label: 'Available Recipes' },
  { key: 'para_5_percent', label: 'Para 5 (%)' },
  { key: 'para_9_percent', label: 'Para 9 (%)' },
  { key: 'para_13_percent', label: 'Para 13 (%)' },
  { key: 'para_16_percent', label: 'Para 16 (%)' },
  { key: 'avail_recipe_percent', label: 'Available Recipes (%)' }
])

// Get parameter label
const getParameterLabel = (key) => {
  const option = parameterOptions.value.find(p => p.key === key)
  return option ? option.label : key
}

// Computed: available product IDs from data
const availableProductIds = computed(() => {
  if (!props.weeklyData || Object.keys(props.weeklyData).length === 0) return []
  
  const prodIdSet = new Set()
  
  // Iterate through all dates to collect unique product IDs
  Object.values(props.weeklyData).forEach(dateData => {
    // Get the appropriate data based on selected category
    const dataKey = props.selectedCategory === 'all' ? 'all_summary' :
                    props.selectedCategory === 'only_normal' ? 'only_normal_summary' :
                    props.selectedCategory === 'mother_normal' ? 'mother_normal_summary' :
                    'only_sample_summary'
    
    const summaryData = dateData[dataKey] || []
    summaryData.forEach(item => {
      if (item.prod_id) {
        prodIdSet.add(item.prod_id)
      }
    })
  })
  
  return Array.from(prodIdSet).sort()
})

// Computed: filtered product IDs based on search
const filteredProductIds = computed(() => {
  if (!productSearchQuery.value) return availableProductIds.value
  
  const query = productSearchQuery.value.toLowerCase()
  return availableProductIds.value.filter(id => 
    id.toLowerCase().includes(query)
  )
})

// Computed: date range
const dateRange = computed(() => {
  if (!props.weeklyData) return []
  return Object.keys(props.weeklyData).sort()
})

// Methods
const selectParameter = (param) => {
  selectedParameter.value = param
}

const toggleProductId = (prodId) => {
  const index = selectedProductIds.value.indexOf(prodId)
  if (index > -1) {
    selectedProductIds.value.splice(index, 1)
  } else {
    selectedProductIds.value.push(prodId)
  }
}

const selectAllProducts = () => {
  selectedProductIds.value = [...availableProductIds.value]
}

const clearAllProducts = () => {
  selectedProductIds.value = []
}

// Process data for chart
const processChartData = () => {
  if (!props.weeklyData || selectedProductIds.value.length === 0 || !selectedParameter.value) {
    return null
  }
  
  const series = []
  const dates = dateRange.value
  const isPercentage = selectedParameter.value.includes('_percent')
  
  // Get the appropriate data key based on selected category and parameter type
  const summaryKey = props.selectedCategory === 'all' ? 'all_summary' :
                     props.selectedCategory === 'only_normal' ? 'only_normal_summary' :
                     props.selectedCategory === 'mother_normal' ? 'mother_normal_summary' :
                     'only_sample_summary'
  
  const recipeKey = props.selectedCategory === 'all' ? 'all_rcp_info' :
                    props.selectedCategory === 'only_normal' ? 'only_normal_rcp_info' :
                    props.selectedCategory === 'mother_normal' ? 'mother_normal_rcp_info' :
                    'only_sample_rcp_info'
  
  // Process each selected product
  selectedProductIds.value.forEach(prodId => {
    const data = []
    
    dates.forEach(date => {
      const dateData = props.weeklyData[date]
      
      if (isPercentage && dateData && dateData[recipeKey]) {
        // For percentage data, aggregate from recipe info
        const recipeData = dateData[recipeKey].filter(item => item.prod_id === prodId)
        if (recipeData.length > 0) {
          // Calculate average percentage across all recipes for this product
          const sum = recipeData.reduce((acc, item) => acc + (Number(item[selectedParameter.value]) || 0), 0)
          data.push(sum / recipeData.length)
        } else {
          data.push(null)
        }
      } else if (dateData && dateData[summaryKey]) {
        // For non-percentage data, use summary data
        const productData = dateData[summaryKey].find(item => item.prod_id === prodId)
        if (productData) {
          data.push(productData[selectedParameter.value] || 0)
        } else {
          data.push(null)
        }
      } else {
        data.push(null)
      }
    })
    
    series.push({
      name: prodId,
      type: 'line',
      data: data,
      smooth: true,
      symbol: 'circle',
      symbolSize: 6,
      lineStyle: {
        width: 2
      },
      emphasis: {
        focus: 'series',
        lineStyle: {
          width: 3
        }
      }
    })
  })
  
  return {
    xAxisData: dates,
    series: series
  }
}

// Initialize or update chart
const updateChart = async () => {
  // Wait for next tick to ensure DOM is updated
  await nextTick()
  
  if (!chartRef.value || !selectedParameter.value) return
  
  // Always initialize chart if it doesn't exist or has been disposed
  if (!chartInstance || chartInstance.isDisposed()) {
    chartInstance = echarts.init(chartRef.value)
  }
  
  const chartData = processChartData()
  if (!chartData || !chartData.series || chartData.series.length === 0) {
    // Show empty state message instead of clearing the chart
    const emptyOption = {
      title: {
        text: 'No Data to Display',
        subtext: 'Please select at least one product ID',
        left: 'center',
        top: 'center',
        textStyle: {
          fontSize: 20,
          color: '#999'
        },
        subtextStyle: {
          fontSize: 16,
          color: '#ccc'
        }
      },
      xAxis: {
        show: false
      },
      yAxis: {
        show: false
      },
      series: []
    }
    chartInstance.setOption(emptyOption, { notMerge: true })
    return
  }
  
  const option = {
    title: {
      text: `${getParameterLabel(selectedParameter.value)} Over Time`,
      left: 'center',
      top: 10
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        label: {
          backgroundColor: '#6a7985'
        }
      },
      formatter: function(params) {
        let tooltip = `<strong>${params[0].axisValue}</strong><br/>`
        params.forEach(param => {
          if (param.value !== null) {
            const value = param.value.toFixed(2)
            const suffix = selectedParameter.value.includes('_percent') ? '%' : ''
            tooltip += `${param.marker} ${param.seriesName}: ${value}${suffix}<br/>`
          } else {
            tooltip += `${param.marker} ${param.seriesName}: N/A<br/>`
          }
        })
        return tooltip
      }
    },
    legend: {
      type: 'scroll',
      bottom: 10,
      data: selectedProductIds.value,
      pageButtonItemGap: 5,
      pageButtonGap: 10
    },
    toolbox: {
      feature: {
        dataZoom: {
          yAxisIndex: 'none'
        },
        restore: {},
        saveAsImage: {}
      },
      right: 20
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: chartData.xAxisData,
      axisLabel: {
        rotate: 45,
        formatter: function(value) {
          // Format date to MM/DD
          const date = new Date(value)
          return `${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`
        }
      }
    },
    yAxis: {
      type: 'value',
      name: getParameterLabel(selectedParameter.value),
      nameLocation: 'middle',
      nameGap: 50,
      axisLabel: {
        formatter: function(value) {
          if (selectedParameter.value.includes('_percent')) {
            return value.toFixed(1) + '%'
          }
          return value.toFixed(0)
        }
      }
    },
    dataZoom: [
      {
        type: 'slider',
        xAxisIndex: 0,
        start: 0,
        end: 100,
        height: 20,
        bottom: 50
      },
      {
        type: 'inside',
        xAxisIndex: 0,
        start: 0,
        end: 100
      }
    ],
    series: chartData.series
  }
  
  chartInstance.setOption(option, { notMerge: true })
}

// Handle window resize
const handleResize = () => {
  if (chartInstance) {
    chartInstance.resize()
  }
}

// Watch for changes
watch([selectedParameter, () => props.weeklyData], () => {
  updateChart()
}, { deep: true })

// Separate watcher for selectedProductIds to ensure chart updates
watch(selectedProductIds, () => {
  // Force chart update when product selection changes
  updateChart()
}, { deep: true })

// Initialize selected products from props
watch(() => props.selectedProdIds, (newProdIds) => {
  if (newProdIds && newProdIds.length > 0) {
    // Filter to only include product IDs that exist in the data
    selectedProductIds.value = newProdIds.filter(id => availableProductIds.value.includes(id))
  }
}, { immediate: true })

// Lifecycle
onMounted(async () => {
  window.addEventListener('resize', handleResize)
  
  // Wait for DOM to be ready
  await nextTick()
  
  // Initial chart render - always render if parameter is selected
  if (selectedParameter.value) {
    updateChart()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
})
</script>

<style scoped>
/* Component-specific styles */
</style>