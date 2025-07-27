<template>
  <div>
    <!-- Header with Back Button -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-semibold text-surface-900 dark:text-surface-0">Recipe 검색</h3>
      <Button 
        label="장비 선택으로 돌아가기" 
        icon="pi pi-arrow-left" 
        @click="goBack" 
        severity="secondary" 
        size="small"
        outlined 
      />
    </div>
    <!-- All Recipe Search Options -->
    <div class="space-y-6">
      <!-- Recipe Open Section -->
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
        <div class="mb-4">
          <div class="flex items-center gap-3 mb-2">
            <i class="pi pi-folder-open text-2xl text-primary"></i>
            <h3 class="text-lg font-semibold text-surface-900 dark:text-surface-0">Recipe 열기</h3>
          </div>
          <p class="text-surface-500 dark:text-surface-400 text-sm">Recipe 설정 상태를 확인할 수 있습니다</p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4">
          <AutoComplete 
            v-model="recipeOpenRecipe" 
            :suggestions="filteredRecipesOpen"
            :forceSelection="true"
            @complete="searchRecipeOpen"
            placeholder="HV-SEM Recipe 이름을 입력하세요..."
            class="flex-1"
            :dropdown="true"
            :minLength="1"
          />
          <Button 
            label="Recipe 열기"
            icon="pi pi-external-link"
            @click="openRecipe"
            :disabled="!recipeOpenRecipe"
            class="w-full sm:w-auto"
          />
        </div>
        
        <!-- Show Recipe Open Content -->
        <div v-if="showRecipeOpen && recipeOpenRecipe" class="mt-6 pt-6 border-t">
          <HvSemRecipeOpenView :recipe-name="recipeOpenRecipe" />
        </div>
      </div>

      <!-- Horizontal Check Section -->
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
        <div class="mb-4">
          <div class="flex items-center gap-3 mb-2">
            <i class="pi pi-check-circle text-2xl text-primary"></i>
            <h3 class="text-lg font-semibold text-surface-900 dark:text-surface-0">횡전개 체크</h3>
          </div>
          <p class="text-surface-500 dark:text-surface-400 text-sm">Recipe의 횡전개 여부와 Version을 체크할 수 있습니다</p>
        </div>
        
        <div class="flex flex-col sm:flex-row gap-4">
          <AutoComplete 
            v-model="horizontalCheckRecipe" 
            :suggestions="filteredRecipesHorizontal"
            :forceSelection="true"
            @complete="searchRecipeHorizontal"
            placeholder="횡전개 체크할 HV-SEM Recipe를 입력하세요..."
            class="flex-1"
            :dropdown="true"
            :minLength="1"
          />
          <Button 
            label="횡전개 체크 실행"
            icon="pi pi-check-square"
            @click="checkHorizontal"
            :disabled="!horizontalCheckRecipe"
            class="w-full sm:w-auto"
          />
        </div>
        
        <!-- Show Horizontal Check Content -->
        <div v-if="showHorizontalCheck && horizontalCheckRecipe" class="mt-6 pt-6 border-t">
          <HvSemRecipeHorizontalCheckView :recipe-name="horizontalCheckRecipe" />
        </div>
      </div>

      <!-- Measurement History Section -->
      <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
        <div class="mb-4">
          <div class="flex items-center gap-3 mb-2">
            <i class="pi pi-chart-line text-2xl text-primary"></i>
            <h3 class="text-lg font-semibold text-surface-900 dark:text-surface-0">Meas. History</h3>
          </div>
          <p class="text-surface-500 dark:text-surface-400 text-sm">측정 기록을 확인할 수 있습니다</p>
        </div>
        
        <div class="space-y-4">
          <div class="flex flex-col sm:flex-row gap-4">
            <AutoComplete 
              v-model="measurementHistoryRecipe" 
              :suggestions="filteredRecipesMeasurement"
              :forceSelection="true"
              @complete="searchRecipeMeasurement"
              placeholder="측정 기록을 조회할 HV-SEM Recipe를 입력하세요..."
              class="flex-1"
              :dropdown="true"
              :minLength="1"
            />
          </div>
          
          <div v-if="measurementHistoryRecipe" class="flex flex-col sm:flex-row gap-4">
            <Calendar 
              v-model="dateRange" 
              selectionMode="range" 
              :manualInput="false" 
              dateFormat="yy/mm/dd"
              placeholder="날짜 범위 선택"
              showIcon
              class="flex-1"
            />
            <Button 
              label="측정 기록 조회"
              icon="pi pi-history"
              @click="checkMeasurementHistory"
              :disabled="!measurementHistoryRecipe || !dateRange || dateRange.length !== 2"
              class="w-full sm:w-auto"
            />
          </div>
        </div>
        
        <!-- Show Measurement History Content -->
        <div v-if="showMeasurementHistory && measurementHistoryRecipe && dateRange" class="mt-6 pt-6 border-t">
          <HvSemRecipeMeasurementHistoryView :recipe-name="measurementHistoryRecipe" :date-range="dateRange" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import AutoComplete from 'primevue/autocomplete'
import Calendar from 'primevue/calendar'
import Button from 'primevue/button'
import HvSemRecipeOpenView from './HvSemRecipeOpenView.vue'
import HvSemRecipeHorizontalCheckView from './HvSemRecipeHorizontalCheckView.vue'
import HvSemRecipeMeasurementHistoryView from './HvSemRecipeMeasurementHistoryView.vue'

// Separate reactive data for each section
const recipeOpenRecipe = ref(null)
const horizontalCheckRecipe = ref(null)
const measurementHistoryRecipe = ref(null)
const dateRange = ref(null)

// Filtered suggestions for each autocomplete
const filteredRecipesOpen = ref([])
const filteredRecipesHorizontal = ref([])
const filteredRecipesMeasurement = ref([])

// Show/hide content for each section
const showRecipeOpen = ref(false)
const showHorizontalCheck = ref(false)
const showMeasurementHistory = ref(false)

// Sample HV-SEM recipe data - replace with actual API call
const recipeDatabase = [
  'HV_RECIPE_001_HIGH_RES',
  'HV_RECIPE_002_FAST_SCAN',
  'HV_RECIPE_003_DEEP_FOCUS',
  'HV_RECIPE_004_WIDE_FIELD',
  'HV_RECIPE_005_ANALYSIS',
  'HV_RECIPE_006_INSPECTION',
  'HV_RECIPE_007_CALIBRATION',
  'HV_RECIPE_008_MAINTENANCE'
]

// Recipe search functions for each autocomplete
const searchRecipeOpen = (event) => {
  const query = event.query.toLowerCase()
  filteredRecipesOpen.value = recipeDatabase.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

const searchRecipeHorizontal = (event) => {
  const query = event.query.toLowerCase()
  filteredRecipesHorizontal.value = recipeDatabase.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

const searchRecipeMeasurement = (event) => {
  const query = event.query.toLowerCase()
  filteredRecipesMeasurement.value = recipeDatabase.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

// Action functions for each section
const openRecipe = () => {
  if (recipeOpenRecipe.value) {
    showRecipeOpen.value = true
  }
}

const checkHorizontal = () => {
  if (horizontalCheckRecipe.value) {
    showHorizontalCheck.value = true
  }
}

const checkMeasurementHistory = () => {
  if (measurementHistoryRecipe.value && dateRange.value && dateRange.value.length === 2) {
    showMeasurementHistory.value = true
  }
}

// Go back function
const goBack = () => {
  window.history.back()
}

// Initialize date range on mount
onMounted(() => {
  const today = new Date()
  const oneMonthAgo = new Date()
  oneMonthAgo.setMonth(today.getMonth() - 1)
  dateRange.value = [oneMonthAgo, today]
})
</script>

<style scoped>
/* Component-specific styles if needed */
</style>