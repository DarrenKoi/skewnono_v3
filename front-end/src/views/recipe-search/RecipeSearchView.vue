<template>
  <div class="recipe-search bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Recipe 검색</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">
        장비 카테고리를 선택하세요
      </div>
    </div>

    <!-- Tool Category Selection -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <Card v-for="tool in toolCategories" :key="tool.id" :class="{
        'cursor-pointer transition-all duration-200 hover:shadow-lg': tool.active,
        'opacity-50 cursor-not-allowed': !tool.active,
        'ring-2 ring-primary-500': selectedTool === tool.id
      }" @click="tool.active ? selectTool(tool.id) : null">
        <template #content>
          <div class="text-center p-4">
            <i :class="[tool.icon, {
              'text-primary-600 dark:text-primary-400': tool.active,
              'text-surface-400': !tool.active
            }]" class="text-4xl mb-4"></i>
            <h3 class="text-xl font-semibold mb-3" :class="{
              'text-surface-900 dark:text-surface-0': tool.active,
              'text-surface-500': !tool.active
            }">{{ tool.name }}</h3>

            <!-- Features List for Active Tools -->
            <div v-if="tool.active && tool.features" class="mb-2">
              <ul class="text-sm text-surface-600 dark:text-surface-400 space-y-1">
                <li v-for="feature in tool.features" :key="feature" class="flex items-center">
                  <i class="pi pi-check text-green-500 text-xs mr-2"></i>
                  {{ feature }}
                </li>
              </ul>
            </div>

            <!-- Simple Description for Inactive Tools -->
            <div v-else-if="!tool.active">
              <p class="text-surface-600 dark:text-surface-400 mb-2 text-sm">{{ tool.description }}</p>
              <div class="text-xs text-surface-500 italic">
                Coming later
              </div>
            </div>
          </div>
        </template>
      </Card>
    </div>

    <!-- Feature Selection Section -->
    <div v-if="selectedTool" class="mt-12">
      <div class="flex flex-col items-start gap-2 mb-8">
        <div class="text-surface-900 dark:text-surface-0 font-semibold text-2xl">
          {{ getSelectedToolName() }} Recipe 기능 선택
        </div>
        <div class="text-surface-500 dark:text-surface-300 text-lg">
          원하는 기능을 선택하고 Recipe를 검색하세요
        </div>
      </div>
      
      <RecipeFeatureSelector 
        :tool-type="selectedTool" 
        :recipe-list="recipeList?.recipe_list || []"
        :is-loading="isLoadingRecipes"
        :error="recipeError"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import Card from 'primevue/card'
import RecipeFeatureSelector from './components/RecipeFeatureSelector.vue'
import { useRecipeList } from '@/services/recipeService'

const route = useRoute()
const selectedTool = ref(null)

// Get facility ID from route
const facId = computed(() => route.params.fac_id || 'R3')

// Fetch recipe list when tool is selected
const { 
  data: recipeList, 
  isLoading: isLoadingRecipes, 
  error: recipeError 
} = useRecipeList(facId, selectedTool)

const toolCategories = [
  {
    id: 'cd-sem',
    name: 'CD-SEM',
    icon: 'pi pi-search',
    active: true,
    features: [
      'Recipe 열기',
      '횡전개 체크',
      '측정 히스토리'
    ]
  },
  {
    id: 'hv-sem',
    name: 'HV-SEM',
    icon: 'pi pi-bolt',
    active: true,
    features: [
      'Recipe 열기',
      '횡전개 체크',
      '측정 히스토리'
    ]
  },
  {
    id: 'verity',
    name: 'VeritySEM',
    icon: 'pi pi-verified',
    active: false
  },
  {
    id: 'provision',
    name: 'Provision',
    icon: 'pi pi-forward',
    active: false
  }
]

// Select a tool and show feature selector below
const selectTool = (toolId) => {
  selectedTool.value = toolId
}

// Get selected tool name
const getSelectedToolName = () => {
  const tool = toolCategories.find(t => t.id === selectedTool.value)
  return tool ? tool.name : ''
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>
