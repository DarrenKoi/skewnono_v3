<template>
  <div class="storage bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
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
        <div class="text-surface-500 dark:text-surface-300 text-lg">CD-SEM 장비의 스토리지 사용량 및 레시피 정보</div>
      </div>
    </div>

    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex flex-col gap-4">
        <div class="flex justify-between items-center">
          <h3 class="text-lg font-medium">장비별 스토리지 현황</h3>
          <div class="flex gap-2">
            <Button 
              label="새로고침" 
              icon="pi pi-refresh" 
              size="small" 
              :loading="isLoading"
              @click="refetch"
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
              <InputIcon>
                <InputText v-model="globalFilterValue" placeholder="검색..." />
                <i class="pi pi-search" />
              </InputIcon>
            </div>
          </template>
          
          <Column field="eqp_id" header="장비 ID" sortable></Column>
          
          <Column field="fab_name" header="FAB" sortable></Column>
          
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

// Add storage query to equipment service
const storageQuery = () => ({
  queryKey: ['equipment', 'storage'],
  queryFn: async () => {
    const response = await fetch('/api/equipment-status/storage')
    if (!response.ok) {
      throw new Error('Failed to fetch storage data')
    }
    const result = await response.json()
    return result.data
  },
  staleTime: 1000 * 60 * 5, // 5 minutes
  cacheTime: 1000 * 60 * 10, // 10 minutes
})

// Fetch storage data using React Query
const { data: storageData, isLoading, isError, refetch } = useQuery(storageQuery())

// Global filter setup
const globalFilterValue = ref('')
const filters = ref({
  'global': { value: null, matchMode: FilterMatchMode.CONTAINS }
})

// Watch for changes in global filter
watch(globalFilterValue, (newValue) => {
  filters.value['global'].value = newValue
})

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
/* Component-specific styles if needed */
</style>