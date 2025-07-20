<template>
  <div class="combined-charts-container">
    <!-- A single div for the combined chart. Height is increased to accommodate both. -->
    <div ref="combinedChartRef" style="height: 1000px; width: 100%;"></div>
  </div>
</template>
<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  DataZoomComponent,
  TitleComponent,
} from 'echarts/components';
import * as echarts from 'echarts';

// Register ECharts components
use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  ToolboxComponent,
  DataZoomComponent,
  TitleComponent,
]);

const props = defineProps({
  chartData: { type: Object, required: true },
  summaryChartData: { type: Object, required: true },
  selectedCategory: { type: String, required: true },
});

const combinedChartRef = ref(null);
const combinedChartInstance = ref(null);
const isDisposing = ref(false);
const resizeTimeout = ref(null);

const categoryLabels = {
  'all': 'All Categories',
  'only_normal': 'Only Normal',
  'mother_normal': 'Mother Normal',
  'only_sample': 'Only Sample',
};

const initChart = () => {
  if (!combinedChartRef.value) return;

  if (combinedChartInstance.value) {
    combinedChartInstance.value.dispose();
  }

  combinedChartInstance.value = echarts.init(combinedChartRef.value, null, {
    renderer: 'canvas',
    useDirtyRect: true
  });

  updateChart();
};

const updateChart = () => {
  if (!combinedChartInstance.value || isDisposing.value) return;

  try {
    // --- Create unified prodIds array defensively ---
    const unifiedProdIds = Array.from(new Set([
      ...(props.chartData?.prodIds ?? []),
      ...(props.summaryChartData?.prodIds ?? [])
    ])).sort();

    // If there's no data at all, clear the chart and stop.
    if (unifiedProdIds.length === 0) {
      combinedChartInstance.value.clear();
      return;
    }

    // --- Remap data defensively ---
    const remapData = (originalData, originalProdIds) => {
      // Use a Map for efficient lookups
      const dataMap = new Map((originalProdIds ?? []).map((id, index) => [id, (originalData ?? [])[index]]));
      return unifiedProdIds.map(prodId => Number(dataMap.get(prodId)) || 0);
    };

    const chartProdIds = props.chartData?.prodIds;
    const summaryProdIds = props.summaryChartData?.prodIds;

    const unifiedPara5Data = remapData(props.chartData?.para5Data, chartProdIds);
    const unifiedPara9Data = remapData(props.chartData?.para9Data, chartProdIds);
    const unifiedPara13Data = remapData(props.chartData?.para13Data, chartProdIds);
    const unifiedPara16Data = remapData(props.chartData?.para16Data, chartProdIds);

    const unifiedParaAll = remapData(props.summaryChartData?.paraAll, summaryProdIds);
    const unifiedAvailRecipe = remapData(props.summaryChartData?.availRecipe, summaryProdIds);

    // --- Prepare Parameter Chart Data ---
    const totalsByProdId = unifiedProdIds.map((_, index) =>
      unifiedPara5Data[index] + unifiedPara9Data[index] + unifiedPara13Data[index] + unifiedPara16Data[index]
    );

    const getPercentageData = (data) => data.map((value, index) => {
      const total = totalsByProdId[index];
      return total > 0 ? parseFloat(((value / total) * 100).toFixed(1)) : 0;
    });

    const para5PercentData = getPercentageData(unifiedPara5Data);
    const para9PercentData = getPercentageData(unifiedPara9Data);
    const para13PercentData = getPercentageData(unifiedPara13Data);
    const para16PercentData = getPercentageData(unifiedPara16Data);

    // --- The Combined ECharts Option ---
    const option = {
      animation: true,
      legend: {
        data: ['Para 5', 'Para 9', 'Para 13', 'Para 16', 'Total Parameters', 'Available Recipes'],
        top: '1%',
        type: 'scroll',
      },
      toolbox: {
        feature: {
          dataView: { show: true, title: 'Data View' },
          restore: { show: true, title: 'Restore' },
          saveAsImage: { show: true, title: 'Save Image' },
        },
      },
      grid: [
        { top: '12%', right: '5%', left: '5%', bottom: '55%' },
        { top: '55%', right: '5%', left: '5%', bottom: '15%' },
      ],
      title: [
        {
          text: `Parameter Distribution - ${categoryLabels[props.selectedCategory]}`,
          left: 'center',
          top: '7%',
        },
        {
          text: `Total Parameters & Recipes - ${categoryLabels[props.selectedCategory]}`,
          left: 'center',
          top: '50%',
        }
      ],
      xAxis: [
        { type: 'category', data: unifiedProdIds, gridIndex: 0, axisLabel: { show: false } },
        { type: 'category', data: unifiedProdIds, gridIndex: 1, axisLabel: { rotate: 45 } },
      ],
      yAxis: [
        { type: 'value', name: 'Percentage (%)', gridIndex: 0, max: 100 },
        { type: 'value', name: 'Total Parameters', gridIndex: 1, position: 'left' },
        { type: 'value', name: 'Available Recipes', gridIndex: 1, position: 'right' },
      ],
      series: [
        { name: 'Para 5', type: 'bar', stack: 'total', data: para5PercentData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#5470c6' } },
        { name: 'Para 9', type: 'bar', stack: 'total', data: para9PercentData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#91cc75' } },
        { name: 'Para 13', type: 'bar', stack: 'total', data: para13PercentData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#fac858' } },
        { name: 'Para 16', type: 'bar', stack: 'total', data: para16PercentData, xAxisIndex: 0, yAxisIndex: 0, itemStyle: { color: '#ee6666' } },
        { name: 'Total Parameters', type: 'bar', data: unifiedParaAll, xAxisIndex: 1, yAxisIndex: 1, itemStyle: { color: '#5470c6' } },
        { name: 'Available Recipes', type: 'bar', data: unifiedAvailRecipe, xAxisIndex: 1, yAxisIndex: 2, itemStyle: { color: '#91cc75' } },
      ]
    };

    combinedChartInstance.value.setOption(option, { notMerge: true });
    combinedChartInstance.value.resize();

  } catch (error) {
    console.error('Error updating combined chart:', error);
  }
};

const handleResize = () => {
  if (resizeTimeout.value) clearTimeout(resizeTimeout.value);
  resizeTimeout.value = setTimeout(() => {
    if (combinedChartInstance.value && !isDisposing.value) {
      combinedChartInstance.value.resize();
    }
  }, 100);
};

watch([() => props.chartData, () => props.summaryChartData, () => props.selectedCategory], () => {
  updateChart();
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
  if (resizeTimeout.value) clearTimeout(resizeTimeout.value);
  if (combinedChartInstance.value) {
    combinedChartInstance.value.dispose();
  }
});
</script>
