<template>
  <div class="recipe-search bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
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
        :class="{
          'border-transparent': selected !== index,
          'border-primary shadow-md': selected === index
        }"
        @click="selected = index"
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

    <!-- Content Display -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <!-- Search Section -->
      <div class="flex flex-col gap-6">
        <h2 class="text-2xl font-semibold">{{ recipeOptions[selected].title }}</h2>
        
        <!-- AutoComplete Search -->
        <div class="flex flex-col gap-3">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">Recipe 검색</label>
          <AutoComplete 
            v-model="selectedRecipe" 
            :suggestions="filteredRecipes"
            :forceSelection="true"
            @complete="searchRecipe"
            placeholder="Recipe 이름을 입력하세요..."
            class="w-full"
            :dropdown="true"
            :minLength="1"
          />
          <small class="text-surface-500 dark:text-surface-400">
            * Recipe를 검색하고 목록에서 선택하세요
          </small>
        </div>

        <!-- Action Button based on selected option -->
        <div class="flex pt-4">
          <Button 
            :label="recipeOptions[selected].buttonLabel" 
            :icon="recipeOptions[selected].buttonIcon"
            @click="executeAction"
            :disabled="!selectedRecipe"
            class="w-full sm:w-auto"
          />
        </div>

        <!-- Selected Recipe Info -->
        <div v-if="selectedRecipe" class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
          <div class="flex items-center gap-3">
            <i class="pi pi-info-circle text-primary"></i>
            <div>
              <h3 class="font-semibold text-surface-900 dark:text-surface-0">선택된 Recipe</h3>
              <p class="text-surface-700 dark:text-surface-200 mt-1">{{ selectedRecipe }}</p>
            </div>
          </div>
        </div>

        <!-- Results Section -->
        <div v-if="actionResult" class="mt-4">
          <Message :severity="actionResult.severity" :closable="true" @close="actionResult = null">
            {{ actionResult.message }}
          </Message>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selected = ref(0)
const selectedRecipe = ref(null)
const filteredRecipes = ref([])
const actionResult = ref(null)

// Recipe options configuration
const recipeOptions = [
  {
    title: 'Recipe 열기',
    description: 'Recipe 설정 상태를<br>확인할 수 있습니다',
    icon: 'pi pi-folder-open',
    tags: ['설정', '확인'],
    buttonLabel: 'Recipe 열기',
    buttonIcon: 'pi pi-external-link',
    action: 'open'
  },
  {
    title: '횡전개 체크',
    description: 'Recipe의 횡전개 여부와<br>Version을 체크할 수 있습니다',
    icon: 'pi pi-check-circle',
    tags: ['버전', '체크'],
    buttonLabel: '횡전개 체크 실행',
    buttonIcon: 'pi pi-check-square',
    action: 'horizontal'
  },
  {
    title: 'Meas. History',
    description: '측정 기록을<br>확인할 수 있습니다',
    icon: 'pi pi-chart-line',
    tags: ['측정', '기록'],
    buttonLabel: '측정 기록 조회',
    buttonIcon: 'pi pi-history',
    action: 'history'
  }
]

// Sample recipe data - replace with actual API call
const recipeDatabase = [
  'RECIPE_001_STANDARD',
  'RECIPE_002_ADVANCED',
  'RECIPE_003_CUSTOM',
  'RECIPE_004_TEST',
  'RECIPE_005_PRODUCTION',
  'RECIPE_006_SPECIAL',
  'RECIPE_007_MAINTENANCE',
  'RECIPE_008_CALIBRATION',
  'RECIPE_009_VALIDATION',
  'RECIPE_010_EMERGENCY'
]

// Search recipes based on input
const searchRecipe = (event) => {
  const query = event.query.toLowerCase()
  filteredRecipes.value = recipeDatabase.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

// Execute action based on selected option
const executeAction = () => {
  if (!selectedRecipe.value) return
  
  const action = recipeOptions[selected.value].action
  
  switch (action) {
    case 'open':
      openRecipe()
      break
    case 'horizontal':
      checkHorizontalDeploy()
      break
    case 'history':
      viewMeasurementHistory()
      break
  }
}

// Action: Open Recipe
const openRecipe = () => {
  actionResult.value = {
    severity: 'success',
    message: `Recipe를 열고 있습니다: ${selectedRecipe.value}`
  }
  
  // TODO: Implement actual recipe opening logic
  console.log('Opening recipe:', selectedRecipe.value)
}

// Action: Check Horizontal Deploy
const checkHorizontalDeploy = () => {
  actionResult.value = {
    severity: 'info',
    message: `횡전개 체크를 진행합니다: ${selectedRecipe.value}`
  }
  
  // TODO: Implement horizontal deploy check logic
  console.log('Checking horizontal deploy for:', selectedRecipe.value)
}

// Action: View Measurement History
const viewMeasurementHistory = () => {
  actionResult.value = {
    severity: 'warn',
    message: `측정 기록을 조회합니다: ${selectedRecipe.value}`
  }
  
  // TODO: Implement measurement history view logic
  console.log('Viewing measurement history for:', selectedRecipe.value)
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>