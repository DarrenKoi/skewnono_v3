<template>
  <div class="hardware-management bg-surface-50 dark:bg-surface-950 px-12 py-20 md:px-20 xl:px-[20rem]">
    <div class="flex flex-col items-start gap-2 mb-8">
      <div class="text-surface-900 dark:text-surface-0 font-semibold text-3xl">H/W 관리</div>
      <div class="text-surface-500 dark:text-surface-300 text-lg">하드웨어 모니터링 및 관리 시스템</div>
    </div>
    
    <!-- Selection Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
      <div
        v-for="(option, index) in hardwareOptions"
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
      <!-- X-bar Chart Content -->
      <div v-if="selected === 0" class="xbar-chart-content">
        <h2 class="text-2xl font-semibold mb-6">X-bar Chart - Daily Monitoring</h2>
        
        <!-- Control Chart Summary -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-chart-line text-3xl text-blue-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ xbarStats.mean }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">평균값</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-arrow-up text-3xl text-green-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ xbarStats.ucl }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">상한선 (UCL)</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-arrow-down text-3xl text-red-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ xbarStats.lcl }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">하한선 (LCL)</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-exclamation-triangle text-3xl text-yellow-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ xbarStats.outOfControl }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">관리이탈</div>
          </div>
        </div>

        <!-- Chart Placeholder -->
        <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-8 mb-6">
          <div class="text-center">
            <i class="pi pi-chart-line text-6xl text-surface-400 mb-4"></i>
            <p class="text-surface-600 dark:text-surface-300">X-bar 관리도 차트가 여기에 표시됩니다</p>
            <p class="text-sm text-surface-500 dark:text-surface-400 mt-2">실시간 품질 관리 모니터링</p>
          </div>
        </div>

        <!-- Recent Data Table -->
        <div class="mt-6">
          <h3 class="text-lg font-semibold mb-4">최근 측정 데이터</h3>
          <DataTable :value="xbarDataList" stripedRows>
            <Column field="timestamp" header="시간"></Column>
            <Column field="sample" header="샘플"></Column>
            <Column field="value" header="측정값"></Column>
            <Column field="status" header="상태">
              <template #body="{ data }">
                <Badge 
                  :value="data.status" 
                  :severity="getControlStatus(data.status)"
                />
              </template>
            </Column>
          </DataTable>
        </div>
      </div>

      <!-- Beam Condition Content -->
      <div v-if="selected === 1" class="beam-condition-content">
        <h2 class="text-2xl font-semibold mb-6">Beam Condition - Shape & Resolution</h2>
        
        <!-- Beam Parameters -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-circle text-3xl text-blue-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ beamCondition.shape }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Beam Shape</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-eye text-3xl text-green-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ beamCondition.resolution }}nm</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Resolution</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-bolt text-3xl text-yellow-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ beamCondition.intensity }}%</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">Intensity</div>
          </div>
        </div>

        <!-- Beam Status Table -->
        <div class="mt-6">
          <h3 class="text-lg font-semibold mb-4">Beam 상태 모니터링</h3>
          <DataTable :value="beamStatusList" stripedRows>
            <Column field="parameter" header="파라미터"></Column>
            <Column field="current" header="현재값"></Column>
            <Column field="target" header="목표값"></Column>
            <Column field="tolerance" header="공차"></Column>
            <Column field="status" header="상태">
              <template #body="{ data }">
                <Badge 
                  :value="data.status" 
                  :severity="getBeamStatus(data.status)"
                />
              </template>
            </Column>
          </DataTable>
        </div>
      </div>

      <!-- FDC Content -->
      <div v-if="selected === 2" class="fdc-content">
        <h2 class="text-2xl font-semibold mb-6">FDC - Fault Detection & Classification</h2>
        
        <!-- FDC Summary -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-shield text-3xl text-green-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ fdcStats.normal }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">정상</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-exclamation-triangle text-3xl text-yellow-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ fdcStats.warning }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">경고</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-times-circle text-3xl text-red-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ fdcStats.fault }}</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">고장</div>
          </div>
          <div class="bg-surface-50 dark:bg-surface-800 rounded-lg p-4 text-center">
            <i class="pi pi-percentage text-3xl text-blue-500 mb-2"></i>
            <div class="text-xl font-bold text-surface-900 dark:text-surface-0">{{ fdcStats.accuracy }}%</div>
            <div class="text-sm text-surface-600 dark:text-surface-300">정확도</div>
          </div>
        </div>

        <!-- FDC Events Table -->
        <div class="mt-6">
          <h3 class="text-lg font-semibold mb-4">FDC 이벤트 로그</h3>
          <DataTable :value="fdcEventList" stripedRows>
            <Column field="timestamp" header="시간"></Column>
            <Column field="component" header="컴포넌트"></Column>
            <Column field="faultType" header="고장 유형"></Column>
            <Column field="severity" header="심각도">
              <template #body="{ data }">
                <Badge 
                  :value="data.severity" 
                  :severity="getFdcSeverity(data.severity)"
                />
              </template>
            </Column>
            <Column field="description" header="설명"></Column>
            <Column header="액션">
              <template #body>
                <div class="flex gap-2">
                  <Button icon="pi pi-eye" size="small" text severity="info" />
                  <Button icon="pi pi-cog" size="small" text severity="warning" />
                </div>
              </template>
            </Column>
          </DataTable>
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
import Button from 'primevue/button'

const selected = ref(0)

const hardwareOptions = [
  {
    title: 'X-bar Chart',
    description: 'Daily Monitoring<br>품질 관리도 분석',
    icon: 'pi pi-chart-line',
    tags: ['관리도', '품질']
  },
  {
    title: 'Beam Condition',
    description: 'Beam Shape &<br>Resolution 모니터링',
    icon: 'pi pi-eye',
    tags: ['빔', '해상도']
  },
  {
    title: 'FDC',
    description: 'Fault Detection &<br>Classification',
    icon: 'pi pi-shield',
    tags: ['고장진단', '분류']
  }
]

// X-bar Chart Statistics
const xbarStats = ref({
  mean: 125.4,
  ucl: 135.2,
  lcl: 115.6,
  outOfControl: 3
})

// X-bar Data List
const xbarDataList = ref([
  {
    timestamp: '2024-01-15 15:30:00',
    sample: 'S-001',
    value: 127.8,
    status: '정상'
  },
  {
    timestamp: '2024-01-15 15:25:00',
    sample: 'S-002',
    value: 138.2,
    status: '이탈'
  },
  {
    timestamp: '2024-01-15 15:20:00',
    sample: 'S-003',
    value: 123.5,
    status: '정상'
  }
])

// Beam Condition Data
const beamCondition = ref({
  shape: 'Circular',
  resolution: 2.5,
  intensity: 95
})

// Beam Status List
const beamStatusList = ref([
  {
    parameter: 'Beam Size',
    current: '2.5nm',
    target: '2.0nm',
    tolerance: '±0.5nm',
    status: '정상'
  },
  {
    parameter: 'Focus',
    current: '98%',
    target: '100%',
    tolerance: '±2%',
    status: '정상'
  },
  {
    parameter: 'Stability',
    current: '0.8%',
    target: '<1%',
    tolerance: '1%',
    status: '정상'
  }
])

// FDC Statistics
const fdcStats = ref({
  normal: 156,
  warning: 12,
  fault: 3,
  accuracy: 97.8
})

// FDC Event List
const fdcEventList = ref([
  {
    timestamp: '2024-01-15 14:45:00',
    component: 'Electron Gun',
    faultType: 'Voltage Drift',
    severity: 'Warning',
    description: 'Voltage deviation detected'
  },
  {
    timestamp: '2024-01-15 14:30:00',
    component: 'Lens System',
    faultType: 'Alignment',
    severity: 'Normal',
    description: 'Auto-correction applied'
  },
  {
    timestamp: '2024-01-15 14:15:00',
    component: 'Detector',
    faultType: 'Calibration',
    severity: 'Fault',
    description: 'Calibration out of range'
  }
])

// Status severity functions
const getControlStatus = (status) => {
  switch (status) {
    case '정상':
      return 'success'
    case '이탈':
      return 'danger'
    default:
      return 'secondary'
  }
}

const getBeamStatus = (status) => {
  switch (status) {
    case '정상':
      return 'success'
    case '경고':
      return 'warning'
    case '이상':
      return 'danger'
    default:
      return 'secondary'
  }
}

const getFdcSeverity = (severity) => {
  switch (severity) {
    case 'Normal':
      return 'success'
    case 'Warning':
      return 'warning'
    case 'Fault':
      return 'danger'
    default:
      return 'secondary'
  }
}

// Fetch data functions
const fetchXbarData = async () => {
  // TODO: Implement API call
}

const fetchBeamCondition = async () => {
  // TODO: Implement API call
}

const fetchFdcData = async () => {
  // TODO: Implement API call
}

onMounted(() => {
  fetchXbarData()
  fetchBeamCondition()
  fetchFdcData()
})
</script>

<style scoped>
/* Page-specific styles if needed */
</style>