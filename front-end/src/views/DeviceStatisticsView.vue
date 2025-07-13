<template>
  <div class="device-statistics bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">디바이스 통계</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">디바이스 상태 및 통계 정보를 확인하세요</div>
    </div>
    
    <!-- Selection Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-8">
      <div
        v-for="(option, index) in statisticsOptions"
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
      <!-- Current Status Content -->
      <div v-if="selected === 0" class="current-status-content">
        <h2 class="text-2xl font-semibold mb-6">현재 디바이스 상황</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-6 text-center">
            <i class="pi pi-check-circle text-4xl text-green-500 mb-3"></i>
            <div class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ currentStatus.active }}</div>
            <div class="text-surface-600 dark:text-surface-300">활성 디바이스</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-6 text-center">
            <i class="pi pi-pause-circle text-4xl text-yellow-500 mb-3"></i>
            <div class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ currentStatus.inactive }}</div>
            <div class="text-surface-600 dark:text-surface-300">비활성 디바이스</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-6 text-center">
            <i class="pi pi-exclamation-circle text-4xl text-red-500 mb-3"></i>
            <div class="text-2xl font-bold text-surface-900 dark:text-surface-0">{{ currentStatus.error }}</div>
            <div class="text-surface-600 dark:text-surface-300">오류 상태</div>
          </div>
        </div>
        
        <!-- Device List -->
        <div class="mt-6">
          <h3 class="text-lg font-semibold mb-4">디바이스 목록</h3>
          <DataTable :value="deviceList" stripedRows>
            <Column field="name" header="디바이스명"></Column>
            <Column field="type" header="타입"></Column>
            <Column field="status" header="상태">
              <template #body="{ data }">
                <Badge 
                  :value="data.status" 
                  :severity="getStatusSeverity(data.status)"
                />
              </template>
            </Column>
            <Column field="lastActive" header="마지막 활동"></Column>
            <Column field="temperature" header="온도">
              <template #body="{ data }">
                {{ data.temperature }}°C
              </template>
            </Column>
          </DataTable>
        </div>
      </div>

      <!-- Weekly Statistics Content -->
      <div v-if="selected === 1" class="weekly-stats-content">
        <h2 class="text-2xl font-semibold mb-6">주간 통계</h2>
        
        <!-- Summary Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-primary">{{ weeklyStats.totalDevices }}</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">전체 디바이스</div>
              </div>
            </template>
          </Card>
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-green-500">{{ weeklyStats.avgUptime }}%</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">평균 가동률</div>
              </div>
            </template>
          </Card>
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-yellow-500">{{ weeklyStats.totalWarnings }}</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">경고 발생</div>
              </div>
            </template>
          </Card>
          <Card>
            <template #content>
              <div class="flex flex-col items-center">
                <div class="text-3xl font-bold text-red-500">{{ weeklyStats.totalErrors }}</div>
                <div class="text-sm text-surface-600 dark:text-surface-300">오류 발생</div>
              </div>
            </template>
          </Card>
        </div>

        <!-- Chart Placeholder -->
        <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-8">
          <div class="text-center">
            <i class="pi pi-chart-line text-6xl text-surface-400 mb-4"></i>
            <p class="text-surface-600 dark:text-surface-300">주간 추이 차트가 여기에 표시됩니다</p>
            <p class="text-sm text-surface-500 dark:text-surface-400 mt-2">Chart.js 또는 PrimeVue Chart 컴포넌트로 구현 예정</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Badge from 'primevue/badge'
import Card from 'primevue/card'

const selected = ref(0)

const statisticsOptions = [
  {
    title: '현재 상황',
    description: '실시간 디바이스<br>상태 확인',
    icon: 'pi pi-chart-line',
    tags: ['실시간', '모니터링']
  },
  {
    title: '주간 통계',
    description: '최근 7일간<br>통계 분석',
    icon: 'pi pi-calendar',
    tags: ['추이', '분석']
  }
]

// Current status data
const currentStatus = ref({
  active: 15,
  inactive: 3,
  error: 2
})

// Device list for current status
const deviceList = ref([
  {
    name: 'Device-A01',
    type: 'Sensor',
    status: '활성',
    lastActive: '2분 전',
    temperature: 25
  },
  {
    name: 'Device-B02',
    type: 'Controller',
    status: '활성',
    lastActive: '5분 전',
    temperature: 28
  },
  {
    name: 'Device-C03',
    type: 'Sensor',
    status: '비활성',
    lastActive: '1시간 전',
    temperature: 22
  },
  {
    name: 'Device-D04',
    type: 'Monitor',
    status: '오류',
    lastActive: '30분 전',
    temperature: 35
  }
])

// Weekly statistics data
const weeklyStats = ref({
  totalDevices: 20,
  avgUptime: 94.5,
  totalWarnings: 12,
  totalErrors: 3
})

// Get badge severity based on status
const getStatusSeverity = (status) => {
  switch (status) {
    case '활성':
      return 'success'
    case '비활성':
      return 'warning'
    case '오류':
      return 'danger'
    default:
      return 'secondary'
  }
}

// Fetch current status
const fetchCurrentStatus = async () => {
  // TODO: Implement API call to get current device status
  // const response = await fetch('/api/devices/status')
  // currentStatus.value = await response.json()
}

// Fetch weekly statistics
const fetchWeeklyStats = async () => {
  // TODO: Implement API call to get weekly statistics
  // const response = await fetch('/api/devices/weekly-stats')
  // weeklyStats.value = await response.json()
}

onMounted(() => {
  fetchCurrentStatus()
  fetchWeeklyStats()
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>