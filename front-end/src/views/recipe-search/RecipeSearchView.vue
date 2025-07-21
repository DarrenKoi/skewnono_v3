<template>
  <div class="recipe-search bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">레시피 검색</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">
        도구 카테고리를 선택하세요
      </div>
    </div>

    <!-- Tool Category Selection -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
      <Card 
        v-for="tool in toolCategories" 
        :key="tool.id"
        :class="{
          'cursor-pointer transition-all duration-200': tool.active,
          'opacity-50 cursor-not-allowed': !tool.active,
          'shadow-lg border-primary-500 border-2': tool.active && selectedTool === tool.id,
          'hover:shadow-lg': tool.active && selectedTool !== tool.id
        }"
        @click="tool.active ? selectTool(tool.id) : null"
      >
        <template #content>
          <div class="text-center p-4">
            <i :class="[tool.icon, {
              'text-primary-500': tool.active && selectedTool === tool.id,
              'text-surface-600': tool.active && selectedTool !== tool.id,
              'text-surface-400': !tool.active
            }]" class="text-4xl mb-4"></i>
            <h3 class="text-xl font-semibold mb-2" :class="{
              'text-primary-600 dark:text-primary-400': tool.active && selectedTool === tool.id,
              'text-surface-900 dark:text-surface-0': tool.active && selectedTool !== tool.id,
              'text-surface-500': !tool.active
            }">{{ tool.name }}</h3>
            <p class="text-surface-600 dark:text-surface-400 mb-2">{{ tool.description }}</p>
            <div v-if="!tool.active" class="text-xs text-surface-500 italic">
              Coming later
            </div>
          </div>
        </template>
      </Card>
    </div>

    <!-- Recipe Search Content - Show below tool selection -->
    <transition name="fade" mode="out-in">
      <div v-if="selectedTool" class="mt-8">
        <Divider />
        
        <!-- CD-SEM specific content -->
        <div v-if="selectedTool === 'cd-sem'" class="mt-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-semibold text-surface-900 dark:text-surface-0">
              CD-SEM 레시피 검색
            </h2>
            <Button 
              label="선택 초기화" 
              icon="pi pi-refresh" 
              severity="secondary" 
              size="small"
              @click="resetSelection"
            />
          </div>

          <!-- CD-SEM Recipe Search Content -->
          <CdSemRecipeContent />
        </div>

        <!-- HV-SEM specific content -->
        <div v-else-if="selectedTool === 'hv-sem'" class="mt-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-semibold text-surface-900 dark:text-surface-0">
              HV-SEM 레시피 검색
            </h2>
            <Button 
              label="선택 초기화" 
              icon="pi pi-refresh" 
              severity="secondary" 
              size="small"
              @click="resetSelection"
            />
          </div>

          <!-- HV-SEM Recipe Search Content -->
          <HvSemRecipeContent />
        </div>

        <!-- Placeholder for other tools -->
        <div v-else class="mt-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-2xl font-semibold text-surface-900 dark:text-surface-0">
              {{ getToolName(selectedTool) }} 레시피 검색
            </h2>
            <Button 
              label="선택 초기화" 
              icon="pi pi-refresh" 
              severity="secondary" 
              size="small"
              @click="resetSelection"
            />
          </div>
          
          <Message severity="info" :closable="false">
            <p>{{ getToolName(selectedTool) }} 도구의 레시피 검색 기능은 준비 중입니다.</p>
          </Message>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import Card from 'primevue/card'
import Divider from 'primevue/divider'
import Button from 'primevue/button'
import Message from 'primevue/message'
import CdSemRecipeContent from './cd-sem/CdSemRecipeContent.vue'
import HvSemRecipeContent from './hv-sem/HvSemRecipeContent.vue'

const route = useRoute()

// Get fac_id from route params
const facId = computed(() => route.params.fac_id || 'R3')

// Selected tool state
const selectedTool = ref(null)

const toolCategories = [
  {
    id: 'cd-sem',
    name: 'CD-SEM',
    description: 'CD-SEM 레시피 검색',
    icon: 'pi pi-search',
    active: true
  },
  {
    id: 'hv-sem',
    name: 'HV-SEM',
    description: 'HV-SEM 레시피 검색',
    icon: 'pi pi-bolt',
    active: true
  },
  {
    id: 'verity',
    name: 'VeritySEM',
    description: 'VeritySEM 레시피 검색',
    icon: 'pi pi-verified',
    active: false
  },
  {
    id: 'provision',
    name: 'Provision',
    description: 'Provision 레시피 검색',
    icon: 'pi pi-forward',
    active: false
  }
]

// Select a tool and show its content below
const selectTool = (toolId) => {
  selectedTool.value = toolId
}

// Reset selection
const resetSelection = () => {
  selectedTool.value = null
}

// Get tool name by ID
const getToolName = (toolId) => {
  const tool = toolCategories.find(t => t.id === toolId)
  return tool ? tool.name : ''
}
</script>

<style scoped>
/* Transition animations */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Page-specific styles if needed */
</style>