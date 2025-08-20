<template>
  <div class="recipe-horizontal-check bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button 
        icon="pi pi-arrow-left" 
        label="Recipe 선택으로 돌아가기"
        outlined
        size="large"
        class="mb-2"
        @click="goBackToRecipeSearch()" 
      />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">횡전개 체크</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">Recipe의 횡전개 여부와 Version을 체크할 수 있습니다</div>
      </div>
    </div>

    <!-- Recipe Search Bar -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="flex flex-col gap-4">
        <div class="flex items-center justify-between">
          <label class="text-surface-900 dark:text-surface-0 font-semibold">Recipe 검색</label>
          <div v-if="selectedRecipe" class="flex items-center gap-2">
            <span class="text-surface-500 dark:text-surface-400 text-sm">현재 선택:</span>
            <Tag :value="selectedRecipe" severity="success" />
          </div>
        </div>
        <div class="flex gap-3">
          <AutoComplete 
            v-model="selectedRecipe" 
            :suggestions="filteredRecipes"
            :forceSelection="true"
            @complete="searchRecipe"
            placeholder="횡전개 체크할 Recipe를 입력하세요..."
            class="flex-1"
            :dropdown="true"
            :minLength="1"
          />
          <Button 
            label="횡전개 체크 실행"
            icon="pi pi-check-square"
            @click="checkHorizontalDeploy"
            :disabled="!selectedRecipe"
            :loading="isChecking"
          />
        </div>
        <small class="text-surface-500 dark:text-surface-400">
          * Recipe를 검색하고 선택하여 횡전개 여부와 버전을 체크하세요
        </small>
      </div>
    </div>

    <!-- Content Display -->
    <div v-if="checkResult" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex flex-col gap-6">

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

        <!-- Horizontal Deploy Check Results -->
        <div v-if="checkResults" class="mt-6">
          <h3 class="text-xl font-semibold mb-4">횡전개 체크 결과</h3>
          
          <!-- Summary Card -->
          <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4 mb-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="text-center">
                <p class="text-surface-600 dark:text-surface-400">총 장비 수</p>
                <p class="text-2xl font-bold text-primary">{{ checkResults.totalEquipment }}</p>
              </div>
              <div class="text-center">
                <p class="text-surface-600 dark:text-surface-400">동일 버전</p>
                <p class="text-2xl font-bold text-green-500">{{ checkResults.sameVersion }}</p>
              </div>
              <div class="text-center">
                <p class="text-surface-600 dark:text-surface-400">다른 버전</p>
                <p class="text-2xl font-bold text-orange-500">{{ checkResults.differentVersion }}</p>
              </div>
            </div>
          </div>

          <!-- Detailed Results Table -->
          <DataTable :value="checkResults.details" class="p-datatable-sm">
            <Column field="equipment" header="장비명"></Column>
            <Column field="version" header="버전">
              <template #body="slotProps">
                <Tag :severity="slotProps.data.version === checkResults.baseVersion ? 'success' : 'warning'">
                  {{ slotProps.data.version }}
                </Tag>
              </template>
            </Column>
            <Column field="lastUpdate" header="최종 업데이트"></Column>
            <Column field="status" header="상태">
              <template #body="slotProps">
                <Tag :severity="slotProps.data.status === 'Active' ? 'success' : 'danger'">
                  {{ slotProps.data.status }}
                </Tag>
              </template>
            </Column>
          </DataTable>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AutoComplete from 'primevue/autocomplete'
import Tag from 'primevue/tag'

const route = useRoute()
const router = useRouter()
const selectedRecipe = ref(null)
const actionResult = ref(null)
const checkResults = ref(null)
const checkResult = ref(null)
const isChecking = ref(false)
const filteredRecipes = ref([])

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

// Recipe search functionality
const searchRecipe = (event) => {
  const query = event.query.toLowerCase()
  filteredRecipes.value = recipeDatabase.filter(recipe => 
    recipe.toLowerCase().includes(query)
  )
}

// Go back to recipe search with CD-SEM pre-selected
const goBackToRecipeSearch = () => {
  // Store that CD-SEM was selected
  sessionStorage.setItem('selectedTool', 'cd-sem')
  const facId = route.params.fac_id || 'R3'
  router.push(`/${facId}/recipe-search`)
}

// Action: Check Horizontal Deploy
const checkHorizontalDeploy = async () => {
  if (!selectedRecipe.value) return
  
  isChecking.value = true
  checkResults.value = null
  checkResult.value = true // Show results section
  
  actionResult.value = {
    severity: 'info',
    message: `횡전개 체크를 진행합니다: ${selectedRecipe.value}`
  }
  
  // Simulate API call
  setTimeout(() => {
    // Mock check results
    checkResults.value = {
      baseVersion: 'v1.2.3',
      totalEquipment: 10,
      sameVersion: 7,
      differentVersion: 3,
      details: [
        { equipment: 'EQP_001', version: 'v1.2.3', lastUpdate: '2024-01-15', status: 'Active' },
        { equipment: 'EQP_002', version: 'v1.2.3', lastUpdate: '2024-01-15', status: 'Active' },
        { equipment: 'EQP_003', version: 'v1.2.2', lastUpdate: '2024-01-10', status: 'Active' },
        { equipment: 'EQP_004', version: 'v1.2.3', lastUpdate: '2024-01-15', status: 'Active' },
        { equipment: 'EQP_005', version: 'v1.2.1', lastUpdate: '2024-01-05', status: 'Inactive' },
        { equipment: 'EQP_006', version: 'v1.2.3', lastUpdate: '2024-01-15', status: 'Active' },
        { equipment: 'EQP_007', version: 'v1.2.3', lastUpdate: '2024-01-15', status: 'Active' },
        { equipment: 'EQP_008', version: 'v1.2.0', lastUpdate: '2024-01-01', status: 'Active' },
        { equipment: 'EQP_009', version: 'v1.2.3', lastUpdate: '2024-01-15', status: 'Active' },
        { equipment: 'EQP_010', version: 'v1.2.3', lastUpdate: '2024-01-15', status: 'Active' }
      ]
    }
    
    actionResult.value = {
      severity: 'success',
      message: '횡전개 체크가 완료되었습니다.'
    }
    
    isChecking.value = false
  }, 2000)
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>