<template>
  <header
    class="bg-surface-0 dark:bg-surface-900 py-4 px-12 border-b border-surface-200 dark:border-surface-800 flex items-center justify-between relative lg:static">
    <router-link to="/"
      class="flex items-center gap-2 py-2 no-underline text-xl font-bold text-surface-900 dark:text-surface-0 transition-transform duration-200 ease-in-out hover:scale-105">
      <!-- <img src="@/assets/skewnono.png" alt="Logo" class="w-8 h-8" /> -->
      <i class="pi pi-ruler text-primary"></i>
      <span class="bg-gradient-to-r from-primary to-blue-600 bg-clip-text text-transparent">{{ dynamicTitle }}</span>
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
      <!-- Mobile Fab & Tool Selection -->
      <div class="block lg:hidden w-full px-4 py-2 border-b border-surface-200 dark:border-surface-700">
        <div
          class="flex items-center gap-2 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 px-4 py-2 rounded-lg border border-blue-200 dark:border-blue-700">
          <i class="pi pi-cog text-blue-600 dark:text-blue-400" />
          <CascadeSelect 
            v-model="cascadeSelection" 
            :options="fabStore.cascadeOptions" 
            option-label="label" 
            option-value="value"
            placeholder="Select Fab & Tool"
            class="w-full fab-tool-select" 
            @change="handleCascadeChange" />
        </div>
      </div>

      <!-- Center section with Fab Selection and Navigation -->
      <div class="flex items-center justify-center flex-1">
        <!-- Fab & Tool Selection - Desktop -->
        <div
          class="hidden lg:flex items-center gap-2 mr-8 bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/30 dark:to-indigo-900/30 px-4 py-2 rounded-lg border border-blue-200 dark:border-blue-700 shadow-sm">
          <i class="pi pi-cog text-blue-600 dark:text-blue-400" />
          <CascadeSelect 
            v-model="cascadeSelection" 
            :options="fabStore.cascadeOptions" 
            option-label="label" 
            option-value="value"
            placeholder="Select Fab & Tool"
            class="w-48 fab-tool-select" 
            @change="handleCascadeChange" />
        </div>

        <!-- Navigation Menu -->
        <ul
          class="list-none p-0 py-4 lg:py-0 m-0 flex lg:items-center text-surface-900 dark:text-surface-0 select-none flex-col lg:flex-row cursor-pointer">
          <!-- Equipment Status -->
          <li class="w-full lg:w-auto relative" @mouseenter="showDropdown('equipment')" @mouseleave="hideDropdown('equipment')">
            <a @click.prevent="handleNavigation('/equipment-status')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/equipment-status') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-desktop" />
              <span>장비 현황</span>
              <i class="pi pi-chevron-down text-xs ml-1" />
            </a>
            <Menu 
              ref="equipmentMenu" 
              :model="equipmentMenuItems" 
              :popup="true" 
              class="absolute top-full left-0 mt-1 z-50" 
              @show="activeDropdown = 'equipment'" 
              @hide="activeDropdown = null" />
          </li>
          <!-- Recipe Search -->
          <li class="w-full lg:w-auto relative" @mouseenter="showDropdown('recipe')" @mouseleave="hideDropdown('recipe')">
            <a @click.prevent="handleNavigation('/recipe-search')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/recipe-search') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-search" />
              <span>Recipe 검색</span>
              <i class="pi pi-chevron-down text-xs ml-1" />
            </a>
            <Menu 
              ref="recipeMenu" 
              :model="recipeMenuItems" 
              :popup="true" 
              class="absolute top-full left-0 mt-1 z-50" 
              @show="activeDropdown = 'recipe'" 
              @hide="activeDropdown = null" />
          </li>
          <!-- Device Statistics -->
          <li class="w-full lg:w-auto relative" @mouseenter="showDropdown('statistics')" @mouseleave="hideDropdown('statistics')">
            <a @click.prevent="handleNavigation('/device-statistics')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/device-statistics') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-chart-bar" />
              <span>디바이스 통계</span>
              <i class="pi pi-chevron-down text-xs ml-1" />
            </a>
            <Menu 
              ref="statisticsMenu" 
              :model="statisticsMenuItems" 
              :popup="true" 
              class="absolute top-full left-0 mt-1 z-50" 
              @show="activeDropdown = 'statistics'" 
              @hide="activeDropdown = null" />
          </li>
          <!-- Fail Issue -->
          <li class="w-full lg:w-auto relative" @mouseenter="showDropdown('fail')" @mouseleave="hideDropdown('fail')">
            <a @click.prevent="handleNavigation('/fail-issue')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/fail-issue') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-exclamation-triangle" />
              <span>Fail Issue</span>
              <i class="pi pi-chevron-down text-xs ml-1" />
            </a>
            <Menu 
              ref="failMenu" 
              :model="failMenuItems" 
              :popup="true" 
              class="absolute top-full left-0 mt-1 z-50" 
              @show="activeDropdown = 'fail'" 
              @hide="activeDropdown = null" />
          </li>
          <!-- Hardware Management -->
          <li class="w-full lg:w-auto relative" @mouseenter="showDropdown('hardware')" @mouseleave="hideDropdown('hardware')">
            <a @click.prevent="handleNavigation('/hardware-management')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/hardware-management') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-cog" />
              <span>H/W 관리</span>
              <i class="pi pi-chevron-down text-xs ml-1" />
            </a>
            <Menu 
              ref="hardwareMenu" 
              :model="hardwareMenuItems" 
              :popup="true" 
              class="absolute top-full left-0 mt-1 z-50" 
              @show="activeDropdown = 'hardware'" 
              @hide="activeDropdown = null" />
          </li>
          <!-- SkewVoir -->
          <li class="w-full lg:w-auto relative" @mouseenter="showDropdown('skewvoir')" @mouseleave="hideDropdown('skewvoir')">
            <a @click.prevent="handleNavigation('/skewvoir')"
              class="flex px-4 lg:px-6 py-3 hover:text-primary font-medium transition-all duration-150 items-center gap-2 rounded-md cursor-pointer"
              :class="route.path.includes('/skewvoir') ? 'text-primary bg-primary/10' : 'hover:bg-surface-100 dark:hover:bg-surface-800'">
              <i class="pi pi-eye" />
              <span>스큐보아</span>
              <Badge value="BETA" severity="warning" class="ml-1 !text-xs !px-1 !py-0.5" />
              <i class="pi pi-chevron-down text-xs ml-1" />
            </a>
            <Menu 
              ref="skewvoirMenu" 
              :model="skewvoirMenuItems" 
              :popup="true" 
              class="absolute top-full left-0 mt-1 z-50" 
              @show="activeDropdown = 'skewvoir'" 
              @hide="activeDropdown = null" />
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
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import CascadeSelect from 'primevue/cascadeselect'
import Menu from 'primevue/menu'
import Badge from 'primevue/badge'
import { useToast } from 'primevue/usetoast'
import { useFabStore } from '@/stores/fab'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const fabStore = useFabStore()

// Refs for menu components
const equipmentMenu = ref()
const recipeMenu = ref()
const statisticsMenu = ref()
const failMenu = ref()
const hardwareMenu = ref()
const skewvoirMenu = ref()

// Dropdown state
const activeDropdown = ref(null)
const dropdownTimeout = ref(null)

// Cascade selection state
const cascadeSelection = computed({
  get() {
    if (fabStore.hasCompleteSelection) {
      return [fabStore.currentFab, fabStore.currentTool]
    }
    return null
  },
  set(value) {
    if (value && value.length === 2) {
      fabStore.setCascadeSelection(value)
    }
  }
})

// Dynamic title based on selected tool
const dynamicTitle = computed(() => {
  const tool = fabStore.currentTool
  if (tool === 'CD-SEM') {
    return 'CD-SEM Data Platform'
  } else if (tool === 'HV-SEM') {
    return 'HV-SEM Data Platform'
  }
  return 'SEM Data Platform'
})

// Handle cascade selection change
const handleCascadeChange = (event) => {
  const selection = event.value
  if (selection && selection.length === 2) {
    fabStore.setCascadeSelection(selection)
    
    // If we're on a fab-specific route, redirect to the new fab
    if (route.params.fac_id) {
      const currentPath = route.path.replace(`/${route.params.fac_id}`, '')
      const newPath = `/${selection[0]}${currentPath}`
      router.push(newPath)
    }
  }
}

// Handle navigation with fab and tool check
const handleNavigation = (path) => {
  // Check if fab and tool are selected for all routes
  if (!fabStore.hasCompleteSelection) {
    toast.add({
      severity: 'warn',
      summary: 'Selection Required',
      detail: 'Please select both a fabrication facility and tool to access this feature',
      life: 3000
    })
    return
  }

  // Build URL with fac_id
  const urlWithFab = `/${fabStore.selectedFab}${path}`
  router.push(urlWithFab)
}

// Dropdown menu items
const equipmentMenuItems = computed(() => [
  {
    label: 'Current Status',
    icon: 'pi pi-desktop',
    command: () => handleNavigation('/equipment-status/current-status')
  },
  {
    label: 'Storage',
    icon: 'pi pi-database',
    command: () => handleNavigation('/equipment-status/storage')
  },
  {
    label: 'Not Available',
    icon: 'pi pi-ban',
    command: () => handleNavigation('/equipment-status/not_available')
  }
])

const recipeMenuItems = computed(() => {
  const tool = fabStore.currentTool?.toLowerCase()
  if (!tool) return []
  
  return [
    {
      label: 'Recipe Open',
      icon: 'pi pi-folder-open',
      command: () => handleNavigation(`/recipe-search/${tool}/open`)
    },
    {
      label: 'Horizontal Check',
      icon: 'pi pi-arrows-h',
      command: () => handleNavigation(`/recipe-search/${tool}/horizontal-check`)
    },
    {
      label: 'Measurement History',
      icon: 'pi pi-history',
      command: () => handleNavigation(`/recipe-search/${tool}/measurement-history`)
    }
  ]
})

const statisticsMenuItems = computed(() => {
  const tool = fabStore.currentTool?.toLowerCase()
  if (!tool) return []
  
  return [
    {
      label: 'Current Status',
      icon: 'pi pi-chart-bar',
      command: () => handleNavigation(`/device-statistics/${tool}/current-status`)
    },
    {
      label: 'Weekly Trend',
      icon: 'pi pi-chart-line',
      command: () => handleNavigation(`/device-statistics/${tool}/weekly-trend`)
    }
  ]
})

const failMenuItems = computed(() => {
  const tool = fabStore.currentTool?.toLowerCase()
  if (!tool) return []
  
  return [
    {
      label: `${fabStore.currentTool} Issues`,
      icon: 'pi pi-exclamation-triangle',
      command: () => handleNavigation(`/fail-issue/${tool}`)
    }
  ]
})

const hardwareMenuItems = computed(() => {
  const tool = fabStore.currentTool?.toLowerCase()
  if (!tool) return []
  
  return [
    {
      label: `${fabStore.currentTool} Hardware`,
      icon: 'pi pi-cog',
      command: () => handleNavigation(`/hardware-management/${tool}`)
    }
  ]
})

const skewvoirMenuItems = computed(() => {
  const tool = fabStore.currentTool?.toLowerCase()
  if (!tool) return []
  
  return [
    {
      label: `${fabStore.currentTool} Analysis`,
      icon: 'pi pi-eye',
      command: () => handleNavigation(`/skewvoir/${tool}`)
    }
  ]
})

// Dropdown handlers
const showDropdown = (menuType) => {
  if (dropdownTimeout.value) {
    clearTimeout(dropdownTimeout.value)
    dropdownTimeout.value = null
  }
  
  if (activeDropdown.value !== menuType) {
    activeDropdown.value = menuType
    
    // Show the appropriate menu
    const menuRef = {
      equipment: equipmentMenu,
      recipe: recipeMenu,
      statistics: statisticsMenu,
      fail: failMenu,
      hardware: hardwareMenu,
      skewvoir: skewvoirMenu
    }[menuType]
    
    if (menuRef?.value) {
      menuRef.value.show(new Event('show'))
    }
  }
}

const hideDropdown = (menuType) => {
  dropdownTimeout.value = setTimeout(() => {
    if (activeDropdown.value === menuType) {
      activeDropdown.value = null
      
      // Hide the appropriate menu
      const menuRef = {
        equipment: equipmentMenu,
        recipe: recipeMenu,
        statistics: statisticsMenu,
        fail: failMenu,
        hardware: hardwareMenu,
        skewvoir: skewvoirMenu
      }[menuType]
      
      if (menuRef?.value) {
        menuRef.value.hide()
      }
    }
  }, 200) // Small delay to prevent flickering
}

// Initialize fab selection on mount
onMounted(() => {
  fabStore.initializeFabSelection()
})
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

/* Fab & Tool Selection Styling */
.fab-tool-select {
  filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.15));
}

.fab-tool-select:hover {
  filter: drop-shadow(0 4px 8px rgba(59, 130, 246, 0.25));
  transform: translateY(-1px);
  transition: all 0.2s ease-out;
}

/* Dropdown Menu Styling */
.relative:hover .absolute {
  opacity: 1;
  transform: translateY(0);
  visibility: visible;
}

/* Menu animations */
:deep(.p-menu) {
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(var(--surface-200));
  border-radius: 0.5rem;
  background: rgba(var(--surface-0));
  min-width: 200px;
}

:deep(.p-menu .p-menuitem-link) {
  padding: 0.75rem 1rem;
  transition: all 0.15s ease;
}

:deep(.p-menu .p-menuitem-link:hover) {
  background: rgba(var(--primary-color), 0.1);
  color: rgba(var(--primary-color));
}

/* Tool-specific theming */
.cd-sem-theme {
  --primary-color: 59, 130, 246; /* Blue */
}

.hv-sem-theme {
  --primary-color: 34, 197, 94; /* Green */
}
</style>
