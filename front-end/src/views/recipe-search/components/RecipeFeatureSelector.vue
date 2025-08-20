<template>
  <div class="recipe-feature-selector">
    <!-- Selection Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div
        v-for="(option, index) in recipeOptions"
        :key="index"
        class="shadow-sm rounded-2xl p-4 bg-surface-0 dark:bg-surface-900 border transition-all duration-200"
        :class="{
          'cursor-pointer': !option.disabled,
          'opacity-50 cursor-not-allowed': option.disabled,
          'border-primary shadow-md': selectedSearchType === index && !option.disabled,
          'border-transparent hover:border-primary hover:shadow-md': selectedSearchType !== index && !option.disabled
        }"
        @click="!option.disabled ? selectSearchType(index) : null"
      >
        <div class="flex items-center justify-center mb-4">
          <i :class="option.icon" class="text-4xl text-primary"></i>
        </div>
        <div class="p-2 flex flex-col items-center gap-3">
          <div class="flex flex-col gap-2 w-full">
            <div class="text-surface-900 dark:text-surface-0 text-lg font-semibold text-center">{{ option.title }}</div>
            <div class="text-surface-500 dark:text-surface-300 text-sm leading-normal text-center" v-html="option.description" />
          </div>
          <div class="flex gap-2">
            <span v-for="(tag, tagIndex) in option.tags" :key="tagIndex" class="bg-slate-100 dark:bg-slate-800 px-2 py-1 text-xs rounded-lg">
              {{ tag }}
            </span>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Confirm Button -->
    <div v-if="selectedSearchType !== null" class="flex justify-center mt-8">
      <Button 
        label="확인"
        icon="pi pi-check"
        @click="navigateToSelectedPage"
        size="large"
        class="px-8"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Button from 'primevue/button'

const props = defineProps({
  toolType: {
    type: String,
    required: true,
    validator: (value) => ['cd-sem', 'hv-sem', 'verity', 'provision'].includes(value)
  },
  recipeList: {
    type: Array,
    default: () => []
  },
  isLoading: {
    type: Boolean,
    default: false
  },
  error: {
    type: [Object, String],
    default: null
  }
})

const router = useRouter()
const route = useRoute()

// Search-related reactive data
const selectedSearchType = ref(null)

// Tool-specific recipe options configuration
const toolOptionsMap = {
  'cd-sem': [
    {
      title: 'Recipe 열기',
      description: 'Recipe 설정 상태를<br>확인할 수 있습니다',
      icon: 'pi pi-folder-open',
      tags: ['설정', '확인'],
      route: 'open'
    },
    {
      title: '횡전개 체크',
      description: 'Recipe의 횡전개 여부와<br>Version을 체크할 수 있습니다',
      icon: 'pi pi-check-circle',
      tags: ['버전', '체크'],
      route: 'horizontal-check'
    },
    {
      title: 'Meas. History',
      description: '측정 기록을<br>확인할 수 있습니다',
      icon: 'pi pi-chart-line',
      tags: ['측정', '기록'],
      route: 'measurement-history'
    }
  ],
  'hv-sem': [
    {
      title: 'Recipe 열기',
      description: 'Recipe 설정 상태를<br>확인할 수 있습니다',
      icon: 'pi pi-folder-open',
      tags: ['설정', '확인'],
      route: 'open'
    },
    {
      title: '횡전개 체크',
      description: 'Recipe의 횡전개 여부와<br>Version을 체크할 수 있습니다',
      icon: 'pi pi-check-circle',
      tags: ['버전', '체크'],
      route: 'horizontal-check'
    },
    {
      title: 'Meas. History',
      description: '측정 기록을<br>확인할 수 있습니다',
      icon: 'pi pi-chart-line',
      tags: ['측정', '기록'],
      route: 'measurement-history'
    }
  ],
  // Placeholder for future verity features
  'verity': [
    {
      title: 'Coming Soon',
      description: 'VeritySEM features<br>will be added here',
      icon: 'pi pi-clock',
      tags: ['개발중'],
      route: null,
      disabled: true
    }
  ],
  // Placeholder for future provision features
  'provision': [
    {
      title: 'Coming Soon',
      description: 'Provision features<br>will be added here',
      icon: 'pi pi-clock',
      tags: ['개발중'],
      route: null,
      disabled: true
    }
  ]
}

// Get recipe options based on current tool type
const recipeOptions = computed(() => {
  return toolOptionsMap[props.toolType] || []
})

// Search type selection
const selectSearchType = (index) => {
  const option = recipeOptions.value[index]
  if (option.disabled) return
  
  selectedSearchType.value = index
}

// Navigate to selected page
const navigateToSelectedPage = () => {
  if (selectedSearchType.value === null) return
  
  const option = recipeOptions.value[selectedSearchType.value]
  if (option && option.route && !option.disabled) {
    // Navigate to the feature view
    const facId = route.params.fac_id || 'R3'
    router.push(`/${facId}/recipe-search/${props.toolType}/${option.route}`)
  }
}
</script>

<style scoped>
/* Component-specific styles if needed */
</style>