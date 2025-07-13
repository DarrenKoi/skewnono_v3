<template>
  <div class="current-status bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
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
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">현재 장비 상태</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">실시간 장비 상태 및 모니터링 정보</div>
      </div>
    </div>

    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-2xl font-semibold">장비 목록</h2>
        <div class="flex items-center gap-2">
          <Button 
            icon="pi pi-refresh" 
            label="새로고침" 
            @click="refetch"
            :loading="isRefetching"
            size="small"
          />
          <Tag :value="`Total: ${filteredTableData.length}`" severity="secondary" />
        </div>
      </div>

      <!-- Model Category Filter - First Layer -->
      <div class="mb-4">
        <div class="text-lg font-semibold mb-3">장비 분류</div>
        <div class="flex flex-wrap gap-2">
          <Button
            label="전체"
            :severity="selectedCategory === null ? 'primary' : 'secondary'"
            :outlined="selectedCategory !== null"
            size="small"
            @click="selectCategory(null)"
          />
          <Button
            v-for="category in modelCategories"
            :key="category.name"
            :label="`${category.name} (${category.count})`"
            :severity="selectedCategory === category.name ? 'primary' : 'secondary'"
            :outlined="selectedCategory !== category.name"
            size="small"
            @click="selectCategory(category.name)"
          />
        </div>
      </div>

      <!-- Specific Model Filter - Second Layer -->
      <div v-if="selectedCategory && availableModels.length > 0" class="mb-4">
        <div class="text-md font-semibold mb-3">{{ selectedCategory }} 모델</div>
        <div class="flex flex-wrap gap-2">
          <Button
            label="전체"
            :severity="selectedModel === null ? 'primary' : 'secondary'"
            :outlined="selectedModel !== null"
            size="small"
            @click="selectModel(null)"
          />
          <Button
            v-for="model in availableModels"
            :key="model.name"
            :label="`${model.name} (${model.count})`"
            :severity="selectedModel === model.name ? 'primary' : 'secondary'"
            :outlined="selectedModel !== model.name"
            size="small"
            @click="selectModel(model.name)"
          />
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-8">
        <ProgressSpinner />
      </div>

      <!-- Error State -->
      <Message v-else-if="isError" severity="error" :closable="false">
        데이터를 불러오는 중 오류가 발생했습니다. 다시 시도해주세요.
      </Message>

      <!-- Data Table -->
      <DataTable 
        v-else
        :value="filteredTableData" 
        :paginator="true" 
        :rows="10"
        :rowsPerPageOptions="[5, 10, 20, 50]"
        :loading="isRefetching"
        stripedRows
        showGridlines
        size="small"
        scrollable
        scrollHeight="600px"
        class="text-sm"
      >
        <template #header>
          <div class="flex flex-wrap gap-2 align-items-center justify-content-between">
            <span class="p-input-icon-left">
              <i class="pi pi-search" />
              <InputText 
                v-model="globalFilterValue" 
                placeholder="전체 검색" 
                @input="onGlobalFilterChange"
              />
            </span>
          </div>
        </template>

        <template #empty>
          <div class="text-center py-4">데이터가 없습니다.</div>
        </template>

        <Column field="fac_id" header="시설 ID" sortable :style="{ width: '100px' }" />
        <Column field="eqp_id" header="장비 ID" sortable :style="{ width: '120px' }" />
        <Column field="eqp_model_cd" header="모델" sortable :style="{ width: '150px' }" />
        <Column field="eqp_grp_id" header="그룹 ID" sortable :style="{ width: '120px' }" />
        
        <Column field="vendor_nm" header="제조사" sortable :style="{ width: '100px' }" />
        <Column field="eqp_ip" header="IP 주소" sortable :style="{ width: '150px' }" />
        <Column field="fab_name" header="FAB" sortable :style="{ width: '100px' }" />
        
        <Column field="available" header="상태" sortable :style="{ width: '80px' }">
          <template #body="{ data }">
            <Tag 
              :value="data.available" 
              :severity="data.available === 'On' ? 'success' : 'danger'"
            />
          </template>
        </Column>

        <Column field="version" header="버전" sortable :style="{ width: '80px' }" />

        <Column field="updt_dt" header="업데이트 시간" sortable :style="{ width: '180px' }">
          <template #body="{ data }">
            {{ formatDate(data.updt_dt) }}
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { equipmentQueries } from '@/services/equipmentService'

// Fetch equipment data
const { data, isLoading, isError, isRefetching, refetch } = useQuery(equipmentQueries.currentStatus())

// Computed properties
const tableData = computed(() => data.value?.data || [])

// Filter states
const selectedCategory = ref(null)
const selectedModel = ref(null)
const globalFilterValue = ref('')

// Model category classification
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

// Compute model categories with counts
const modelCategories = computed(() => {
  const categories = {}
  
  tableData.value.forEach(item => {
    const category = getModelCategory(item.eqp_model_cd)
    if (category !== 'UNKNOWN' && category !== 'OTHER') {
      if (!categories[category]) {
        categories[category] = { name: category, count: 0 }
      }
      categories[category].count++
    }
  })
  
  return Object.values(categories).sort((a, b) => a.name.localeCompare(b.name))
})

// Get available models for selected category
const availableModels = computed(() => {
  if (!selectedCategory.value) return []
  
  const models = {}
  
  tableData.value
    .filter(item => getModelCategory(item.eqp_model_cd) === selectedCategory.value)
    .forEach(item => {
      const modelName = item.eqp_model_cd
      if (!models[modelName]) {
        models[modelName] = { name: modelName, count: 0 }
      }
      models[modelName].count++
    })
  
  return Object.values(models).sort((a, b) => a.name.localeCompare(b.name))
})

// Category-filtered data
const categoryFilteredData = computed(() => {
  if (!selectedCategory.value) return tableData.value
  
  return tableData.value.filter(item => 
    getModelCategory(item.eqp_model_cd) === selectedCategory.value
  )
})

// Model-filtered data
const modelFilteredData = computed(() => {
  if (!selectedModel.value) return categoryFilteredData.value
  
  return categoryFilteredData.value.filter(item => 
    item.eqp_model_cd === selectedModel.value
  )
})

// Global search filtered data
const filteredTableData = computed(() => {
  if (!globalFilterValue.value) return modelFilteredData.value
  
  const searchValue = globalFilterValue.value.toLowerCase()
  return modelFilteredData.value.filter(item => {
    return Object.values(item).some(field => 
      String(field).toLowerCase().includes(searchValue)
    )
  })
})

// Selection methods
const selectCategory = (category) => {
  selectedCategory.value = category
  selectedModel.value = null // Reset model selection when category changes
}

const selectModel = (model) => {
  selectedModel.value = model
}

// Watch for category changes to reset model selection
watch(selectedCategory, () => {
  selectedModel.value = null
})

// Global filter
const onGlobalFilterChange = (event) => {
  globalFilterValue.value = event.target.value
}

// Format date
const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}
</script>

<style scoped>
:deep(.p-datatable-header) {
  background-color: transparent;
  border: none;
}

:deep(.p-datatable .p-datatable-thead > tr > th) {
  background-color: var(--p-surface-100);
  font-weight: 600;
}

:deep(.p-input-icon-left > svg) {
  top: 50%;
  margin-top: -0.5rem;
}

:deep(.p-input-icon-left > .p-inputtext) {
  padding-left: 2.5rem;
}

.p-button {
  transition: all 0.2s ease;
}
</style>