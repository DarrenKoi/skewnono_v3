<template>
  <div class="fail-issue bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <!-- Back Button -->
    <div class="mb-6">
      <Button 
        label="장비 선택으로 돌아가기" 
        icon="pi pi-arrow-left" 
        @click="$router.back()" 
        severity="secondary" 
        outlined 
      />
    </div>
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">HV-SEM 불량 이슈</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">
        HV-SEM 불량 이슈 기능은 준비 중입니다
      </div>
    </div>
  </div>
</template>

<script setup>
import Button from 'primevue/button'

// HV-SEM fail issue implementation will be added here
</script>

<style scoped>
/* Page-specific styles if needed */
</style>