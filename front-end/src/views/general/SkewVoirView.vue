<template>
  <div class="skewboa">
    <h1 class="text-4xl font-bold mb-4">스큐보아</h1>
    <p class="text-lg text-surface-600">
      스큐보아 페이지입니다. 스큐보아 관련 기능을 사용할 수 있습니다.
    </p>
    <div class="mt-4 bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg border border-blue-200 dark:border-blue-800">
      <p class="text-blue-700 dark:text-blue-300">
        <i class="pi pi-info-circle mr-2"></i>
        Currently viewing data for <span class="font-bold">{{ selectedFab }}</span> Fab
      </p>
    </div>
  </div>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useFabStore } from '@/stores/fab'

const fabStore = useFabStore()
const { selectedFab } = storeToRefs(fabStore)
</script>

<style scoped>
/* Page-specific styles if needed */
</style>
