<template>
  <div class="main-page relative">
    <!-- Fab Selection Alert (shown temporarily when navigation is blocked) -->
    <transition name="slide-fade">
      <div v-if="showFabAlert" class="fixed top-20 right-4 z-50">
        <div
          class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4 shadow-lg max-w-sm">
          <div class="flex items-start gap-3">
            <i class="pi pi-exclamation-triangle text-amber-600 dark:text-amber-400 text-xl mt-0.5" />
            <div class="flex-1">
              <h4 class="font-semibold text-amber-800 dark:text-amber-300 mb-1">Fab Selection Required</h4>
              <p class="text-sm text-amber-700 dark:text-amber-400 mb-3">
                Please select your fabrication facility to access this feature
              </p>
              <Select v-model="localSelectedFab" :options="fabList" placeholder="Select Fab" class="w-full"
                @change="handleFabChange" />
            </div>
            <button @click="showFabAlert = false"
              class="text-amber-600 dark:text-amber-400 hover:text-amber-800 dark:hover:text-amber-300 transition-colors">
              <i class="pi pi-times" />
            </button>
          </div>
        </div>
      </div>
    </transition>

    <!-- Welcome Header -->
    <div class="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-8 rounded-lg mb-8">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-4xl font-bold mb-2">Welcome to SKEWNONO</h1>
          <p class="text-xl opacity-90">
            Metrology SEM Management System{{ selectedFab ? ` - ${selectedFab} Fab` : '' }}
          </p>
        </div>
        <div class="text-right">
          <i class="pi pi-building text-6xl opacity-70" />
        </div>
      </div>
    </div>

    <!-- Dashboard Grid -->
    <div class="grid grid-cols-3 gap-6 mb-8">
      <!-- Equipment Status Card -->
      <div @click="handleNavigation('/equipment-status')" class="group">
        <div :class="[
          'bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg transition-all duration-300 border-l-4 border-blue-500',
          selectedFab ? 'hover:shadow-xl cursor-pointer' : 'opacity-60 cursor-not-allowed'
        ]">
          <div class="flex items-center justify-between mb-4">
            <i class="pi pi-desktop text-3xl text-blue-500" />
            <span class="text-sm text-gray-500 dark:text-gray-400 group-hover:text-blue-500 transition-colors">
              <i class="pi pi-arrow-right" />
            </span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">장비 현황</h3>
          <p class="text-gray-600 dark:text-gray-300">Equipment status monitoring</p>
        </div>
      </div>

      <!-- Recipe Search Card -->
      <div @click="handleNavigation('/recipe-search')" class="group">
        <div :class="[
          'bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg transition-all duration-300 border-l-4 border-green-500',
          selectedFab ? 'hover:shadow-xl cursor-pointer' : 'opacity-60 cursor-not-allowed'
        ]">
          <div class="flex items-center justify-between mb-4">
            <i class="pi pi-search text-3xl text-green-500" />
            <span class="text-sm text-gray-500 dark:text-gray-400 group-hover:text-green-500 transition-colors">
              <i class="pi pi-arrow-right" />
            </span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Recipe 검색</h3>
          <p class="text-gray-600 dark:text-gray-300">Recipe search and management</p>
        </div>
      </div>

      <!-- Device Statistics Card -->
      <div @click="handleNavigation('/device-statistics')" class="group">
        <div :class="[
          'bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg transition-all duration-300 border-l-4 border-purple-500',
          selectedFab ? 'hover:shadow-xl cursor-pointer' : 'opacity-60 cursor-not-allowed'
        ]">
          <div class="flex items-center justify-between mb-4">
            <i class="pi pi-chart-bar text-3xl text-purple-500" />
            <span class="text-sm text-gray-500 dark:text-gray-400 group-hover:text-purple-500 transition-colors">
              <i class="pi pi-arrow-right" />
            </span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">디바이스 통계</h3>
          <p class="text-gray-600 dark:text-gray-300">Device statistics and analytics</p>
        </div>
      </div>

      <!-- Fail Issue Card -->
      <div @click="handleNavigation('/fail-issue')" class="group">
        <div :class="[
          'bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg transition-all duration-300 border-l-4 border-red-500',
          selectedFab ? 'hover:shadow-xl cursor-pointer' : 'opacity-60 cursor-not-allowed'
        ]">
          <div class="flex items-center justify-between mb-4">
            <i class="pi pi-exclamation-triangle text-3xl text-red-500" />
            <span class="text-sm text-gray-500 dark:text-gray-400 group-hover:text-red-500 transition-colors">
              <i class="pi pi-arrow-right" />
            </span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Fail Issue</h3>
          <p class="text-gray-600 dark:text-gray-300">Issue tracking and management</p>
        </div>
      </div>

      <!-- Hardware Management Card -->
      <div @click="handleNavigation('/hardware-management')" class="group">
        <div :class="[
          'bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg transition-all duration-300 border-l-4 border-orange-500',
          selectedFab ? 'hover:shadow-xl cursor-pointer' : 'opacity-60 cursor-not-allowed'
        ]">
          <div class="flex items-center justify-between mb-4">
            <i class="pi pi-cog text-3xl text-orange-500" />
            <span class="text-sm text-gray-500 dark:text-gray-400 group-hover:text-orange-500 transition-colors">
              <i class="pi pi-arrow-right" />
            </span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">H/W 관리</h3>
          <p class="text-gray-600 dark:text-gray-300">Hardware management system</p>
        </div>
      </div>

      <!-- Skewboa Card (No fab requirement) -->
      <div @click="handleNavigation('/skewvoir')" class="group">
        <div
          class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300 border-l-4 border-teal-500 cursor-pointer">
          <div class="flex items-center justify-between mb-4">
            <i class="pi pi-eye text-3xl text-teal-500" />
            <span class="text-sm text-gray-500 dark:text-gray-400 group-hover:text-teal-500 transition-colors">
              <i class="pi pi-arrow-right" />
            </span>
          </div>
          <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">스큐보아</h3>
          <p class="text-gray-600 dark:text-gray-300">Data visualization and viewer</p>
        </div>
      </div>
    </div>

    <!-- API Status -->
    <div class="mb-6">
      <div :class="[
        'inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all',
        apiStatus === 'checking' && 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
        apiStatus === 'connected' && 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
        apiStatus === 'error' && 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
      ]">
        <i :class="[
          'pi',
          apiStatus === 'checking' && 'pi-spin pi-spinner',
          apiStatus === 'connected' && 'pi-check-circle',
          apiStatus === 'error' && 'pi-times-circle'
        ]" />
        <span>{{ apiMessage }}</span>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-4">
        Quick Overview - {{ selectedFab }} Fab
      </h2>
      <div class="grid grid-cols-4 gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600 mb-1">24</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Active Equipment</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600 mb-1">98.5%</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Uptime</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-purple-600 mb-1">156</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Recipes</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-orange-600 mb-1">2</div>
          <div class="text-sm text-gray-500 dark:text-gray-400">Active Issues</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'
import { storeToRefs } from 'pinia'
import Select from 'primevue/select'
import { useToast } from 'primevue/usetoast'
import { useFabStore } from '@/stores/fab'
import { healthQueries } from '@/services/healthService'

const router = useRouter()
const route = useRoute()
const toast = useToast()

// Use Pinia store directly
const fabStore = useFabStore()
const { selectedFab, fabList } = storeToRefs(fabStore)

// Local fab selection for the alert
const localSelectedFab = ref(selectedFab.value || '')

// Alert state
const showFabAlert = ref(false)
let alertTimeout = null

// Use Vue Query for health check
const { data: healthData, isLoading, isError } = useQuery(healthQueries.health())

// Computed API status based on query state
const apiStatus = ref('checking')
const apiMessage = ref('')

watch([isLoading, isError, healthData], ([loading, error, data]) => {
  if (loading) {
    apiStatus.value = 'checking'
    apiMessage.value = 'Checking API connection...'
  } else if (error) {
    apiStatus.value = 'error'
    apiMessage.value = 'API Connection Failed'
  } else if (data) {
    apiStatus.value = 'connected'
    apiMessage.value = data.message || 'API Connected'
  }
})

// Handle fab selection change
const handleFabChange = (event) => {
  const newFab = event.value || event
  if (newFab) {
    fabStore.setSelectedFab(newFab)
    localSelectedFab.value = newFab
  }
}

// Watch for selectedFab changes
watch(selectedFab, (newVal) => {
  localSelectedFab.value = newVal || ''
  // Hide alert when fab is selected
  if (newVal) {
    showFabAlert.value = false
  }
})

// Handle navigation with fab check
const handleNavigation = (path) => {
  // Special case: SkewVoir doesn't require fab selection
  if (path === '/skewvoir') {
    router.push(path)
    return
  }

  if (!selectedFab.value) {
    // Show toast notification
    console.log('Showing toast notification for fab selection')
    toast.add({
      severity: 'warn',
      summary: 'Fab Selection Required',
      detail: 'Please select a fabrication facility in the header to access this feature',
      life: 3000
    })

    // Also show the fab selection alert
    showFabAlert.value = true

    // Auto-hide after 10 seconds
    if (alertTimeout) clearTimeout(alertTimeout)
    alertTimeout = setTimeout(() => {
      showFabAlert.value = false
    }, 10000)

    return
  }

  // Build URL with fac_id
  const urlWithFab = `/${selectedFab.value}${path}`
  router.push(urlWithFab)
}

// Handle query parameters for edge cases
onMounted(() => {
  if (route.query.needsFab) {
    toast.add({
      severity: 'warn',
      summary: 'Fab Selection Required',
      detail: 'Please select a fabrication facility to access this feature',
      life: 5000
    })
    showFabAlert.value = true
  }
  
  if (route.query.invalidFab) {
    toast.add({
      severity: 'error',
      summary: 'Invalid Fab',
      detail: `The fab "${route.query.invalidFab}" is not valid. Please select a valid fabrication facility.`,
      life: 5000
    })
    showFabAlert.value = true
  }
})

// Cleanup on unmount
onUnmounted(() => {
  if (alertTimeout) {
    clearTimeout(alertTimeout)
  }
})
</script>

<style scoped>
/* Slide fade transition */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s ease-in;
}

.slide-fade-enter-from {
  transform: translateX(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(20px);
  opacity: 0;
}
</style>
