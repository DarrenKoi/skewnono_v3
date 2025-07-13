<template>
  <div class="not-available bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button 
        icon="pi pi-arrow-left" 
        label="장비 현황으로 돌아가기"
        outlined
        size="large"
        class="mb-2"
        @click="$router.push({ name: 'equipment-status' })" 
      />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Skewnono 미지원 장비</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">Skewnono 시스템에서 지원하지 않는 장비 정보</div>
      </div>
    </div>

    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <h2 class="text-2xl font-semibold mb-6">Skewnono 미지원 장비</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card>
          <template #title>레거시 장비 D</template>
          <template #content>
            <div class="flex items-center gap-2 mb-2">
              <Badge value="미지원" severity="secondary" />
              <span class="text-sm text-surface-600">수동 관리 필요</span>
            </div>
            <p class="text-sm">담당자: 홍길동</p>
            <p class="text-sm">연락처: ext.1234</p>
          </template>
        </Card>
        
        <Card>
          <template #title>외부 장비 E</template>
          <template #content>
            <div class="flex items-center gap-2 mb-2">
              <Badge value="외부관리" severity="secondary" />
              <span class="text-sm text-surface-600">제3자 관리</span>
            </div>
            <p class="text-sm">관리업체: ABC Tech</p>
            <p class="text-sm">연락처: 02-1234-5678</p>
          </template>
        </Card>
      </div>
      
      <div class="mt-6 p-4 bg-surface-100 dark:bg-surface-800 rounded-lg">
        <div class="flex items-start gap-3">
          <i class="pi pi-info-circle text-surface-600 mt-1"></i>
          <div>
            <h4 class="font-medium text-surface-900 dark:text-surface-0">안내사항</h4>
            <p class="text-sm text-surface-600 dark:text-surface-300 mt-1">
              이 장비들은 Skewnono 시스템에서 직접 제어할 수 없습니다. 
              각 담당자 또는 관리업체에 직접 연락하여 상태를 확인하세요.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// This component will handle not available equipment data from Flask API
// API endpoint: /api/equipment/not_available
</script>

<style scoped>
/* Component-specific styles if needed */
</style>