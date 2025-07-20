<template>
  <div class="skewvoir-homepage min-h-screen flex flex-col">
    <!-- Main content container -->
    <div class="flex-1 flex flex-col items-center justify-center px-6">
      <!-- Logo section -->
      <div class="mb-8 text-center">
        <div class="mb-4">
          <!-- SkewVoir logo with colorful letters inspired by Google -->
          <h1 class="text-6xl md:text-7xl lg:text-8xl font-normal tracking-tight">
            <span class="text-blue-500">S</span>
            <span class="text-red-500">k</span>
            <span class="text-yellow-500">e</span>
            <span class="text-blue-500">w</span>
            <span class="text-green-500">V</span>
            <span class="text-red-500">o</span>
            <span class="text-yellow-500">i</span>
            <span class="text-blue-500">r</span>
          </h1>
        </div>
        <p class="text-sm text-surface-600 dark:text-surface-400">
          Smart Knowledge Engine for Wafer Verification and Operations Intelligence Research
        </p>
      </div>

      <!-- Search section -->
      <div class="w-full max-w-2xl">
        <!-- Search bar -->
        <div class="relative mb-8">
          <div class="flex items-center bg-white dark:bg-surface-800 rounded-full shadow-lg border border-surface-200 dark:border-surface-700 hover:shadow-xl transition-shadow duration-200 px-4 py-3">
            <i class="pi pi-search text-surface-400 mr-3"></i>
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search for recipes, processes, or equipment..."
              class="flex-1 bg-transparent border-0 outline-0 text-base placeholder:text-surface-400"
              @keyup.enter="handleSearch"
            />
            <button
              v-if="searchQuery"
              @click="clearSearch"
              class="ml-2 p-1 hover:bg-surface-100 dark:hover:bg-surface-700 rounded-full transition-colors"
            >
              <i class="pi pi-times text-surface-400"></i>
            </button>
          </div>
        </div>

        <!-- Search buttons -->
        <div class="flex justify-center gap-4 mb-8">
          <Button
            label="SkewVoir Search"
            @click="handleSearch"
            class="px-6 py-2"
            severity="secondary"
            outlined
          />
          <Button
            label="I'm Feeling Lucky"
            @click="handleLuckySearch"
            class="px-6 py-2"
            severity="secondary"
            outlined
          />
        </div>

        <!-- Quick access links -->
        <div class="text-center">
          <div class="text-sm text-surface-600 dark:text-surface-400 mb-2">
            Quick access:
          </div>
          <div class="flex justify-center gap-6 text-sm">
            <router-link
              to="/equipment-status"
              class="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Equipment Status
            </router-link>
            <router-link
              to="/current-status"
              class="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Current Status
            </router-link>
            <router-link
              to="/storage"
              class="text-blue-600 dark:text-blue-400 hover:underline"
            >
              Storage
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Footer info -->
    <div class="text-center py-6">
      <div class="text-xs text-surface-500 dark:text-surface-500">
        Currently connected to <span class="font-medium">{{ selectedFab }}</span> Fab
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { storeToRefs } from 'pinia'
import { useFabStore } from '@/stores/fab'
import { useRouter } from 'vue-router'
import Button from 'primevue/button'

const router = useRouter()
const fabStore = useFabStore()
const { selectedFab } = storeToRefs(fabStore)

const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    console.log('Searching for:', searchQuery.value)
    // TODO: Implement search functionality
    // router.push({ name: 'SearchResults', query: { q: searchQuery.value } })
  }
}

const handleLuckySearch = () => {
  console.log('Feeling lucky search')
  // TODO: Implement "I'm feeling lucky" functionality
  // Could redirect to a random relevant page or the most popular search result
}

const clearSearch = () => {
  searchQuery.value = ''
}
</script>

<style scoped>
/* Page-specific styles if needed */
</style>
