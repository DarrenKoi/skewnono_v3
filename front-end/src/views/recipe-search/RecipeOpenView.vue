<template>
  <div class="recipe-open bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button 
        icon="pi pi-arrow-left" 
        label="Recipe 검색으로 돌아가기"
        outlined
        size="large"
        class="mb-2"
        @click="$router.push({ name: 'recipe-search' })" 
      />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Recipe 열기</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">Recipe 설정 상태를 확인할 수 있습니다</div>
      </div>
    </div>

    <!-- Content Display -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex flex-col gap-6">
        <!-- Selected Recipe Display -->
        <div class="flex flex-col gap-3">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">선택된 Recipe</label>
          <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-3 border">
            <p class="text-surface-700 dark:text-surface-200">
              {{ selectedRecipe || 'Recipe 검색 페이지에서 선택하세요' }}
            </p>
          </div>
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
import { ref, onMounted } from 'vue'

const selectedRecipe = ref(null)
const actionResult = ref(null)
const recipeDetails = ref(null)

// Load selected recipe from sessionStorage and auto-execute if present
onMounted(() => {
  const storedRecipe = sessionStorage.getItem('selectedRecipe')
  if (storedRecipe) {
    selectedRecipe.value = storedRecipe
    sessionStorage.removeItem('selectedRecipe')
    // Auto-execute the action
    openRecipe()
  }
})

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