<template>
  <div class="recipe-search bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <!-- Back Button -->
    <Button 
      icon="pi pi-arrow-left" 
      label="장비 선택으로 돌아가기" 
      outlined 
      size="large" 
      class="mb-2"
      @click="goBackToToolSelection" 
    />
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Recipe 검색</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">Recipe 정보를 검색하고 조회하세요</div>
    </div>
    
    <!-- Selection Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div
        v-for="(option, index) in recipeOptions"
        :key="index"
        class="shadow-sm rounded-2xl p-4 cursor-pointer bg-surface-0 dark:bg-surface-900 border transition-all duration-200"
        :class="selectedSearchType === index ? 'border-primary shadow-md' : 'border-transparent hover:border-primary hover:shadow-md'"
        @click="selectSearchType(index)"
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
    
    <!-- Confirm Button -->
    <div v-if="selectedSearchType !== null" class="flex justify-center mt-8">
      <Button 
        label="확인"
        icon="pi pi-check"
        @click="navigateToSelectedPage"
        size="large"
        class="px-8"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'

const router = useRouter()
const route = useRoute()

// Search type selection
const selectedSearchType = ref(null)

// Recipe options configuration
const recipeOptions = [
  {
    title: 'Recipe 열기',
    description: 'Recipe 설정 상태를<br>확인할 수 있습니다',
    icon: 'pi pi-folder-open',
    tags: ['설정', '확인'],
    route: 'recipe-open'
  },
  {
    title: '횡전개 체크',
    description: 'Recipe의 횡전개 여부와<br>Version을 체크할 수 있습니다',
    icon: 'pi pi-check-circle',
    tags: ['버전', '체크'],
    route: 'recipe-horizontal-check'
  },
  {
    title: 'Meas. History',
    description: '측정 기록을<br>확인할 수 있습니다',
    icon: 'pi pi-chart-line',
    tags: ['측정', '기록'],
    route: 'recipe-measurement-history'
  }
]

// Search type selection
const selectSearchType = (index) => {
  selectedSearchType.value = index
}

// Go back to tool selection
const goBackToToolSelection = () => {
  const facId = route.params.fac_id || 'R3'
  router.push(`/${facId}/recipe-search`)
}

// Navigate to selected page
const navigateToSelectedPage = () => {
  if (selectedSearchType.value === null) return
  
  const option = recipeOptions[selectedSearchType.value]
  if (option.route) {
    // Navigate to the sub-route
    router.push({ name: option.route })
  }
}

</script>

<style scoped>
/* Page-specific styles if needed */
</style>