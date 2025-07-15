<template>
  <div class="not-available bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
    <div class="flex flex-col items-start gap-4 mb-8">
      <Button 
        icon="pi pi-arrow-left" 
        label="장비 현황으로 돌아가기"
        outlined
        size="large"
        class="mb-2"
        @click="$router.push({ name: 'equipment-status' })" 
      />
      <div class="flex flex-col gap-2">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Data 확인 불가 현황</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          스큐노노가 접근 불가능한 장비 리스트
          <span v-if="fabStore.currentFab" class="ml-2 font-medium text-primary">
            (FAB: {{ fabStore.currentFab }})
          </span>
        </div>
      </div>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <ProgressSpinner />
    </div>

    <!-- Error state -->
    <div v-else-if="isError" class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <Message severity="error" :closable="false">
        데이터를 불러오는 중 오류가 발생했습니다.
      </Message>
    </div>

    <!-- Main content -->
    <div v-else class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <!-- Category selection buttons -->
      <div class="flex flex-col gap-4 mb-6">
        <h2 class="text-xl font-semibold">Data 확인 불가 분류</h2>
        <div class="flex flex-wrap gap-3">
          <Button 
            :label="`장비 OFF (${notAvailableData?.counts?.equipment_off || 0})`"
            :severity="selectedCategory === 'equipment_off' ? 'primary' : 'secondary'"
            :outlined="selectedCategory !== 'equipment_off'"
            @click="selectedCategory = 'equipment_off'"
          />
          <Button 
            :label="`버전 없음 (${notAvailableData?.counts?.version_empty || 0})`"
            :severity="selectedCategory === 'version_empty' ? 'primary' : 'secondary'"
            :outlined="selectedCategory !== 'version_empty'"
            @click="selectedCategory = 'version_empty'"
          />
          <Button 
            :label="`스토리지 없음 (${notAvailableData?.counts?.storage_empty || 0})`"
            :severity="selectedCategory === 'storage_empty' ? 'primary' : 'secondary'"
            :outlined="selectedCategory !== 'storage_empty'"
            @click="selectedCategory = 'storage_empty'"
          />
        </div>
        
        <!-- Refresh timing info -->
        <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
          <div class="flex items-start gap-3">
            <i class="pi pi-clock text-surface-600 mt-1"></i>
            <div>
              <h4 class="font-medium text-surface-900 dark:text-surface-0 mb-2">업데이트 주기</h4>
              <ul class="text-sm text-surface-600 dark:text-surface-300 space-y-1">
                <li>• 장비 OFF 상태: 30분마다 확인</li>
                <li>• 버전 정보: 24시간마다 확인</li>
                <li>• 스토리지 정보: 24시간마다 확인</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- FAB Filter -->
      <div class="mb-4">
        <div class="text-lg font-semibold mb-3">FAB 선택</div>
        <div class="flex flex-wrap gap-2">
          <Button
            label="전체"
            :severity="selectedFab === null ? 'primary' : 'secondary'"
            :outlined="selectedFab !== null"
            size="small"
            @click="selectFab(null)"
          />
          <Button
            v-for="fab in availableFabs"
            :key="fab.name"
            :label="`${fab.name} (${fab.count})`"
            :severity="selectedFab === fab.name ? 'primary' : 'secondary'"
            :outlined="selectedFab !== fab.name"
            size="small"
            @click="selectFab(fab.name)"
          />
        </div>
      </div>

      <!-- Model filter -->
      <div class="flex flex-col gap-4 mb-6">
        <h3 class="text-lg font-medium">모델 필터</h3>
        <div class="flex gap-4">
          <Dropdown 
            v-model="selectedModel" 
            :options="availableModels" 
            optionLabel="label"
            optionValue="value"
            placeholder="모델 선택"
            class="w-64"
            showClear
          />
        </div>
      </div>

      <!-- Data display -->
      <div class="mt-6">
        <h3 class="text-lg font-medium mb-4">{{ getCategoryTitle() }}</h3>
        <DataTable 
          :value="filteredData" 
          :paginator="true" 
          :rows="10" 
          :loading="isLoading"
          stripedRows
          showGridlines
          size="small"
          scrollable
          scrollHeight="600px"
          class="text-sm"
        >
          <Column field="eqp_id" header="장비 ID" sortable />
          <Column field="eqp_model_cd" header="모델" sortable />
          <Column field="vendor_nm" header="벤더" sortable />
          <Column field="fac_id" header="시설 ID" sortable />
          <Column field="fab_name" header="FAB 이름" sortable />
          <Column field="eqp_ip" header="IP 주소" sortable />
          <Column v-if="selectedCategory === 'equipment_off' || selectedCategory === 'storage_empty'" field="available" header="상태">
            <template #body="slotProps">
              <Badge 
                :value="selectedCategory === 'equipment_off' ? slotProps.data.available : '스토리지 없음'" 
                :severity="selectedCategory === 'equipment_off' ? (slotProps.data.available === 'Off' ? 'danger' : 'success') : 'warning'"
              />
            </template>
          </Column>
          <Column v-if="selectedCategory === 'version_empty'" field="version" header="버전">
            <template #body="slotProps">
              <span v-if="slotProps.data.version === ''">
                <Badge value="버전 없음" severity="warning" />
              </span>
              <span v-else>{{ slotProps.data.version }}</span>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { equipmentQueries } from '@/services/equipmentService'
import { useFabStore } from '@/stores/fab'

// FAB store
const fabStore = useFabStore()

// Reactive state
const selectedCategory = ref('equipment_off')
const selectedFab = ref(null)
const selectedModel = ref(null)

// Fetch not available equipment data
const { data: notAvailableData, isLoading, isError } = useQuery(equipmentQueries.notAvailable())

// Get all available FABs from raw data filtered by current fac_id
const availableFabs = computed(() => {
  if (!notAvailableData.value?.data) return []
  
  const fabs = {}
  const categoryData = notAvailableData.value.data[selectedCategory.value] || []
  
  // First filter by fac_id from navbar store
  const filteredData = fabStore.currentFab 
    ? categoryData.filter(item => item.fac_id === fabStore.currentFab)
    : categoryData
  
  filteredData.forEach(item => {
    if (item.fab_name) {
      if (!fabs[item.fab_name]) {
        fabs[item.fab_name] = { name: item.fab_name, count: 0 }
      }
      fabs[item.fab_name].count++
    }
  })
  
  return Object.values(fabs).sort((a, b) => a.name.localeCompare(b.name))
})

// Computed properties
const currentCategoryData = computed(() => {
  if (!notAvailableData.value?.data) return []
  const categoryData = notAvailableData.value.data[selectedCategory.value] || []
  
  // First filter by fac_id from navbar store
  let filteredData = fabStore.currentFab 
    ? categoryData.filter(item => item.fac_id === fabStore.currentFab)
    : categoryData
  
  // Then filter by selected fab_name if any
  if (selectedFab.value) {
    filteredData = filteredData.filter(item => item.fab_name === selectedFab.value)
  }
  
  return filteredData
})

const availableModels = computed(() => {
  if (!currentCategoryData.value || currentCategoryData.value.length === 0) return []
  
  const models = [...new Set(currentCategoryData.value.map(item => item.eqp_model_cd))]
  return [
    { label: '모든 모델', value: null },
    ...models.map(model => ({ label: model, value: model }))
  ]
})

const filteredData = computed(() => {
  if (!currentCategoryData.value) return []
  
  let filtered = [...currentCategoryData.value]
  
  if (selectedModel.value) {
    filtered = filtered.filter(item => item.eqp_model_cd === selectedModel.value)
  }
  
  return filtered
})

// Methods
const getCategoryTitle = () => {
  switch (selectedCategory.value) {
    case 'equipment_off':
      return '장비 OFF 상태'
    case 'version_empty':
      return '버전 정보 없음'
    case 'storage_empty':
      return '스토리지 정보 없음'
    default:
      return '장비 정보'
  }
}

// Selection methods
const selectFab = (fab) => {
  selectedFab.value = fab
  selectedModel.value = null // Reset model when FAB changes
}

// Reset filters when category changes
const resetFilters = () => {
  selectedFab.value = null
  selectedModel.value = null
}

// Watch for category changes
import { watch } from 'vue'
watch(selectedCategory, () => {
  resetFilters()
})

// Watch for store FAB changes to reset selections
watch(() => fabStore.currentFab, () => {
  selectedFab.value = null
  selectedModel.value = null
})
</script>

<style scoped>
:deep(.p-datatable) {
  width: 100%;
}

:deep(.p-datatable-wrapper) {
  width: 100%;
}

:deep(.p-datatable-header) {
  background-color: transparent;
  border: none;
  padding: 1rem 1.5rem;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background-color: var(--p-surface-100);
  font-weight: 600;
}

.p-button {
  transition: all 0.2s ease;
}
</style>