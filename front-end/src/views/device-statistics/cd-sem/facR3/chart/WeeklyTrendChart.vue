<template>
  <div class="weekly-trend-chart-container">
    <!-- Y-Axis Metric Selector -->
    <div class="mb-4">
      <div class="flex flex-wrap gap-2">
        <span class="text-sm font-medium text-surface-600 dark:text-surface-400 flex items-center">Y-Axis Metrics:</span>
        <button
          v-for="metric in availableMetrics"
          :key="metric.key"
          @click="toggleMetric(metric.key)"
          :class="[
            'px-3 py-1 text-xs rounded-full border transition-all',
            selectedMetrics.includes(metric.key)
              ? 'bg-primary-500 text-white border-primary-500'
              : 'bg-surface-100 text-surface-600 border-surface-300 hover:border-primary-300 dark:bg-surface-800 dark:text-surface-300 dark:border-surface-600'
          ]"
        >
          {{ metric.label }}
        </button>
      </div>
      <p class="text-xs text-surface-500 dark:text-surface-400 mt-2">
        Click metrics to show/hide them on the chart
      </p>
    </div>

    <!-- Chart Container -->
    <div ref="chartRef" style="height: 500px; width: 100%;"></div>

    <!-- No Data State -->
    <div v-if="!hasData" class="text-center py-8">
      <i class="pi pi-inbox text-4xl text-surface-400 mb-4"></i>
      <p class="text-surface-600 dark:text-surface-400">No weekly trend data available for the selected criteria.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick, computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent,
  TitleComponent,
} from 'echarts/components';
import * as echarts from 'echarts';

// Register ECharts components
use([
  CanvasRenderer,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  DataZoomComponent,
  ToolboxComponent,
  TitleComponent,
]);

const props = defineProps({
  weeklyData: { type: Object, required: true },
  selectedCategory: { type: String, required: true },
  selectedProdIds: { type: Array, required: true },
});

const chartRef = ref(null);
let chartInstance = null;
const isDisposing = ref(false);
let resizeTimeout = null;

// Available metrics for Y-axis selection
const availableMetrics = ref([
  { key: 'para_5', label: 'Para 5', color: '#5470c6' },
  { key: 'para_9', label: 'Para 9', color: '#91cc75' },
  { key: 'para_13', label: 'Para 13', color: '#fac858' },
  { key: 'para_16', label: 'Para 16', color: '#ee6666' },
  { key: 'para_all', label: 'Total Parameters', color: '#73c0de' },
  { key: 'avail_recipe', label: 'Available Recipes', color: '#3ba272' },
]);

// Selected metrics (default: show para_all and avail_recipe)
const selectedMetrics = ref(['para_all', 'avail_recipe']);

// Toggle metric visibility
const toggleMetric = (metricKey) => {
  const index = selectedMetrics.value.indexOf(metricKey);
  if (index > -1) {
    selectedMetrics.value.splice(index, 1);
  } else {
    selectedMetrics.value.push(metricKey);
  }
};

// Check if we have data
const hasData = computed(() => {
  return props.weeklyData && Object.keys(props.weeklyData).length > 0;
});

// Category labels for display
const categoryLabels = {
  'all': 'All Categories',
  'only_normal': 'Only Normal',
  'mother_normal': 'Mother Normal',
  'only_sample': 'Only Sample',
};

const initChart = () => {
  if (!chartRef.value) return;

  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }

  chartInstance = echarts.init(chartRef.value);
  updateChart();
};

const updateChart = () => {
  if (!chartInstance || isDisposing.value || !hasData.value) return;

  try {
    const processedData = processWeeklyData();
    
    if (!processedData || processedData.dates.length === 0) {
      chartInstance.clear();
      return;
    }

    const option = {
      animation: true,
      title: {
        text: `Weekly Trend (Step Line) - ${categoryLabels[props.selectedCategory] || props.selectedCategory}`,
        left: 'center',
        top: '2%',
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
          let tooltipText = `<strong>${params[0].axisValue}</strong><br/>`;
          params.forEach(item => {
            if (selectedMetrics.value.includes(item.seriesName.toLowerCase().replace(' ', '_'))) {
              tooltipText += `${item.marker} ${item.seriesName}: ${item.value}<br/>`;
            }
          });
          return tooltipText;
        }
      },
      legend: {
        data: availableMetrics.value
          .filter(metric => selectedMetrics.value.includes(metric.key))
          .map(metric => metric.label),
        top: '8%',
        type: 'scroll',
      },
      toolbox: {
        feature: {
          dataZoom: { show: true, title: { zoom: 'Zoom', back: 'Reset Zoom' } },
          dataView: { show: true, title: 'Data View' },
          restore: { show: true, title: 'Restore' },
          saveAsImage: { show: true, title: 'Save Image' },
        },
        top: '2%',
        right: '2%',
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '20%',
        top: '20%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: processedData.dates,
        axisLabel: {
          rotate: 45,
          formatter: function(value) {
            return value; // Already formatted as YYYY-MM-DD
          }
        }
      },
      yAxis: {
        type: 'value',
        name: 'Count',
        splitLine: { show: true, lineStyle: { type: 'dashed' } }
      },
      dataZoom: [
        {
          type: 'slider',
          show: true,
          start: 0,
          end: 100,
          bottom: '5%',
        },
        {
          type: 'inside',
          start: 0,
          end: 100,
        },
      ],
      series: processedData.series
    };

    chartInstance.setOption(option, { notMerge: true });
    chartInstance.resize();

  } catch (error) {
    console.error('Error updating weekly trend chart:', error);
  }
};

const processWeeklyData = () => {
  console.log('[WeeklyTrendChart] processWeeklyData called with:', {
    hasWeeklyData: !!props.weeklyData,
    weeklyDataKeys: props.weeklyData ? Object.keys(props.weeklyData) : 'null',
    weeklyDataKeysCount: props.weeklyData ? Object.keys(props.weeklyData).length : 0,
    selectedCategory: props.selectedCategory,
    selectedProdIds: props.selectedProdIds
  });

  if (!props.weeklyData || Object.keys(props.weeklyData).length === 0) {
    console.log('[WeeklyTrendChart] No weekly data available')
    return null;
  }

  // Get the summary key for the selected category
  const summaryKey = props.selectedCategory === 'all' ? 'all_summary' :
    props.selectedCategory === 'only_normal' ? 'only_normal_summary' :
      props.selectedCategory === 'mother_normal' ? 'mother_normal_summary' :
        'only_sample_summary';

  // Sort dates
  const dates = Object.keys(props.weeklyData).sort();
  console.log('[WeeklyTrendChart] Processing weekly data for dates:', dates);
  console.log('[WeeklyTrendChart] Using summary key:', summaryKey);

  // Process data for each date
  const dataByMetric = {};
  
  availableMetrics.value.forEach(metric => {
    dataByMetric[metric.key] = [];
  });

  dates.forEach(date => {
    const dayData = props.weeklyData[date];
    
    // Aggregate data for this date across all selected categories
    const aggregated = {
      para_5: 0,
      para_9: 0,
      para_13: 0,
      para_16: 0,
      para_all: 0,
      avail_recipe: 0,
    };

    // Process the selected category
    const summaryData = dayData[summaryKey] || [];
    
    // Filter by selected product IDs
    const filteredData = summaryData.filter(item => 
      props.selectedProdIds.includes(item.prod_id)
    );

    // Add to aggregated values
    filteredData.forEach(item => {
      aggregated.para_5 += Number(item.para_5) || 0;
      aggregated.para_9 += Number(item.para_9) || 0;
      aggregated.para_13 += Number(item.para_13) || 0;
      aggregated.para_16 += Number(item.para_16) || 0;
      aggregated.para_all += Number(item.para_all) || 0;
      aggregated.avail_recipe += Number(item.avail_recipe) || 0;
    });

    console.log(`Date ${date}: aggregated values:`, aggregated);

    // Store aggregated values
    availableMetrics.value.forEach(metric => {
      dataByMetric[metric.key].push(aggregated[metric.key]);
    });
  });

  // Create series for selected metrics only
  const series = availableMetrics.value
    .filter(metric => selectedMetrics.value.includes(metric.key))
    .map((metric, index) => ({
      name: metric.label,
      type: 'line',
      step: index % 3 === 0 ? 'start' : index % 3 === 1 ? 'middle' : 'end', // Alternate between step types
      data: dataByMetric[metric.key],
      itemStyle: { color: metric.color },
      lineStyle: { 
        color: metric.color,
        width: 2
      },
      symbol: 'circle',
      symbolSize: 6,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }));

  console.log('Generated series:', series);

  return {
    dates,
    series
  };
};

const handleResize = () => {
  if (resizeTimeout) clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    if (chartInstance && !isDisposing.value) {
      chartInstance.resize();
    }
  }, 100);
};

// Watch for changes in props and selected metrics
watch([() => props.weeklyData, () => props.selectedCategory, () => props.selectedProdIds, selectedMetrics], () => {
  if (chartInstance) {
    updateChart();
  }
}, { deep: true });

onMounted(() => {
  nextTick(() => {
    initChart();
    window.addEventListener('resize', handleResize, { passive: true });
  });
});

onUnmounted(() => {
  isDisposing.value = true;
  window.removeEventListener('resize', handleResize);
  if (resizeTimeout) {
    clearTimeout(resizeTimeout);
    resizeTimeout = null;
  }
  if (chartInstance) {
    chartInstance.dispose();
    chartInstance = null;
  }
});
</script>