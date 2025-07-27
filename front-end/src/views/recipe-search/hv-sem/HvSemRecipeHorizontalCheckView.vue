<template>
  <div class="recipe-horizontal-check bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
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
          <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">HV-SEM 횡전개 체크</div>
          <div class="text-surface-500 dark:text-surface-300 text-lg mt-1">Recipe의 횡전개 여부와 Version을 체크합니다</div>
        </div>
      </div>
    </div>

    <!-- Recipe Information Card -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border mb-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-xl font-semibold">Recipe: {{ selectedRecipe || 'Loading...' }}</h3>
        <Button 
          label="횡전개 체크 실행" 
          icon="pi pi-sync" 
          @click="performHorizontalCheck"
          :loading="checking"
        />
      </div>
      
      <!-- Check Summary -->
      <div v-if="checkPerformed" class="mt-4 p-4 bg-surface-100 dark:bg-surface-800 rounded-lg">
        <div class="flex items-center gap-4">
          <i :class="checkPassed ? 'pi pi-check-circle text-green-500' : 'pi pi-times-circle text-red-500'" class="text-2xl"></i>
          <div>
            <p class="font-semibold">{{ checkPassed ? '횡전개 체크 통과' : '횡전개 체크 실패' }}</p>
            <p class="text-sm text-surface-600 dark:text-surface-400">
              총 {{ totalEquipments }}대 중 {{ matchedEquipments }}대 일치 ({{ matchPercentage }}%)
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Equipment Comparison Table -->
    <div v-if="checkPerformed" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <h3 class="text-xl font-semibold mb-4">Equipment별 버전 비교</h3>
      
      <DataTable 
        :value="equipmentComparison" 
        :paginator="true" 
        :rows="10"
        :rowsPerPageOptions="[10, 20, 50]"
        paginatorTemplate="CurrentPageReport FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} equipments"
        responsiveLayout="scroll"
        :loading="loading"
      >
        <Column field="equipmentId" header="Equipment ID" :sortable="true" />
        <Column field="equipmentName" header="Equipment Name" :sortable="true" />
        <Column field="currentVersion" header="Current Version" :sortable="true" />
        <Column field="targetVersion" header="Target Version" />
        <Column field="status" header="Status">
          <template #body="slotProps">
            <Tag 
              :value="slotProps.data.status" 
              :severity="getStatusSeverity(slotProps.data.status)"
              :icon="getStatusIcon(slotProps.data.status)"
            />
          </template>
        </Column>
        <Column field="lastUpdate" header="Last Update" :sortable="true" />
        <Column header="Actions">
          <template #body="slotProps">
            <Button 
              v-if="slotProps.data.status !== 'Match'"
              label="Update" 
              size="small" 
              @click="updateEquipment(slotProps.data)"
              :disabled="slotProps.data.updating"
              :loading="slotProps.data.updating"
            />
          </template>
        </Column>
      </DataTable>
      
      <!-- Batch Actions -->
      <div v-if="mismatchedEquipments.length > 0" class="mt-4 flex gap-2">
        <Button 
          label="일괄 업데이트" 
          icon="pi pi-upload" 
          severity="primary"
          @click="batchUpdate"
          :disabled="batchUpdating"
          :loading="batchUpdating"
        />
        <Button 
          label="Export 결과" 
          icon="pi pi-download" 
          severity="secondary"
          @click="exportResults"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'
import Tag from 'primevue/tag'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

const router = useRouter()

// Reactive data
const selectedRecipe = ref('')
const loading = ref(false)
const checking = ref(false)
const checkPerformed = ref(false)
const batchUpdating = ref(false)
const targetVersion = ref('2.1.0')

// Sample equipment comparison data
const equipmentComparison = ref([])

// Computed properties
const totalEquipments = computed(() => equipmentComparison.value.length)
const matchedEquipments = computed(() => 
  equipmentComparison.value.filter(eq => eq.status === 'Match').length
)
const matchPercentage = computed(() => 
  totalEquipments.value > 0 ? Math.round((matchedEquipments.value / totalEquipments.value) * 100) : 0
)
const checkPassed = computed(() => matchPercentage.value === 100)
const mismatchedEquipments = computed(() => 
  equipmentComparison.value.filter(eq => eq.status !== 'Match')
)

// Methods
const goBack = () => {
  router.back()
}

const getStatusSeverity = (status) => {
  switch (status) {
    case 'Match':
      return 'success'
    case 'Mismatch':
      return 'warning'
    case 'Not Found':
      return 'danger'
    default:
      return 'info'
  }
}

const getStatusIcon = (status) => {
  switch (status) {
    case 'Match':
      return 'pi pi-check'
    case 'Mismatch':
      return 'pi pi-exclamation-triangle'
    case 'Not Found':
      return 'pi pi-times'
    default:
      return ''
  }
}

const performHorizontalCheck = async () => {
  checking.value = true
  checkPerformed.value = false
  
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1500))
  
  // Generate sample comparison data
  equipmentComparison.value = [
    { equipmentId: 'HV-001', equipmentName: 'HV-SEM Equipment 1', currentVersion: '2.1.0', targetVersion: targetVersion.value, status: 'Match', lastUpdate: '2024-03-20 14:30', updating: false },
    { equipmentId: 'HV-002', equipmentName: 'HV-SEM Equipment 2', currentVersion: '2.0.5', targetVersion: targetVersion.value, status: 'Mismatch', lastUpdate: '2024-03-15 10:20', updating: false },
    { equipmentId: 'HV-003', equipmentName: 'HV-SEM Equipment 3', currentVersion: '2.1.0', targetVersion: targetVersion.value, status: 'Match', lastUpdate: '2024-03-20 14:30', updating: false },
    { equipmentId: 'HV-004', equipmentName: 'HV-SEM Equipment 4', currentVersion: '1.9.8', targetVersion: targetVersion.value, status: 'Mismatch', lastUpdate: '2024-02-28 09:15', updating: false },
    { equipmentId: 'HV-005', equipmentName: 'HV-SEM Equipment 5', currentVersion: '-', targetVersion: targetVersion.value, status: 'Not Found', lastUpdate: '-', updating: false },
    { equipmentId: 'HV-006', equipmentName: 'HV-SEM Equipment 6', currentVersion: '2.1.0', targetVersion: targetVersion.value, status: 'Match', lastUpdate: '2024-03-20 14:30', updating: false },
    { equipmentId: 'HV-007', equipmentName: 'HV-SEM Equipment 7', currentVersion: '2.1.0', targetVersion: targetVersion.value, status: 'Match', lastUpdate: '2024-03-20 14:30', updating: false },
    { equipmentId: 'HV-008', equipmentName: 'HV-SEM Equipment 8', currentVersion: '2.0.8', targetVersion: targetVersion.value, status: 'Mismatch', lastUpdate: '2024-03-10 11:45', updating: false }
  ]
  
  checking.value = false
  checkPerformed.value = true
}

const updateEquipment = async (equipment) => {
  equipment.updating = true
  
  // Simulate update process
  await new Promise(resolve => setTimeout(resolve, 2000))
  
  // Update the equipment data
  equipment.currentVersion = equipment.targetVersion
  equipment.status = 'Match'
  equipment.lastUpdate = new Date().toLocaleString('ko-KR')
  equipment.updating = false
}

const batchUpdate = async () => {
  batchUpdating.value = true
  
  // Update all mismatched equipments
  for (const equipment of mismatchedEquipments.value) {
    if (equipment.status !== 'Not Found') {
      await updateEquipment(equipment)
    }
  }
  
  batchUpdating.value = false
}

const exportResults = () => {
  // Simulate export functionality
  console.log('Exporting results...')
  // In real implementation, this would generate and download a CSV/Excel file
}

// Load recipe data on mount
onMounted(() => {
  // Get selected recipe from sessionStorage
  selectedRecipe.value = sessionStorage.getItem('selectedRecipe') || 'HV_RECIPE_001_STANDARD'
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>