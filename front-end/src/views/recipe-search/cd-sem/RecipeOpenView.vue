<template>
  <div class="recipe-open bg-surface-50 dark:bg-surface-950 px-6 py-20 md:px-12 xl:px-20">
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
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Recipe 열기</div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">Recipe 설정 상태를 확인할 수 있습니다</div>
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
            label="Recipe 열기"
            icon="pi pi-external-link"
            @click="openRecipe"
            :disabled="!selectedRecipe"
            :loading="loading"
            class="w-full sm:w-auto"
          />
        </div>

        <!-- Error Message -->
        <Message v-if="error" severity="error" :closable="true" @close="error = null">
          {{ error }}
        </Message>

        <!-- Recipe Data Tables -->
        <div v-if="recipeData" class="mt-6">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Left Side: IDP Image Info Table -->
            <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
              <h3 class="text-lg font-semibold mb-4">IDP Image Information</h3>
              <DataTable 
                :value="recipeData.idp_image_info" 
                :paginator="true" 
                :rows="10"
                responsiveLayout="scroll"
                @row-click="handleParameterClick"
                class="cursor-pointer"
                :rowHover="true"
              >
                <Column field="Parameter" header="Parameter" :sortable="true" />
                <Column field="SEQ" header="SEQ" :sortable="true" />
                <Column field="Region" header="Region" :sortable="true" />
                <Column field="Addressing" header="Addressing" />
                <Column field="Meas_Counting" header="Meas Count" :sortable="true" />
              </DataTable>
            </div>

            <!-- Right Side: Dynamic Data Table -->
            <div class="bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
              <h3 class="text-lg font-semibold mb-4">
                {{ selectedParameter ? `Parameter ${selectedParameter} Details` : 'Select a Parameter' }}
              </h3>
              <DataTable 
                v-if="filteredData && filteredData.length > 0"
                :value="filteredData" 
                :paginator="true" 
                :rows="10"
                responsiveLayout="scroll"
              >
                <!-- Wafer MP Info Columns -->
                <Column field="ChipNo_X" header="Chip X" :sortable="true" />
                <Column field="ChipNo_Y" header="Chip Y" :sortable="true" />
                <Column field="Coordinate_X" header="Coord X" :sortable="true" />
                <Column field="Coordinate_Y" header="Coord Y" :sortable="true" />
                <Column field="P_No" header="P No" :sortable="true" />
                <Column field="D_No" header="D No" :sortable="true" />
                <Column field="Diff" header="Diff">
                  <template #body="slotProps">
                    <Tag :severity="slotProps.data.Diff ? 'success' : 'danger'">
                      {{ slotProps.data.Diff ? 'Yes' : 'No' }}
                    </Tag>
                  </template>
                </Column>
                <Column field="Rel" header="Rel">
                  <template #body="slotProps">
                    <Tag :severity="slotProps.data.Rel ? 'success' : 'danger'">
                      {{ slotProps.data.Rel ? 'Yes' : 'No' }}
                    </Tag>
                  </template>
                </Column>
              </DataTable>
              <div v-else class="text-center text-surface-500 py-8">
                Click on a parameter in the left table to view details
              </div>
            </div>
          </div>

          <!-- Additional Data Tables Below -->
          <div class="mt-6 bg-surface-100 dark:bg-surface-800 rounded-lg p-4">
            <h3 class="text-lg font-semibold mb-4">Wafer Alignment Information</h3>
            <DataTable 
              :value="recipeData.wafer_align_info" 
              :paginator="true" 
              :rows="5"
              responsiveLayout="scroll"
            >
              <Column field="Align_No" header="Align No" :sortable="true" />
              <Column field="Chip.X" header="Chip X" :sortable="true" />
              <Column field="Chip.Y" header="Chip Y" :sortable="true" />
              <Column field="Coordinate.X" header="Coordinate X" :sortable="true" />
              <Column field="Coordinate.Y" header="Coordinate Y" :sortable="true" />
              <Column field="P.No" header="P No" :sortable="true" />
            </DataTable>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const selectedRecipe = ref(null)
const recipeData = ref(null)
const loading = ref(false)
const error = ref(null)
const selectedParameter = ref(null)

// Get fac_id from route params
const facId = computed(() => route.params.fac_id || 'R3')

// Filter wafer_mp_info based on selected parameter
const filteredData = computed(() => {
  if (!recipeData.value || !selectedParameter.value) return []
  
  // Filter wafer_mp_info by P_No matching the selected parameter
  const paramNumber = parseInt(selectedParameter.value.replace('Para_', ''))
  return recipeData.value.wafer_mp_info.filter(item => item.P_No === paramNumber)
})

// Load selected recipe from sessionStorage
onMounted(() => {
  const storedRecipe = sessionStorage.getItem('selectedRecipe')
  if (storedRecipe) {
    selectedRecipe.value = storedRecipe
    sessionStorage.removeItem('selectedRecipe')
    // Auto-execute the action
    openRecipe()
  }
})

// Handle parameter click in IDP table
const handleParameterClick = (event) => {
  const rowData = event.data
  selectedParameter.value = rowData.Parameter
  console.log('Selected parameter:', rowData)
}

// Action: Open Recipe
const openRecipe = async () => {
  if (!selectedRecipe.value) return
  
  loading.value = true
  error.value = null
  
  try {
    // Call the API with fac_id and tool_category
    const response = await axios.get(
      `/api/recipe-search/${facId.value}/cd-sem/recipe-open/${selectedRecipe.value}`
    )
    
    if (response.data.success) {
      recipeData.value = response.data.data
      console.log('Recipe data received:', recipeData.value)
      
      // Log each data type separately for clarity
      console.log('IDP Image Info:', recipeData.value.idp_image_info)
      console.log('Wafer MP Info:', recipeData.value.wafer_mp_info)
      console.log('Wafer Align Info:', recipeData.value.wafer_align_info)
    } else {
      error.value = response.data.error || 'Failed to load recipe data'
    }
  } catch (err) {
    console.error('Error fetching recipe data:', err)
    error.value = err.response?.data?.error || 'Error loading recipe data'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
:deep(.p-datatable-row:hover) {
  background-color: var(--p-surface-200) !important;
}

:deep(.p-datatable-row) {
  cursor: pointer;
}
</style>