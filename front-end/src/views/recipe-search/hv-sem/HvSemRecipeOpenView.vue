<template>
  <div class="recipe-open-view bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="flex items-center gap-4">
        <Button 
          icon="pi pi-arrow-left" 
          rounded 
          text 
          @click="goBack"
          v-tooltip.right="'이전 페이지로'"
        />
        <div>
          <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">HV-SEM Recipe 열기</div>
          <div class="text-surface-500 dark:text-surface-300 text-lg mt-1">Recipe 설정 상태를 확인합니다</div>
        </div>
      </div>
    </div>

    <!-- Recipe Information Card -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold">Recipe: {{ selectedRecipe || 'Loading...' }}</h3>
        <Tag :value="recipeStatus" :severity="getStatusSeverity(recipeStatus)" />
      </div>
      
      <!-- Recipe Details Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="flex flex-col gap-4">
          <div>
            <label class="text-sm text-surface-600 dark:text-surface-400">Recipe ID</label>
            <p class="text-surface-900 dark:text-surface-0 font-medium">{{ selectedRecipe }}</p>
          </div>
          <div>
            <label class="text-sm text-surface-600 dark:text-surface-400">생성일</label>
            <p class="text-surface-900 dark:text-surface-0 font-medium">{{ recipeData.createdDate }}</p>
          </div>
          <div>
            <label class="text-sm text-surface-600 dark:text-surface-400">수정일</label>
            <p class="text-surface-900 dark:text-surface-0 font-medium">{{ recipeData.modifiedDate }}</p>
          </div>
        </div>
        <div class="flex flex-col gap-4">
          <div>
            <label class="text-sm text-surface-600 dark:text-surface-400">버전</label>
            <p class="text-surface-900 dark:text-surface-0 font-medium">{{ recipeData.version }}</p>
          </div>
          <div>
            <label class="text-sm text-surface-600 dark:text-surface-400">상태</label>
            <p class="text-surface-900 dark:text-surface-0 font-medium">{{ recipeStatus }}</p>
          </div>
          <div>
            <label class="text-sm text-surface-600 dark:text-surface-400">작성자</label>
            <p class="text-surface-900 dark:text-surface-0 font-medium">{{ recipeData.author }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recipe Parameters -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <h3 class="text-xl font-semibold mb-4">Recipe Parameters</h3>
      
      <DataTable 
        :value="recipeParameters" 
        :paginator="true" 
        :rows="10"
        :rowsPerPageOptions="[10, 20, 50]"
        paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} parameters"
        responsiveLayout="scroll"
        :loading="loading"
      >
        <Column field="paramName" header="Parameter Name" :sortable="true" />
        <Column field="value" header="Value" :sortable="true" />
        <Column field="unit" header="Unit" />
        <Column field="min" header="Min" />
        <Column field="max" header="Max" />
        <Column field="status" header="Status">
          <template #body="slotProps">
            <Tag 
              :value="slotProps.data.status" 
              :severity="slotProps.data.status === 'Valid' ? 'success' : 'warning'"
            />
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const router = useRouter()

// Reactive data
const selectedRecipe = ref('')
const loading = ref(false)
const recipeStatus = ref('Active')
const recipeData = ref({
  createdDate: '2024-01-15',
  modifiedDate: '2024-03-20',
  version: '2.1.0',
  author: 'System Admin'
})

// Sample parameters data
const recipeParameters = ref([
  { paramName: 'Beam Voltage', value: '30', unit: 'kV', min: '20', max: '40', status: 'Valid' },
  { paramName: 'Beam Current', value: '150', unit: 'pA', min: '100', max: '200', status: 'Valid' },
  { paramName: 'Working Distance', value: '8.5', unit: 'mm', min: '5', max: '15', status: 'Valid' },
  { paramName: 'Magnification', value: '50000', unit: 'x', min: '1000', max: '100000', status: 'Valid' },
  { paramName: 'Scan Speed', value: '3', unit: '', min: '1', max: '10', status: 'Valid' },
  { paramName: 'Detector Type', value: 'SE', unit: '', min: '-', max: '-', status: 'Valid' },
  { paramName: 'Vacuum Level', value: '5e-6', unit: 'Pa', min: '1e-6', max: '1e-5', status: 'Valid' },
  { paramName: 'Stage Tilt', value: '0', unit: '°', min: '-5', max: '70', status: 'Valid' },
  { paramName: 'Image Resolution', value: '1024x768', unit: 'px', min: '-', max: '-', status: 'Valid' },
  { paramName: 'Dwell Time', value: '10', unit: 'μs', min: '1', max: '100', status: 'Valid' }
])

// Methods
const goBack = () => {
  router.back()
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'Active':
      return 'success'
    case 'Inactive':
      return 'warning'
    case 'Error':
      return 'danger'
    default:
      return 'info'
  }
}

// Load recipe data on mount
onMounted(() => {
  // Get selected recipe from sessionStorage
  selectedRecipe.value = sessionStorage.getItem('selectedRecipe') || 'HV_RECIPE_001_STANDARD'
  
  // Simulate loading recipe data
  loading.value = true
  setTimeout(() => {
    loading.value = false
  }, 1000)
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>