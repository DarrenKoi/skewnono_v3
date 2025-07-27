<template>
  <div class="recipe-search bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <!-- Back Button -->
    <Button 
      icon="pi pi-arrow-left" 
      label="장비 선택으로 도아가기" 
      outlined 
      size="large" 
      class="mb-2"
      @click="goBackToToolSelection" 
    />
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">HV-SEM Recipe 검색</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">HV-SEM Recipe 정보를 검색하고 조회하세요</div>
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
    
    <!-- Context-aware Search Bar -->
    <div v-if="selectedSearchType !== null" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex flex-col gap-6">
        <!-- Recipe Search Input -->
        <div class="flex flex-col gap-3">
          <AutoComplete 
            v-model="selectedRecipe" 
            :suggestions="filteredRecipes"
            :forceSelection="true"
            @complete="searchRecipe"
            :placeholder="getSearchPlaceholder()"
            class="w-full"
            :dropdown="true"
            :minLength="1"
          />
          <small class="text-surface-500 dark:text-surface-400">
            * {{ getSearchDescription() }}
          </small>
        </div>
        
        <!-- Additional Fields based on search type -->
        <div v-if="selectedSearchType === 2 && selectedRecipe" class="flex flex-col gap-3">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">기간 선택</label>
          <Calendar 
            v-model="dateRange" 
            selectionMode="range" 
            :manualInput="false" 
            dateFormat="yy/mm/dd"
            placeholder="날짜 범위 선택"
            showIcon
            class="w-full sm:w-auto"
          />
        </div>
        
        <!-- Action Button -->
        <div v-if="selectedSearchType !== null" class="flex pt-4">
          <Button 
            :label="getActionLabel()"
            :icon="getActionIcon()"
            @click="executeAction"
            :disabled="!canExecuteAction"
            class="w-full sm:w-auto"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'
import AutoComplete from 'primevue/autocomplete'
import Calendar from 'primevue/calendar'

const router = useRouter()
const route = useRoute()

// Search-related reactive data
const selectedSearchType = ref(null)
const selectedRecipe = ref(null)
const filteredRecipes = ref([])
const dateRange = ref(null)

// Sample HV-SEM recipe data - replace with actual API call
const recipeDatabase = [
  'HV_RECIPE_001_STANDARD',
  'HV_RECIPE_002_ADVANCED',
  'HV_RECIPE_003_CUSTOM',
  'HV_RECIPE_004_TEST',
  'HV_RECIPE_005_PRODUCTION',
  'HV_RECIPE_006_SPECIAL',
  'HV_RECIPE_007_MAINTENANCE',
  'HV_RECIPE_008_CALIBRATION',
  'HV_RECIPE_009_VALIDATION',
  'HV_RECIPE_010_EMERGENCY'
]

// Recipe options configuration
const recipeOptions = [
  {
    title: 'Recipe 열기',
    description: 'HV-SEM Recipe 설정 상태를<br>확인할 수 있습니다',
    icon: 'pi pi-folder-open',
    tags: ['설정', '확인'],
    route: 'hv-sem-recipe-open'
  },
  {
    title: '횡전개 체크',
    description: 'HV-SEM Recipe의 횡전개 여부와<br>Version을 체크할 수 있습니다',
    icon: 'pi pi-check-circle',
    tags: ['버전', '체크'],
    route: 'hv-sem-recipe-horizontal-check'
  },
  {
    title: 'Meas. History',
    description: 'HV-SEM 측정 기록을<br>확인할 수 있습니다',
    icon: 'pi pi-chart-line',
    tags: ['측정', '기록'],
    route: 'hv-sem-recipe-measurement-history'
  }
]

// Search type selection
const selectSearchType = (index) => {
  selectedSearchType.value = index
  selectedRecipe.value = null
  
  // Set default date range for measurement history (1 month from today)
  if (index === 2) {
    const today = new Date()
    const oneMonthAgo = new Date()
    oneMonthAgo.setMonth(today.getMonth() - 1)
    dateRange.value = [oneMonthAgo, today]
  } else {
    dateRange.value = null
  }
}

// Recipe search functionality
const searchRecipe = (event) => {
  const query = event.query.toLowerCase()
  filteredRecipes.value = recipeDatabase.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

// Get search placeholder based on selected type
const getSearchPlaceholder = () => {
  if (selectedSearchType.value === null) return ''
  const placeholders = {
    0: 'HV-SEM Recipe 이름을 입력하세요...',
    1: '횡전개 체크할 HV-SEM Recipe를 입력하세요...',
    2: '측정 기록을 조회할 HV-SEM Recipe를 입력하세요...'
  }
  return placeholders[selectedSearchType.value] || 'Recipe 이름을 입력하세요...'
}

// Get search description based on selected type
const getSearchDescription = () => {
  if (selectedSearchType.value === null) return ''
  const descriptions = {
    0: 'HV-SEM Recipe를 검색하고 선택하여 설정 상태를 확인하세요',
    1: 'HV-SEM Recipe를 검색하고 선택하여 횡전개 여부와 버전을 체크하세요',
    2: 'HV-SEM Recipe를 검색하고 선택한 후 기간을 설정하여 측정 기록을 조회하세요'
  }
  return descriptions[selectedSearchType.value] || ''
}

// Get action label based on selected type
const getActionLabel = () => {
  if (selectedSearchType.value === null) return ''
  const labels = {
    0: 'Recipe 열기',
    1: '횡전개 체크 실행',
    2: '측정 기록 조회'
  }
  return labels[selectedSearchType.value] || ''
}

// Get action icon based on selected type
const getActionIcon = () => {
  if (selectedSearchType.value === null) return ''
  const icons = {
    0: 'pi pi-external-link',
    1: 'pi pi-check-square',
    2: 'pi pi-history'
  }
  return icons[selectedSearchType.value] || ''
}

// Check if action can be executed
const canExecuteAction = computed(() => {
  if (selectedSearchType.value === null || !selectedRecipe.value) return false
  if (selectedSearchType.value === 2) {
    return dateRange.value && dateRange.value.length === 2
  }
  return true
})

// Go back to tool selection
const goBackToToolSelection = () => {
  const facId = route.params.fac_id || 'R3'
  router.push(`/${facId}/recipe-search`)
}

// Execute action by navigating to sub-route
const executeAction = () => {
  if (!canExecuteAction.value) return
  
  const option = recipeOptions[selectedSearchType.value]
  if (option.route) {
    // Store the selected recipe and date range in sessionStorage for the target page
    sessionStorage.setItem('selectedRecipe', selectedRecipe.value)
    if (dateRange.value) {
      sessionStorage.setItem('dateRange', JSON.stringify(dateRange.value))
    }
    
    // Navigate to the sub-route
    router.push({ name: option.route })
  }
}

</script>

<style scoped>
/* Page-specific styles if needed */
</style>