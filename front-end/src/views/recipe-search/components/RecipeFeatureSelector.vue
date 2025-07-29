<template>
  <div class="recipe-feature-selector">
    <!-- Selection Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div
        v-for="(option, index) in recipeOptions"
        :key="index"
        class="shadow-sm rounded-2xl p-4 bg-surface-0 dark:bg-surface-900 border transition-all duration-200"
        :class="{
          'cursor-pointer': !option.disabled,
          'opacity-50 cursor-not-allowed': option.disabled,
          'border-primary shadow-md': selectedSearchType === index && !option.disabled,
          'border-transparent hover:border-primary hover:shadow-md': selectedSearchType !== index && !option.disabled
        }"
        @click="!option.disabled ? selectSearchType(index) : null"
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
        <!-- Loading State -->
        <div v-if="isLoading" class="flex items-center justify-center py-8">
          <i class="pi pi-spinner pi-spin text-2xl text-primary"></i>
          <span class="ml-3 text-surface-600 dark:text-surface-400">Recipe 목록을 불러오는 중...</span>
        </div>
        
        <!-- Error State -->
        <div v-else-if="error" class="flex items-center justify-center py-8 text-red-500">
          <i class="pi pi-exclamation-triangle text-2xl"></i>
          <span class="ml-3">Recipe 목록을 불러오는데 실패했습니다.</span>
        </div>
        
        <!-- Recipe Search Input -->
        <div v-else class="flex flex-col gap-3">
          <AutoComplete 
            v-model="selectedRecipe" 
            :suggestions="filteredRecipes"
            :forceSelection="true"
            @complete="searchRecipe"
            :placeholder="getSearchPlaceholder()"
            class="w-full"
            :dropdown="true"
            :minLength="1"
            :disabled="recipeDatabase.length === 0"
          />
          <small class="text-surface-500 dark:text-surface-400">
            * {{ getSearchDescription() }}
            <span v-if="recipeDatabase.length === 0" class="text-orange-500">
              (사용 가능한 Recipe가 없습니다)
            </span>
          </small>
        </div>
        
        <!-- Additional Fields based on search type -->
        <div v-if="recipeOptions[selectedSearchType]?.route === 'measurement-history' && selectedRecipe" class="flex flex-col gap-3">
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
        <div v-if="selectedSearchType !== null && !isLoading && !error" class="flex pt-4">
          <Button 
            :label="getActionLabel()"
            :icon="getActionIcon()"
            @click="executeAction"
            :disabled="!canExecuteAction || recipeDatabase.length === 0"
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

const props = defineProps({
  toolType: {
    type: String,
    required: true,
    validator: (value) => ['cd-sem', 'hv-sem', 'verity', 'provision'].includes(value)
  },
  recipeList: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: [Object, String],
    default: null
  }
})

const router = useRouter()
const route = useRoute()

// Search-related reactive data
const selectedSearchType = ref(null)
const selectedRecipe = ref(null)
const filteredRecipes = ref([])
const dateRange = ref(null)

// Use recipe data from props (fetched from API)
const recipeDatabase = computed(() => props.recipeList)

// Tool-specific recipe options configuration
const toolOptionsMap = {
  'cd-sem': [
    {
      title: 'Recipe 열기',
      description: 'Recipe 설정 상태를<br>확인할 수 있습니다',
      icon: 'pi pi-folder-open',
      tags: ['설정', '확인'],
      route: 'open'
    },
    {
      title: '횡전개 체크',
      description: 'Recipe의 횡전개 여부와<br>Version을 체크할 수 있습니다',
      icon: 'pi pi-check-circle',
      tags: ['버전', '체크'],
      route: 'horizontal-check'
    },
    {
      title: 'Meas. History',
      description: '측정 기록을<br>확인할 수 있습니다',
      icon: 'pi pi-chart-line',
      tags: ['측정', '기록'],
      route: 'measurement-history'
    }
  ],
  'hv-sem': [
    {
      title: 'Recipe 열기',
      description: 'Recipe 설정 상태를<br>확인할 수 있습니다',
      icon: 'pi pi-folder-open',
      tags: ['설정', '확인'],
      route: 'open'
    },
    {
      title: '횡전개 체크',
      description: 'Recipe의 횡전개 여부와<br>Version을 체크할 수 있습니다',
      icon: 'pi pi-check-circle',
      tags: ['버전', '체크'],
      route: 'horizontal-check'
    },
    {
      title: 'Meas. History',
      description: '측정 기록을<br>확인할 수 있습니다',
      icon: 'pi pi-chart-line',
      tags: ['측정', '기록'],
      route: 'measurement-history'
    }
  ],
  // Placeholder for future verity features
  'verity': [
    {
      title: 'Coming Soon',
      description: 'VeritySEM features<br>will be added here',
      icon: 'pi pi-clock',
      tags: ['개발중'],
      route: null,
      disabled: true
    }
  ],
  // Placeholder for future provision features
  'provision': [
    {
      title: 'Coming Soon',
      description: 'Provision features<br>will be added here',
      icon: 'pi pi-clock',
      tags: ['개발중'],
      route: null,
      disabled: true
    }
  ]
}

// Get recipe options based on current tool type
const recipeOptions = computed(() => {
  return toolOptionsMap[props.toolType] || []
})

// Search type selection
const selectSearchType = (index) => {
  const option = recipeOptions.value[index]
  if (option.disabled) return
  
  selectedSearchType.value = index
  selectedRecipe.value = null
  
  // Set default date range for measurement history (1 month from today)
  // Check by route name instead of index to be tool-agnostic
  if (option.route === 'measurement-history') {
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
  filteredRecipes.value = recipeDatabase.value.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

// Get search placeholder based on selected type
const getSearchPlaceholder = () => {
  if (selectedSearchType.value === null) return ''
  const option = recipeOptions.value[selectedSearchType.value]
  if (!option) return 'Recipe 이름을 입력하세요...'
  
  const placeholderMap = {
    'open': 'Recipe 이름을 입력하세요...',
    'horizontal-check': '횡전개 체크할 Recipe를 입력하세요...',
    'measurement-history': '측정 기록을 조회할 Recipe를 입력하세요...'
  }
  return placeholderMap[option.route] || 'Recipe 이름을 입력하세요...'
}

// Get search description based on selected type
const getSearchDescription = () => {
  if (selectedSearchType.value === null) return ''
  const option = recipeOptions.value[selectedSearchType.value]
  if (!option) return ''
  
  const descriptionMap = {
    'open': 'Recipe를 검색하고 선택하여 설정 상태를 확인하세요',
    'horizontal-check': 'Recipe를 검색하고 선택하여 횡전개 여부와 버전을 체크하세요',
    'measurement-history': 'Recipe를 검색하고 선택한 후 기간을 설정하여 측정 기록을 조회하세요'
  }
  return descriptionMap[option.route] || ''
}

// Get action label based on selected type
const getActionLabel = () => {
  if (selectedSearchType.value === null) return ''
  const option = recipeOptions.value[selectedSearchType.value]
  if (!option) return ''
  
  const labelMap = {
    'open': 'Recipe 열기',
    'horizontal-check': '횡전개 체크 실행',
    'measurement-history': '측정 기록 조회'
  }
  return labelMap[option.route] || ''
}

// Get action icon based on selected type
const getActionIcon = () => {
  if (selectedSearchType.value === null) return ''
  const option = recipeOptions.value[selectedSearchType.value]
  if (!option) return ''
  
  const iconMap = {
    'open': 'pi pi-external-link',
    'horizontal-check': 'pi pi-check-square',
    'measurement-history': 'pi pi-history'
  }
  return iconMap[option.route] || ''
}

// Check if action can be executed
const canExecuteAction = computed(() => {
  if (selectedSearchType.value === null || !selectedRecipe.value) return false
  const option = recipeOptions.value[selectedSearchType.value]
  if (!option || option.disabled) return false
  
  // Check if measurement history requires date range
  if (option.route === 'measurement-history') {
    return dateRange.value && dateRange.value.length === 2
  }
  return true
})

// Execute action by navigating to sub-route
const executeAction = () => {
  if (!canExecuteAction.value) return
  
  const option = recipeOptions.value[selectedSearchType.value]
  if (option && option.route && !option.disabled) {
    // Store the selected recipe and date range in sessionStorage for the target page
    sessionStorage.setItem('selectedRecipe', selectedRecipe.value)
    if (dateRange.value) {
      sessionStorage.setItem('dateRange', JSON.stringify(dateRange.value))
    }
    
    // Navigate to the feature view
    const facId = route.params.fac_id || 'R3'
    router.push(`/${facId}/recipe-search/${props.toolType}/${option.route}`)
  }
}
</script>

<style scoped>
/* Component-specific styles if needed */
</style>