<template>
  <div class="hv-sem-recipe-content">
    <!-- HV-SEM Recipe Search Interface -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="flex flex-col gap-6">
        <!-- Search Input -->
        <div class="flex flex-col gap-3">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">HV-SEM Recipe 검색</label>
          <AutoComplete 
            v-model="selectedRecipe" 
            :suggestions="filteredRecipes"
            :forceSelection="true"
            @complete="searchRecipe"
            placeholder="HV-SEM Recipe 이름을 입력하세요..."
            class="w-full"
            :dropdown="true"
            :minLength="1"
          />
          <small class="text-surface-500 dark:text-surface-400">
            * HV-SEM 전용 레시피를 검색하고 선택하세요
          </small>
        </div>

        <!-- Equipment Selection -->
        <div class="flex flex-col gap-3">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">장비 선택</label>
          <Dropdown 
            v-model="selectedEquipment" 
            :options="hvSemEquipments" 
            optionLabel="name"
            optionValue="id"
            placeholder="HV-SEM 장비를 선택하세요"
            class="w-full"
          />
        </div>

        <!-- Action Buttons -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <Button 
            label="Recipe 정보 조회"
            icon="pi pi-info-circle"
            @click="viewRecipeInfo"
            :disabled="!selectedRecipe"
            class="w-full"
          />
          <Button 
            label="Recipe 실행"
            icon="pi pi-play"
            @click="executeRecipe"
            :disabled="!selectedRecipe || !selectedEquipment"
            severity="success"
            class="w-full"
          />
        </div>
      </div>
    </div>

    <!-- Recipe Information Display -->
    <div v-if="recipeInfo" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <h3 class="text-xl font-semibold mb-4 text-surface-900 dark:text-surface-0">Recipe 정보</h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <h4 class="font-semibold mb-2 text-surface-700 dark:text-surface-300">기본 정보</h4>
          <div class="space-y-2 text-sm">
            <div><strong>Recipe ID:</strong> {{ recipeInfo.id }}</div>
            <div><strong>버전:</strong> {{ recipeInfo.version }}</div>
            <div><strong>생성일:</strong> {{ recipeInfo.createDate }}</div>
            <div><strong>수정일:</strong> {{ recipeInfo.modifyDate }}</div>
          </div>
        </div>
        
        <div>
          <h4 class="font-semibold mb-2 text-surface-700 dark:text-surface-300">설정 정보</h4>
          <div class="space-y-2 text-sm">
            <div><strong>전압:</strong> {{ recipeInfo.voltage }} kV</div>
            <div><strong>빔 전류:</strong> {{ recipeInfo.beamCurrent }} pA</div>
            <div><strong>배율:</strong> {{ recipeInfo.magnification }}x</div>
            <div><strong>픽셀 크기:</strong> {{ recipeInfo.pixelSize }} nm</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import AutoComplete from 'primevue/autocomplete'
import Dropdown from 'primevue/dropdown'
import Button from 'primevue/button'

// Reactive data
const selectedRecipe = ref(null)
const selectedEquipment = ref(null)
const filteredRecipes = ref([])
const recipeInfo = ref(null)

// Sample HV-SEM recipe data
const hvSemRecipes = [
  'HV_RECIPE_001_HIGH_RES',
  'HV_RECIPE_002_FAST_SCAN',
  'HV_RECIPE_003_DEEP_FOCUS',
  'HV_RECIPE_004_WIDE_FIELD',
  'HV_RECIPE_005_ANALYSIS',
  'HV_RECIPE_006_INSPECTION',
  'HV_RECIPE_007_CALIBRATION',
  'HV_RECIPE_008_MAINTENANCE'
]

// Sample HV-SEM equipment data
const hvSemEquipments = [
  { id: 'HVSEM_001', name: 'HV-SEM-A (고해상도)' },
  { id: 'HVSEM_002', name: 'HV-SEM-B (고속스캔)' },
  { id: 'HVSEM_003', name: 'HV-SEM-C (분석전용)' },
  { id: 'HVSEM_004', name: 'HV-SEM-D (검사전용)' }
]

// Recipe search functionality
const searchRecipe = (event) => {
  const query = event.query.toLowerCase()
  filteredRecipes.value = hvSemRecipes.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

// View recipe information
const viewRecipeInfo = () => {
  if (!selectedRecipe.value) return
  
  // Simulate recipe information retrieval
  recipeInfo.value = {
    id: selectedRecipe.value,
    version: '1.2.3',
    createDate: '2024-01-15',
    modifyDate: '2024-07-15',
    voltage: '15.0',
    beamCurrent: '50',
    magnification: '100000',
    pixelSize: '2.5'
  }
}

// Execute recipe
const executeRecipe = () => {
  if (!selectedRecipe.value || !selectedEquipment.value) return
  
  // Simulate recipe execution
  alert(`HV-SEM Recipe "${selectedRecipe.value}"을(를) ${selectedEquipment.value} 장비에서 실행합니다.`)
}
</script>

<style scoped>
/* Component-specific styles if needed */
</style>