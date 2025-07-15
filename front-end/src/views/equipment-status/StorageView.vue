<template>
  <div class="storage bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
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
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">장비 스토리지 정보</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          CD-SEM & HV-SEM 장비의 스토리지 사용량 및 레시피 정보
          <span v-if="fabStore.currentFab" class="ml-2 font-medium text-primary">
            (FAB: {{ fabStore.currentFab }})
          </span>
        </div>
      </div>
    </div>

    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex flex-col gap-4">
        <div class="flex justify-between items-center">
          <div class="flex flex-col gap-1">
            <h3 class="text-lg font-medium">CD-SEM & HV-SEM 스토리지 현황</h3>
            <p class="text-sm text-surface-500">스토리지 사용률 높은 순으로 정렬</p>
          </div>
        </div>
        
        <!-- Equipment Type Filter Buttons -->
        <div class="mb-4">
          <div class="text-md font-semibold mb-3">장비 유형 필터</div>
          <div class="flex flex-wrap gap-2">
            <Button
              label="전체"
              :severity="selectedEquipmentType === null ? 'primary' : 'secondary'"
              :outlined="selectedEquipmentType !== null"
              size="small"
              @click="selectEquipmentType(null)"
            />
            <Button
              v-for="category in equipmentCategories"
              :key="category.name"
              :label="`${category.name} (${category.count})`"
              :severity="selectedEquipmentType === category.name ? 'primary' : 'secondary'"
              :outlined="selectedEquipmentType !== category.name"
              size="small"
              @click="selectEquipmentType(category.name)"
            />
          </div>
        </div>
        
        <div v-if="isLoading" class="flex justify-center py-8">
          <ProgressSpinner />
        </div>
        
        <div v-else-if="isError" class="text-center py-8">
          <Message severity="error" :closable="false">
            데이터를 불러오는 중 오류가 발생했습니다.
          </Message>
        </div>
        
        <DataTable 
          v-else
          :value="storageData" 
          stripedRows
          paginator
          :rows="10"
          :rowsPerPageOptions="[10, 20, 50]"
          sortMode="multiple"
          removableSort
          :globalFilterFields="['eqp_id', 'fab_name', 'fac_id', 'eqp_model_cd']"
          v-model:filters="filters"
        >
          <template #header>
            <div class="flex justify-between items-center">
              <span class="text-sm text-surface-500">
                총 {{ storageData?.length || 0 }}개 장비
              </span>
              <span class="p-input-icon-left">
                <i class="pi pi-search" />
                <InputText 
                  v-model="globalFilterValue" 
                  placeholder="전체 검색" 
                  class="w-64"
                />
              </span>
            </div>
          </template>
          
          <Column field="eqp_id" header="장비 ID" sortable></Column>
          
          <Column field="fab_name" header="FAB" sortable></Column>
          
          <Column header="장비 유형" sortable>
            <template #body="{ data }">
              <Tag 
                :value="getModelCategory(data.eqp_model_cd)" 
                :severity="getModelCategory(data.eqp_model_cd) === 'CD-SEM' ? 'info' : 'warning'"
              />
            </template>
          </Column>
          
          <Column field="eqp_model_cd" header="모델" sortable />
          
          <Column field="total" header="전체 용량" sortable>
            <template #body="{ data }">
              <span class="font-medium">{{ data.total }}</span>
            </template>
          </Column>
          
          <Column field="used" header="사용량" sortable>
            <template #body="{ data }">
              <span>{{ data.used }}</span>
            </template>
          </Column>
          
          <Column field="percent" header="사용률" sortable>
            <template #body="{ data }">
              <div class="flex items-center gap-2">
                <ProgressBar 
                  :value="parseInt(data.percent)" 
                  :showValue="false"
                  class="w-full"
                  :class="{
                    'bg-red-100': parseInt(data.percent) > 85,
                    'bg-yellow-100': parseInt(data.percent) > 70 && parseInt(data.percent) <= 85
                  }"
                />
                <span class="text-sm font-medium min-w-[3rem] text-right">{{ data.percent }}</span>
              </div>
            </template>
          </Column>
          
          <Column field="rcp_counts" header="레시피 수" sortable>
            <template #body="{ data }">
              <Badge :value="data.rcp_counts" severity="info" />
            </template>
          </Column>
          
          <Column field="storage_mt" header="업데이트 시간" sortable>
            <template #body="{ data }">
              <span class="text-sm">{{ formatDate(data.storage_mt) }}</span>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { equipmentQueries } from '@/services/equipmentService'
import { FilterMatchMode } from '@primevue/core/api'
import { useFabStore } from '@/stores/fab'

// FAB store
const fabStore = useFabStore()

// Fetch storage data using React Query
const { data: rawStorageData, isLoading, isError } = useQuery(equipmentQueries.storage())

// Filter state
const selectedEquipmentType = ref(null)

// Model category classification (same as CurrentStatusView)
const getModelCategory = (modelCode) => {
  if (!modelCode) return 'UNKNOWN'
  
  const model = modelCode.toUpperCase()
  
  if (model.startsWith('CG') || model.startsWith('GT')) {
    return 'CD-SEM'
  } else if (model.startsWith('TP')) {
    return 'HV-SEM'
  } else if (model.includes('VERITY')) {
    return 'VeritySEM'
  } else if (model.includes('PROVISION')) {
    return 'PROVISION'
  }
  
  return 'OTHER'
}

// Get base filtered data (FAB + CD-SEM/HV-SEM only)
const baseFilteredData = computed(() => {
  const rawData = rawStorageData.value?.data || []
  
  let filteredData = rawData
  
  // Filter by selected FAB (fac_id matches selected FAB)
  if (fabStore.currentFab) {
    filteredData = filteredData.filter(item => item.fac_id === fabStore.currentFab)
  }
  
  // Filter by equipment type - only CD-SEM and HV-SEM
  filteredData = filteredData.filter(item => {
    const category = getModelCategory(item.eqp_model_cd)
    return category === 'CD-SEM' || category === 'HV-SEM'
  })
  
  return filteredData
})

// Compute equipment categories with counts from base filtered data
const equipmentCategories = computed(() => {
  const categories = {}
  
  baseFilteredData.value.forEach(item => {
    const category = getModelCategory(item.eqp_model_cd)
    if (category === 'CD-SEM' || category === 'HV-SEM') {
      if (!categories[category]) {
        categories[category] = { name: category, count: 0 }
      }
      categories[category].count++
    }
  })
  
  return Object.values(categories).sort((a, b) => a.name.localeCompare(b.name))
})

// Final filtered data with equipment type selection
const storageData = computed(() => {
  let filteredData = baseFilteredData.value
  
  // Apply equipment type filter if selected
  if (selectedEquipmentType.value) {
    filteredData = filteredData.filter(item => 
      getModelCategory(item.eqp_model_cd) === selectedEquipmentType.value
    )
  }
  
  // Sort by storage usage percentage (highest first)
  return filteredData.sort((a, b) => {
    const percentA = parseInt(a.percent) || 0
    const percentB = parseInt(b.percent) || 0
    return percentB - percentA // Descending order (highest first)
  })
})

// Global filter setup
const globalFilterValue = ref('')
const filters = ref({
  'global': { value: null, matchMode: FilterMatchMode.CONTAINS }
})

// Watch for changes in global filter
watch(globalFilterValue, (newValue) => {
  filters.value['global'].value = newValue
})

// Equipment type selection method
const selectEquipmentType = (type) => {
  selectedEquipmentType.value = type
}

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}
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

:deep(.p-input-icon-left) {
  position: relative;
}

:deep(.p-input-icon-left > .pi) {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--p-text-color-secondary);
}

:deep(.p-input-icon-left > .p-inputtext) {
  padding-left: 2.5rem;
}

.p-button {
  transition: all 0.2s ease;
}
</style>