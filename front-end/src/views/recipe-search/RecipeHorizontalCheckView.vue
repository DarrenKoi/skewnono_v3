<template>
  <div class="recipe-horizontal-check bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
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
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">횡전개 체크</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">Recipe의 횡전개 여부와 Version을 체크할 수 있습니다</div>
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
            label="횡전개 체크 실행"
            icon="pi pi-check-square"
            @click="checkHorizontalDeploy"
            :disabled="!selectedRecipe"
            :loading="isChecking"
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
import { ref, onMounted } from 'vue'

const selectedRecipe = ref(null)
const actionResult = ref(null)
const checkResults = ref(null)
const isChecking = ref(false)

// Load selected recipe from sessionStorage and auto-execute if present
onMounted(() => {
  const storedRecipe = sessionStorage.getItem('selectedRecipe')
  if (storedRecipe) {
    selectedRecipe.value = storedRecipe
    sessionStorage.removeItem('selectedRecipe')
    // Auto-execute the action
    checkHorizontalDeploy()
  }
})

// Action: Check Horizontal Deploy
const checkHorizontalDeploy = async () => {
  if (!selectedRecipe.value) return
  
  isChecking.value = true
  checkResults.value = null
  
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