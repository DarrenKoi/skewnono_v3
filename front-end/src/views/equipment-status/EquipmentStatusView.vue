<template>
  <div class="equipment-status bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">장비 현황</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">장비 상태 및 보관 정보를 확인하세요</div>
    </div>
    
    <!-- Selection Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(option, index) in statusOptions"
        :key="index"
        class="shadow-sm rounded-2xl p-4 cursor-pointer bg-surface-0 dark:bg-surface-900 border border-transparent transition-all duration-200 hover:border-primary hover:shadow-md"
        @click="navigateToSection(index)"
      >
        <div class="flex items-center justify-center mb-4">
          <i :class="option.icon" class="text-4xl text-primary"></i>
        </div>
        <div class="p-2 flex flex-col items-center gap-3">
          <div class="flex flex-col gap-2 w-full">
            <div class="text-surface-900 dark:text-surface-0 text-lg font-semibold text-center">{{ option.title }}</div>
            <div class="text-surface-500 dark:text-surface-300 text-sm leading-normal text-center" v-html="option.description" />
          </div>
          <div class="flex gap-2">
            <span v-for="(tag, tagIndex) in option.tags" :key="tagIndex" class="bg-slate-100 dark:bg-slate-800 px-2 py-1 text-xs rounded-lg">
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const statusOptions = [
  {
    title: 'Current Status',
    description: '현재 운영 중인<br>장비 상태 확인',
    icon: 'pi pi-desktop',
    tags: ['실시간', '모니터링'],
    route: 'equipment-current-status'
  },
  {
    title: 'Storage',
    description: '보관 도구 및<br>재고 관리',
    icon: 'pi pi-box',
    tags: ['재고', '관리'],
    route: 'equipment-storage'
  },
  {
    title: 'Not Available',
    description: 'Skewnono 미지원<br>장비 정보',
    icon: 'pi pi-exclamation-triangle',
    tags: ['미지원', '수동관리'],
    route: 'equipment-not-available'
  }
]

// Function to handle card navigation
const navigateToSection = (index) => {
  const option = statusOptions[index]
  if (option.route) {
    router.push({ name: option.route })
  }
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>