<template>
  <div class="weekly-trend bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button 
        icon="pi pi-arrow-left" 
        label="디바이스 통계로 돌아가기"
        outlined
        size="large"
        class="mb-2"
        @click="goBack" 
      />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">주별 트렌드</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          주별 데이터 변화 추이를 분석합니다
        </div>
      </div>
    </div>

    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-semibold">Weekly Trend Analysis</h2>
      </div>
      
      <!-- Placeholder for now -->
      <div class="text-center py-12">
        <i class="pi pi-chart-line text-6xl text-surface-400 mb-4"></i>
        <p class="text-surface-600 dark:text-surface-300">주별 트렌드 기능은 준비 중입니다</p>
        <p class="text-sm text-surface-500 dark:text-surface-400 mt-2">
          선택된 카테고리: {{ selectedCategories }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'

const router = useRouter()

// R3-specific stored selections from session storage
const facId = 'R3'
const selectedR3Options = JSON.parse(sessionStorage.getItem('deviceStatistics_selectedR3Options') || '[]')

// Computed property for display
const selectedCategories = computed(() => {
  return selectedR3Options.join(', ') || 'None'
})

// Go back to device statistics main page
const goBack = () => {
  router.push(`/${facId}/device-statistics`)
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>