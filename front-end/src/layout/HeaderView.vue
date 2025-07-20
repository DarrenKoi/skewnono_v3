<template>
  <header
    class="bg-surface-0 dark:bg-surface-900 py-4 px-12 border-b border-surface-200 dark:border-surface-800 flex items-center justify-between relative lg:static">
    <router-link to="/" class="flex items-center gap-4 py-2 no-underline">
      <!-- <img src="@/assets/skewnono.png" alt="Logo" class="w-8 h-8" /> -->
      <span
        class="flex items-center text-xl font-bold text-surface-900 dark:text-surface-0 hover:text-primary transition-colors duration-150">
        <i class="pi pi-ruler mr-2 text-primary"></i>
        <span class="bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">CD-SEM Data
          Solution</span>

      </span>
    </router-link>

    <a v-styleclass="{
      selector: '@next',
      enterFromClass: 'hidden',
      leaveToClass: 'hidden',
      hideOnOutsideClick: true
    }" class="cursor-pointer block lg:hidden text-surface-700 dark:text-surface-100 mt-1">
      <i class="pi pi-bars !text-2xl" />
    </a>

    <div
      class="items-center grow justify-between hidden lg:flex absolute lg:static w-full bg-surface-0 dark:bg-surface-900 left-0 top-full px-12 lg:px-0 z-50 shadow lg:shadow-none">
      <!-- Mobile Fab Selection -->
      <div class="block lg:hidden w-full px-4 py-2 border-b border-surface-200 dark:border-surface-700">
        <div
          class="flex items-center gap-2 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 px-4 py-2 rounded-lg border border-blue-200 dark:border-blue-700">
          <i class="pi pi-warehouse text-blue-600 dark:text-blue-400" />
          <Select v-model="fabStore.selectedFab" :options="fabStore.fabList" checkmark placeholder="Select Fab"
            class="w-full fab-select" @change="handleFabChange" />
        </div>
      </div>

      <!-- Center section with Fab Selection and Navigation -->
      <div class="flex items-center justify-center flex-1">
        <!-- Fab Selection - Desktop -->
        <div
          class="hidden lg:flex items-center gap-2 mr-8 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 px-4 py-2 rounded-lg border border-blue-200 dark:border-blue-700 shadow-sm">
          <i class="pi pi-warehouse text-blue-600 dark:text-blue-400" />
          <Select v-model="fabStore.selectedFab" :options="fabStore.fabList" checkmark placeholder="Select Fab"
            class="w-32 fab-select" @change="handleFabChange" />
        </div>

        <!-- Navigation Menu -->
        <ul
          class="list-none p-0 py-4 lg:py-0 m-0 flex lg:items-center text-surface-900 dark:text-surface-0 select-none flex-col lg:flex-row cursor-pointer">
          <li class="w-full lg:w-auto">
            <a @click.prevent="handleNavigation('/equipment-status')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/equipment-status') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-desktop" />
              <span>장비 현황</span>
            </a>
          </li>
          <li class="w-full lg:w-auto">
            <a @click.prevent="handleNavigation('/recipe-search')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/recipe-search') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-search" />
              <span>Recipe 검색</span>
            </a>
          </li>
          <li class="w-full lg:w-auto">
            <a @click.prevent="handleNavigation('/device-statistics')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/device-statistics') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-chart-bar" />
              <span>디바이스 통계</span>
            </a>
          </li>
          <li class="w-full lg:w-auto">
            <a @click.prevent="handleNavigation('/fail-issue')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/fail-issue') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-exclamation-triangle" />
              <span>Fail Issue</span>
            </a>
          </li>
          <li class="w-full lg:w-auto">
            <a @click.prevent="handleNavigation('/hardware-management')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/hardware-management') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-cog" />
              <span>H/W 관리</span>
            </a>
          </li>
          <li class="w-full lg:w-auto">
            <a @click.prevent="handleNavigation('/skewvoir')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path === '/skewvoir' ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-eye" />
              <span>스큐보아</span>
              <Badge value="BETA" severity="warning" class="ml-1 !text-xs !px-1 !py-0.5" />
            </a>
          </li>
        </ul>
      </div>

      <!-- Right Side - Info Link -->
      <div class="flex items-center border-t lg:border-t-0 border-surface py-4 lg:py-0 mt-4 lg:mt-0">
        <router-link to="/about"
          class="flex items-center gap-2 text-surface-600 dark:text-surface-400 hover:text-primary transition-colors duration-150 no-underline">
          <i class="pi pi-info-circle !text-xl" />
          <span class="font-medium">정보</span>
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import Select from 'primevue/select'
import Badge from 'primevue/badge'
import { useToast } from 'primevue/usetoast'
import { useFabStore } from '@/stores/fab'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const fabStore = useFabStore()

// Handle fab selection change
const handleFabChange = (event) => {
  // event.value contains the selected value when using @change
  const newFab = event.value || event
  if (newFab) {
    fabStore.setSelectedFab(newFab)

    // If we're on a fab-specific route, redirect to the new fab
    if (route.params.fac_id) {
      const currentPath = route.path.replace(`/${route.params.fac_id}`, '')
      const newPath = `/${newFab}${currentPath}`
      router.push(newPath)
    }
  }
}

// Handle navigation with fab check
const handleNavigation = (path) => {
  // Check if fab is selected for all routes
  if (!fabStore.selectedFab) {
    toast.add({
      severity: 'warn',
      summary: 'Fab Selection Required',
      detail: 'Please select a fabrication facility to access this feature',
      life: 3000
    })
    return
  }

  // Build URL with fac_id
  const urlWithFab = `/${fabStore.selectedFab}${path}`
  router.push(urlWithFab)
}
</script>

<style scoped>
@keyframes scalein {
  from {
    opacity: 0;
    transform: scale(0.9);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes fadeout {
  from {
    opacity: 1;
  }

  to {
    opacity: 0;
  }
}

.animate-scalein {
  animation: scalein 0.2s ease-out;
}

.animate-fadeout {
  animation: fadeout 0.2s ease-out;
}

/* Fab Selection Styling */
.fab-select {
  filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.15));
}

.fab-select:hover {
  filter: drop-shadow(0 4px 8px rgba(59, 130, 246, 0.25));
  transform: translateY(-1px);
  transition: all 0.2s ease-out;
}
</style>
