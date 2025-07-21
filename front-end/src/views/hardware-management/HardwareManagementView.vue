<template>
  <div class="hardware-management bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">하드웨어 관리</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">
        도구 카테고리를 선택하세요
      </div>
    </div>

    <!-- Tool Category Selection -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <Card 
        v-for="tool in toolCategories" 
        :key="tool.id"
        :class="{
          'cursor-pointer hover:shadow-lg transition-shadow duration-200': tool.active,
          'opacity-50 cursor-not-allowed': !tool.active
        }"
        @click="tool.active ? navigateToTool(tool.id) : null"
      >
        <template #content>
          <div class="text-center p-4">
            <i :class="[tool.icon, {
              'text-primary-500': tool.active,
              'text-surface-400': !tool.active
            }]" class="text-4xl mb-4"></i>
            <h3 class="text-xl font-semibold mb-2" :class="{
              'text-surface-900 dark:text-surface-0': tool.active,
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
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import Card from 'primevue/card'

const router = useRouter()
const route = useRoute()

const toolCategories = [
  {
    id: 'cd-sem',
    name: 'CD-SEM',
    description: 'CD-SEM 하드웨어 관리',
    icon: 'pi pi-search',
    active: true
  },
  {
    id: 'hv-sem',
    name: 'HV-SEM',
    description: 'HV-SEM 하드웨어 관리',
    icon: 'pi pi-bolt',
    active: false
  },
  {
    id: 'verity',
    name: 'VeritySEM',
    description: 'VeritySEM 하드웨어 관리',
    icon: 'pi pi-verified',
    active: false
  },
  {
    id: 'provision',
    name: 'Provision',
    description: 'Provision 하드웨어 관리',
    icon: 'pi pi-forward',
    active: false
  }
]

const navigateToTool = (toolId) => {
  const facId = route.params.fac_id || 'R3'
  router.push({
    name: `hardware-management-${toolId}`,
    params: { fac_id: facId }
  })
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>