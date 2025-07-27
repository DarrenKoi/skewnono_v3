<template>
  <div class="combined-charts-container">
    <!-- A single div for the combined chart. Height is increased to accommodate both charts and dataZoom. -->
    <div ref="combinedChartRef" style="height: 1050px; width: 100%;"></div>
    
    <!-- Recipe Details Table Card -->
    <div v-if="selectedProductData" class="mt-6">
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-xl font-semibold">
            Recipe Details for {{ selectedProductData.prodId }}
            <span class="text-sm font-normal text-surface-600 dark:text-surface-400 ml-2">
              ({{ categoryLabels[selectedProductData.category] }})
            </span>
          </h3>
          <div class="flex gap-2">
            <button 
              @click="exportToExcel"
              class="px-3 py-1.5 bg-green-600 hover:bg-green-700 text-white rounded-md flex items-center gap-2 text-sm transition-colors shadow-sm hover:shadow-md"
              title="Export to Excel"
            >
              <i class="pi pi-file-excel"></i>
              Export Excel
            </button>
            <button 
              @click="clearSelectedProduct"
              class="text-surface-400 hover:text-surface-600 dark:hover:text-surface-300 p-1.5"
              title="Close"
            >
              <i class="pi pi-times text-lg"></i>
            </button>
          </div>
        </div>
        
        <div v-if="selectedProductData.recipeData.length === 0" class="text-center py-8">
          <i class="pi pi-info-circle text-4xl text-surface-400 mb-4"></i>
          <p class="text-surface-600 dark:text-surface-400">No recipe data found for this product.</p>
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-surface-200 dark:border-surface-700">
                <th class="text-left py-2 px-3 font-semibold">Recipe ID</th>
                <th class="text-left py-2 px-3 font-semibold">Operation</th>
                <th class="text-center py-2 px-3 font-semibold">Para 5</th>
                <th class="text-center py-2 px-3 font-semibold">Para 9</th>
                <th class="text-center py-2 px-3 font-semibold">Para 13</th>
                <th class="text-center py-2 px-3 font-semibold">Para 16</th>
                <th class="text-center py-2 px-3 font-semibold">Para 5%</th>
                <th class="text-center py-2 px-3 font-semibold">Para 9%</th>
                <th class="text-center py-2 px-3 font-semibold">Para 13%</th>
                <th class="text-center py-2 px-3 font-semibold">Para 16%</th>
                <th class="text-center py-2 px-3 font-semibold">Skip</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(recipe, index) in selectedProductData.recipeData" 
                :key="`${recipe.recipe_id}-${index}`"
                class="border-b border-surface-100 dark:border-surface-800 hover:bg-surface-50 dark:hover:bg-surface-800"
              >
                <td class="py-2 px-3">{{ recipe.recipe_id }}</td>
                <td class="py-2 px-3">{{ recipe.oper_desc || '-' }}</td>
                <td class="text-center py-2 px-3">{{ recipe.para_5 || 0 }}</td>
                <td class="text-center py-2 px-3">{{ recipe.para_9 || 0 }}</td>
                <td class="text-center py-2 px-3">{{ recipe.para_13 || 0 }}</td>
                <td class="text-center py-2 px-3">{{ recipe.para_16 || 0 }}</td>
                <td class="text-center py-2 px-3">{{ (recipe.para_5_percent || 0).toFixed(1) }}%</td>
                <td class="text-center py-2 px-3">{{ (recipe.para_9_percent || 0).toFixed(1) }}%</td>
                <td class="text-center py-2 px-3">{{ (recipe.para_13_percent || 0).toFixed(1) }}%</td>
                <td class="text-center py-2 px-3">{{ (recipe.para_16_percent || 0).toFixed(1) }}%</td>
                <td class="text-center py-2 px-3">
                  <span class="inline-flex items-center px-2 py-1 rounded-full text-xs" :class="{
                    'bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-300': recipe.skip_yn === 'Y',
                    'bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-300': recipe.skip_yn !== 'Y'
                  }">
                    {{ recipe.skip_yn === 'Y' ? 'Yes' : 'No' }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div v-if="selectedProductData.recipeData.length > 0" class="mt-4 text-sm text-surface-600 dark:text-surface-400">
          Showing {{ selectedProductData.recipeData.length }} recipe(s)
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { BarChart } from 'echarts/charts';
import {
  GridComponent,
  LegendComponent,
  ToolboxComponent,
  TitleComponent,
  DataZoomComponent,
  TooltipComponent,
} from 'echarts/components';
import * as echarts from 'echarts';

// Register ECharts components
use([
  CanvasRenderer,
  BarChart,
  GridComponent,
  LegendComponent,
  ToolboxComponent,
  TitleComponent,
  DataZoomComponent,
  TooltipComponent,
]);

const props = defineProps({
  chartData: { type: Object, required: true },
  summaryChartData: { type: Object, required: true },
  selectedCategory: { type: String, required: true },
  rawLatestData: { type: Object, required: false },
});

const emit = defineEmits(['productSelected']);

const combinedChartRef = ref(null);
let combinedChartInstance = null;
const isDisposing = ref(false);
let resizeTimeout = null;
const selectedProductData = ref(null);

const categoryLabels = {
  'all': 'All Categories',
  'only_normal': 'Only Normal',
  'mother_normal': 'Mother Normal',
  'only_sample': 'Only Sample',
};

const initChart = () => {
  if (!combinedChartRef.value) return;

  if (combinedChartInstance) {
    combinedChartInstance.dispose();
    combinedChartInstance = null;
  }

  combinedChartInstance = echarts.init(combinedChartRef.value);

  // Add click event handler
  combinedChartInstance.on('click', handleBarClick);

  // Only update chart if we have valid data
  if (props.chartData && props.summaryChartData) {
    updateChart();
  }
};

const handleBarClick = (params) => {
  console.log('Bar clicked:', params);
  
  if (!props.rawLatestData || !params.name) return;
  
  const prodId = params.name;
  
  // Get the appropriate recipe info based on selected category
  const recipeKey = props.selectedCategory === 'all' ? 'all_rcp_info' :
    props.selectedCategory === 'only_normal' ? 'only_normal_rcp_info' :
      props.selectedCategory === 'mother_normal' ? 'mother_normal_rcp_info' :
        'only_sample_rcp_info';
  
  const recipeData = props.rawLatestData[recipeKey] || [];
  
  // Filter recipe data for the clicked product ID
  const filteredRecipeData = recipeData.filter(item => item.prod_id === prodId);
  
  console.log('Filtered recipe data for', prodId, ':', filteredRecipeData);
  
  // Store the selected product data
  selectedProductData.value = {
    prodId,
    recipeData: filteredRecipeData,
    category: props.selectedCategory
  };
  
  // Emit event with the product info and recipe data
  emit('productSelected', {
    prodId,
    recipeData: filteredRecipeData,
    category: props.selectedCategory
  });
};

const clearSelectedProduct = () => {
  selectedProductData.value = null;
};

// Export table data to Excel
const exportToExcel = async () => {
  if (!selectedProductData.value || !selectedProductData.value.recipeData.length) {
    console.warn('No data to export');
    return;
  }

  try {
    // Dynamically import xlsx to reduce initial bundle size
    const XLSX = await import('xlsx');
    
    // Prepare data for export
    const exportData = selectedProductData.value.recipeData.map(recipe => ({
      'Recipe ID': recipe.recipe_id,
      'Operation': recipe.oper_desc || '-',
      'Para 5': recipe.para_5 || 0,
      'Para 9': recipe.para_9 || 0,
      'Para 13': recipe.para_13 || 0,
      'Para 16': recipe.para_16 || 0,
      'Para 5%': `${(recipe.para_5_percent || 0).toFixed(1)}%`,
      'Para 9%': `${(recipe.para_9_percent || 0).toFixed(1)}%`,
      'Para 13%': `${(recipe.para_13_percent || 0).toFixed(1)}%`,
      'Para 16%': `${(recipe.para_16_percent || 0).toFixed(1)}%`,
      'Skip': recipe.skip_yn === 'Y' ? 'Yes' : 'No'
    }));

    // Create workbook and worksheet
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(exportData);

    // Set column widths
    const colWidths = [
      { wch: 15 }, // Recipe ID
      { wch: 30 }, // Operation
      { wch: 10 }, // Para 5
      { wch: 10 }, // Para 9
      { wch: 10 }, // Para 13
      { wch: 10 }, // Para 16
      { wch: 10 }, // Para 5%
      { wch: 10 }, // Para 9%
      { wch: 10 }, // Para 13%
      { wch: 10 }, // Para 16%
      { wch: 8 }   // Skip
    ];
    ws['!cols'] = colWidths;

    // Add worksheet to workbook
    XLSX.utils.book_append_sheet(wb, ws, 'Recipe Details');

    // Generate filename with product ID and timestamp
    const timestamp = new Date().toISOString().slice(0, 19).replace(/:/g, '-');
    const filename = `Recipe_Details_${selectedProductData.value.prodId}_${timestamp}.xlsx`;

    // Write and download the file
    XLSX.writeFile(wb, filename);
  } catch (error) {
    console.error('Error exporting to Excel:', error);
    alert('Failed to export data. Please try again.');
  }
};

const updateChart = () => {
  if (!combinedChartInstance || isDisposing.value) return;

  try {
    // Validate props exist
    if (!props.chartData || !props.summaryChartData) {
      console.warn('Missing required props for chart update');
      combinedChartInstance.clear();
      return;
    }

    // --- Create unified prodIds array defensively ---
    const unifiedProdIds = Array.from(new Set([
      ...(props.chartData?.prodIds ?? []),
      ...(props.summaryChartData?.prodIds ?? [])
    ])).sort();

    // If there's no data at all, clear the chart and stop.
    if (unifiedProdIds.length === 0) {
      combinedChartInstance.clear();
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

    // First remap all data to unified prodIds
    const unifiedPara5Data = remapData(props.chartData?.para5Data, chartProdIds);
    const unifiedPara9Data = remapData(props.chartData?.para9Data, chartProdIds);
    const unifiedPara13Data = remapData(props.chartData?.para13Data, chartProdIds);
    const unifiedPara16Data = remapData(props.chartData?.para16Data, chartProdIds);

    const unifiedParaAll = remapData(props.summaryChartData?.paraAll, summaryProdIds);
    const unifiedAvailRecipe = remapData(props.summaryChartData?.availRecipe, summaryProdIds);

    // --- Sort data based on para_all values (largest to smallest) ---
    const sortedIndices = unifiedParaAll
      .map((value, index) => ({ value, index }))
      .sort((a, b) => b.value - a.value)
      .map(item => item.index);

    // Apply sorting to all data arrays
    const sortData = (data) => sortedIndices.map(i => data[i]);
    
    const sortedProdIds = sortData(unifiedProdIds);
    const sortedPara5Data = sortData(unifiedPara5Data);
    const sortedPara9Data = sortData(unifiedPara9Data);
    const sortedPara13Data = sortData(unifiedPara13Data);
    const sortedPara16Data = sortData(unifiedPara16Data);
    const sortedParaAll = sortData(unifiedParaAll);
    const sortedAvailRecipe = sortData(unifiedAvailRecipe);
    
    console.log('Summary data check:', {
      hasSummaryData: !!props.summaryChartData,
      hasParaAll: !!props.summaryChartData?.paraAll,
      hasAvailRecipe: !!props.summaryChartData?.availRecipe,
      paraAllLength: props.summaryChartData?.paraAll?.length,
      availRecipeLength: props.summaryChartData?.availRecipe?.length,
      unifiedParaAllLength: unifiedParaAll.length,
      unifiedAvailRecipeLength: unifiedAvailRecipe.length
    });

    console.log('Sorting check:', {
      originalOrder: unifiedProdIds.slice(0, 10),
      sortedOrder: sortedProdIds.slice(0, 10),
      originalParaAll: unifiedParaAll.slice(0, 10),
      sortedParaAll: sortedParaAll.slice(0, 10)
    });

    // Validate that we have valid data arrays
    if (!Array.isArray(unifiedPara5Data) || !Array.isArray(unifiedParaAll)) {
      console.error('Invalid data arrays after remapping');
      combinedChartInstance.clear();
      return;
    }

    // --- Prepare Parameter Chart Data ---
    const totalsByProdId = sortedProdIds.map((_, index) =>
      sortedPara5Data[index] + sortedPara9Data[index] + sortedPara13Data[index] + sortedPara16Data[index]
    );

    const getPercentageData = (data) => data.map((value, index) => {
      const total = totalsByProdId[index];
      return total > 0 ? parseFloat(((value / total) * 100).toFixed(1)) : 0;
    });

    const para5PercentData = getPercentageData(sortedPara5Data);
    const para9PercentData = getPercentageData(sortedPara9Data);
    const para13PercentData = getPercentageData(sortedPara13Data);
    const para16PercentData = getPercentageData(sortedPara16Data);

    // Ensure all arrays have the same length
    const dataLength = sortedProdIds.length;
    if (para5PercentData.length !== dataLength ||
        para9PercentData.length !== dataLength ||
        para13PercentData.length !== dataLength ||
        para16PercentData.length !== dataLength ||
        sortedParaAll.length !== dataLength ||
        sortedAvailRecipe.length !== dataLength) {
      console.error('Data arrays have mismatched lengths');
      combinedChartInstance.clear();
      return;
    }

    // --- The Combined ECharts Option ---
    const option = {
      animation: true,
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        },
        formatter: function(params) {
          const dataIndex = params[0].dataIndex;
          const prodId = params[0].name;
          
          // Get ctn_desc from summaryChartData - need to find the original index before sorting
          let ctnDesc = '';
          if (props.summaryChartData?.ctnDesc) {
            // Find the original index of this prodId in the unsorted data
            const originalIndex = (props.summaryChartData.prodIds || []).findIndex(id => id === prodId);
            if (originalIndex !== -1) {
              ctnDesc = props.summaryChartData.ctnDesc[originalIndex] || '';
            }
          }
          
          let tooltipText = `<strong>${prodId}</strong><br/>`;
          if (ctnDesc) {
            tooltipText += `<em>${ctnDesc}</em><br/><br/>`;
          }
          
          // Check if it's parameter distribution (stacked) or total/recipe chart
          if (params[0].seriesIndex <= 3) {
            // Parameter distribution chart
            const total = totalsByProdId[dataIndex];
            tooltipText += `Total Count: ${total.toFixed(2)}<br/>`;
            params.forEach(item => {
              const actualValue = item.seriesIndex === 0 ? sortedPara5Data[item.dataIndex] :
                                  item.seriesIndex === 1 ? sortedPara9Data[item.dataIndex] :
                                  item.seriesIndex === 2 ? sortedPara13Data[item.dataIndex] :
                                  sortedPara16Data[item.dataIndex];
              tooltipText += `${item.marker} ${item.seriesName}: ${actualValue.toFixed(2)} (${item.value}%)<br/>`;
            });
          } else {
            // Total parameters & recipes chart
            params.forEach(item => {
              tooltipText += `${item.marker} ${item.seriesName}: ${item.value}<br/>`;
            });
          }
          
          return tooltipText;
        }
      },
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
        { top: '55%', right: '5%', left: '5%', bottom: '20%' },
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
        { type: 'category', data: sortedProdIds, gridIndex: 0, axisLabel: { show: false } },
        { type: 'category', data: sortedProdIds, gridIndex: 1, axisLabel: { rotate: 45 } },
      ],
      yAxis: [
        { 
          type: 'value', 
          name: 'Percentage (%)', 
          gridIndex: 0, 
          max: 100,
          splitLine: { show: false }  // Remove horizontal grid lines
        },
        { 
          type: 'value', 
          name: 'Total Parameters', 
          gridIndex: 1, 
          position: 'left',
          splitLine: { show: false }  // Remove horizontal grid lines
        },
        { 
          type: 'value', 
          name: 'Available Recipes', 
          gridIndex: 1, 
          position: 'right',
          splitLine: { show: false }  // Remove horizontal grid lines
        },
      ],
      dataZoom: [
        {
          type: 'slider',
          show: true,
          xAxisIndex: [0, 1],
          start: 0,
          end: 30,  // Show first 30% of data
          bottom: '5%',
          height: 30,
          handleSize: '80%',
          handleStyle: {
            color: '#fff',
            shadowBlur: 3,
            shadowColor: 'rgba(0, 0, 0, 0.6)',
            shadowOffsetX: 2,
            shadowOffsetY: 2,
          },
        },
        {
          type: 'inside',
          xAxisIndex: [0, 1],
          start: 0,
          end: 30,  // Show first 30% of data
        },
      ],
      series: [
        { 
          name: 'Para 5', 
          type: 'bar', 
          stack: 'total', 
          data: para5PercentData, 
          xAxisIndex: 0, 
          yAxisIndex: 0, 
          itemStyle: { color: '#5470c6' },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            position: 'inside',
            formatter: (params) => params.value > 5 ? params.value + '%' : '',
            fontSize: 10,
          }
        },
        { 
          name: 'Para 9', 
          type: 'bar', 
          stack: 'total', 
          data: para9PercentData, 
          xAxisIndex: 0, 
          yAxisIndex: 0, 
          itemStyle: { color: '#91cc75' },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            position: 'inside',
            formatter: (params) => params.value > 5 ? params.value + '%' : '',
            fontSize: 10,
          }
        },
        { 
          name: 'Para 13', 
          type: 'bar', 
          stack: 'total', 
          data: para13PercentData, 
          xAxisIndex: 0, 
          yAxisIndex: 0, 
          itemStyle: { color: '#fac858' },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            position: 'inside',
            formatter: (params) => params.value > 5 ? params.value + '%' : '',
            fontSize: 10,
          }
        },
        { 
          name: 'Para 16', 
          type: 'bar', 
          stack: 'total', 
          data: para16PercentData, 
          xAxisIndex: 0, 
          yAxisIndex: 0, 
          itemStyle: { color: '#ee6666' },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            position: 'inside',
            formatter: (params) => params.value > 5 ? params.value + '%' : '',
            fontSize: 10,
          }
        },
        { 
          name: 'Total Parameters', 
          type: 'bar', 
          data: sortedParaAll, 
          xAxisIndex: 1, 
          yAxisIndex: 1, 
          itemStyle: { color: '#5470c6' },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}',
            fontSize: 10,
          }
        },
        { 
          name: 'Available Recipes', 
          type: 'bar', 
          data: sortedAvailRecipe, 
          xAxisIndex: 1, 
          yAxisIndex: 2, 
          itemStyle: { color: '#91cc75' },
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)'
            }
          },
          label: {
            show: true,
            position: 'top',
            formatter: '{c}',
            fontSize: 10,
          }
        },
      ]
    };

    // Set the option with better error handling
    try {
      combinedChartInstance.setOption(option, { notMerge: true });
      combinedChartInstance.resize();
    } catch (setOptionError) {
      console.error('Error setting chart option:', setOptionError);
      // Try to recover by clearing and re-initializing
      combinedChartInstance.clear();
      combinedChartInstance.setOption(option);
    }

  } catch (error) {
    console.error('Error updating combined chart:', error);
  }
};

const handleResize = () => {
  if (resizeTimeout) clearTimeout(resizeTimeout);
  resizeTimeout = setTimeout(() => {
    if (combinedChartInstance && !isDisposing.value) {
      combinedChartInstance.resize();
    }
  }, 100);
};

watch([() => props.chartData, () => props.summaryChartData, () => props.selectedCategory], (newValues, oldValues) => {
  // Clear selected product if category changed
  if (oldValues && newValues[2] !== oldValues[2]) {
    selectedProductData.value = null;
  }
  
  // Only update if the chart instance exists
  if (combinedChartInstance) {
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
  if (combinedChartInstance) {
    combinedChartInstance.dispose();
    combinedChartInstance = null;
  }
});
</script>
