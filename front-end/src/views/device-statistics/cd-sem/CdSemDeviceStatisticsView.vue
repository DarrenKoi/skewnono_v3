<template>
  <div class="device-statistics bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">디바이스 통계</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">
        {{ facId }} 시설의 디바이스 상태 및 통계 정보를 확인하세요
      </div>
    </div>

    <!-- Component based on facility type -->
    <FacR3Selection 
      v-if="facId === 'R3'" 
      :fac-id="facId"
      @selection-changed="handleR3SelectionChanged"
      @data-fetched="handleDataFetched"
    />
    
    <FacOthersSelection 
      v-else 
      :fac-id="facId"
      @selection-changed="handleOthersSelectionChanged"
      @data-fetched="handleDataFetched"
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import FacR3Selection from './facR3/FacR3Selection.vue'
import FacOthersSelection from './facOthers/FacOthersSelection.vue'

const route = useRoute()

// Get fac_id from route params or query
const facId = computed(() => route.params.facId || route.query.fac_id || 'R3')

// State for tracking data
const currentSelectionData = ref(null)

// Handle R3 selection changed
const handleR3SelectionChanged = (data) => {
  currentSelectionData.value = data
  console.log('R3 selection changed:', data)
}

// Handle Others selection changed
const handleOthersSelectionChanged = (data) => {
  currentSelectionData.value = data
  console.log('Others selection changed:', data)
}

// Handle data fetched from child components
const handleDataFetched = (data) => {
  console.log('Data fetched:', data)
  // You can emit this data to parent components or use it as needed
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>