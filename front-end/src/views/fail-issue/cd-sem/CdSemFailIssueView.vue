<template>
  <div class="fail-issue bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <!-- Back Button -->
    <Button 
        label="장비 선택으로 돌아가기" 
        icon="pi pi-arrow-left" 
        @click="goBackToToolSelection" 
        size="large" 
        outlined 
      class="mb-2"
    />
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">Fail Issue</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">장비 및 프로세스 관련 이슈를 확인하고 관리하세요</div>
    </div>
    
    <!-- Selection Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div
        v-for="(option, index) in failIssueOptions"
        :key="index"
        class="shadow-sm rounded-2xl p-4 cursor-pointer bg-surface-0 dark:bg-surface-900 border transition-all duration-200"
        :class="{
          'border-transparent': selected !== index,
          'border-primary shadow-md': selected === index
        }"
        @click="selected = index"
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

    <!-- Content Display -->
    <div class="bg-surface-0 dark:bg-surface-900 rounded-xl p-6 shadow-sm border">
      <!-- Align Fail Content -->
      <div v-if="selected === 0" class="align-fail-content">
        <h2 class="text-2xl font-semibold mb-6">Align Fail Issues</h2>
        
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-exclamation-triangle text-3xl text-red-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ alignFailStats.critical }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Critical</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-exclamation-circle text-3xl text-yellow-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ alignFailStats.warning }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Warning</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-info-circle text-3xl text-blue-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ alignFailStats.info }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Info</div>
          </div>
        </div>

        <!-- Align Fail Table -->
        <DataTable :value="alignFailList" stripedRows>
          <Column field="device" header="Device"></Column>
          <Column field="type" header="Type"></Column>
          <Column field="severity" header="Severity">
            <template #body="{ data }">
              <Badge 
                :value="data.severity" 
                :severity="getSeverityType(data.severity)"
              />
            </template>
          </Column>
          <Column field="description" header="Description"></Column>
          <Column field="timestamp" header="Timestamp"></Column>
          <Column header="Actions">
            <template #body>
              <div class="flex gap-2">
                <Button icon="pi pi-eye" size="small" text severity="info" />
                <Button icon="pi pi-wrench" size="small" text severity="success" />
              </div>
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- Meas Fail Content -->
      <div v-if="selected === 1" class="meas-fail-content">
        <h2 class="text-2xl font-semibold mb-6">Meas Fail Issues</h2>
        
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-times-circle text-3xl text-red-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ measFailStats.failed }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Failed</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-clock text-3xl text-yellow-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ measFailStats.timeout }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Timeout</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-chart-line text-3xl text-blue-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ measFailStats.outOfRange }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Out of Range</div>
          </div>
        </div>

        <!-- Meas Fail Table -->
        <DataTable :value="measFailList" stripedRows>
          <Column field="recipe" header="Recipe"></Column>
          <Column field="parameter" header="Parameter"></Column>
          <Column field="expected" header="Expected"></Column>
          <Column field="actual" header="Actual"></Column>
          <Column field="deviation" header="Deviation"></Column>
          <Column field="timestamp" header="Timestamp"></Column>
          <Column header="Actions">
            <template #body>
              <div class="flex gap-2">
                <Button icon="pi pi-eye" size="small" text severity="info" />
                <Button icon="pi pi-refresh" size="small" text severity="warning" />
              </div>
            </template>
          </Column>
        </DataTable>
      </div>

      <!-- Weekly Statistics Content -->
      <div v-if="selected === 2" class="weekly-stats-content">
        <h2 class="text-2xl font-semibold mb-6">주간 통계</h2>
        
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-red-500">{{ weeklyStats.totalFails }}</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">총 실패 건수</div>
              </div>
            </template>
          </Card>
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-yellow-500">{{ weeklyStats.alignFails }}</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">Align 실패</div>
              </div>
            </template>
          </Card>
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-blue-500">{{ weeklyStats.measFails }}</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">Meas 실패</div>
              </div>
            </template>
          </Card>
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-green-500">{{ weeklyStats.resolved }}</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">해결됨</div>
              </div>
            </template>
          </Card>
        </div>

        <!-- Chart Placeholder -->
        <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-8">
          <div class="text-center">
            <i class="pi pi-chart-bar text-6xl text-surface-400 mb-4"></i>
            <p class="text-surface-600 dark:text-surface-300">주간 실패 이슈 추이 차트가 여기에 표시됩니다</p>
            <p class="text-sm text-surface-500 dark:text-surface-400 mt-2">실패 유형별 트렌드 분석</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Badge from 'primevue/badge'
import Card from 'primevue/card'
import Button from 'primevue/button'

const router = useRouter()
const route = useRoute()

const selected = ref(0)

const failIssueOptions = [
  {
    title: 'Align Fail',
    description: '정렬 실패 이슈<br>모니터링 및 관리',
    icon: 'pi pi-align-center',
    tags: ['정렬', '실패']
  },
  {
    title: 'Meas Fail',
    description: '측정 실패 이슈<br>분석 및 대응',
    icon: 'pi pi-chart-line',
    tags: ['측정', '실패']
  },
  {
    title: '주간 통계',
    description: '실패 이슈<br>주간 통계 분석',
    icon: 'pi pi-calendar',
    tags: ['통계', '분석']
  }
]

// Align Fail Statistics
const alignFailStats = ref({
  critical: 5,
  warning: 12,
  info: 3
})

// Align Fail List
const alignFailList = ref([
  {
    device: 'Device-A01',
    type: 'Position',
    severity: 'Critical',
    description: 'X-axis alignment out of tolerance',
    timestamp: '2024-01-15 14:30:25'
  },
  {
    device: 'Device-B02',
    type: 'Rotation',
    severity: 'Warning',
    description: 'Z-axis rotation deviation detected',
    timestamp: '2024-01-15 14:25:10'
  },
  {
    device: 'Device-C03',
    type: 'Calibration',
    severity: 'Info',
    description: 'Calibration drift within acceptable range',
    timestamp: '2024-01-15 14:20:45'
  }
])

// Meas Fail Statistics
const measFailStats = ref({
  failed: 8,
  timeout: 4,
  outOfRange: 6
})

// Meas Fail List
const measFailList = ref([
  {
    recipe: 'RECIPE_001',
    parameter: 'Voltage',
    expected: '3.3V',
    actual: '2.9V',
    deviation: '-12.1%',
    timestamp: '2024-01-15 15:45:30'
  },
  {
    recipe: 'RECIPE_002',
    parameter: 'Current',
    expected: '100mA',
    actual: '125mA',
    deviation: '+25.0%',
    timestamp: '2024-01-15 15:40:15'
  },
  {
    recipe: 'RECIPE_003',
    parameter: 'Temperature',
    expected: '25°C',
    actual: '28°C',
    deviation: '+12.0%',
    timestamp: '2024-01-15 15:35:20'
  }
])

// Weekly Statistics
const weeklyStats = ref({
  totalFails: 42,
  alignFails: 20,
  measFails: 18,
  resolved: 38
})

// Go back to tool selection
const goBackToToolSelection = () => {
  const facId = route.params.fac_id || 'R3'
  router.push(`/${facId}/fail-issue`)
}

// Get severity type for badge
const getSeverityType = (severity) => {
  switch (severity) {
    case 'Critical':
      return 'danger'
    case 'Warning':
      return 'warning'
    case 'Info':
      return 'info'
    default:
      return 'secondary'
  }
}

// Fetch data functions
const fetchAlignFailData = async () => {
  // TODO: Implement API call
}

const fetchMeasFailData = async () => {
  // TODO: Implement API call
}

const fetchWeeklyStats = async () => {
  // TODO: Implement API call
}

onMounted(() => {
  fetchAlignFailData()
  fetchMeasFailData()
  fetchWeeklyStats()
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>