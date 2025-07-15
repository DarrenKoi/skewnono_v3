<template>
  <div class="recipe-open bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Recipe 열기</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">Recipe 설정 상태를 확인할 수 있습니다</div>
    </div>

    <!-- Content Display -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex flex-col gap-6">
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

        <!-- Action Button -->
        <div class="flex pt-4">
          <Button 
            label="Recipe 열기"
            icon="pi pi-external-link"
            @click="openRecipe"
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

        <!-- Recipe Details (shown after opening) -->
        <div v-if="recipeDetails" class="mt-6">
          <h3 class="text-xl font-semibold mb-4">Recipe 상세 정보</h3>
          <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p class="text-surface-600 dark:text-surface-400">Recipe ID</p>
                <p class="font-semibold">{{ recipeDetails.id }}</p>
              </div>
              <div>
                <p class="text-surface-600 dark:text-surface-400">버전</p>
                <p class="font-semibold">{{ recipeDetails.version }}</p>
              </div>
              <div>
                <p class="text-surface-600 dark:text-surface-400">작성일</p>
                <p class="font-semibold">{{ recipeDetails.createdAt }}</p>
              </div>
              <div>
                <p class="text-surface-600 dark:text-surface-400">상태</p>
                <p class="font-semibold">{{ recipeDetails.status }}</p>
              </div>
            </div>
            <div class="mt-4">
              <p class="text-surface-600 dark:text-surface-400">설명</p>
              <p class="mt-1">{{ recipeDetails.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const selectedRecipe = ref(null)
const filteredRecipes = ref([])
const actionResult = ref(null)
const recipeDetails = ref(null)

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

// Action: Open Recipe
const openRecipe = async () => {
  if (!selectedRecipe.value) return
  
  actionResult.value = {
    severity: 'info',
    message: `Recipe를 열고 있습니다: ${selectedRecipe.value}`
  }
  
  // Simulate API call
  setTimeout(() => {
    // Mock recipe details
    recipeDetails.value = {
      id: selectedRecipe.value,
      version: '1.2.3',
      createdAt: '2024-01-15',
      status: 'Active',
      description: '이 Recipe는 표준 생산 공정을 위한 설정입니다.'
    }
    
    actionResult.value = {
      severity: 'success',
      message: `Recipe가 성공적으로 열렸습니다: ${selectedRecipe.value}`
    }
  }, 1000)
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>