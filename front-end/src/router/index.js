import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/general/MainView.vue'
import { useFabStore } from '@/stores/fab'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/general/AboutView.vue'),
    },
    {
      path: '/equipment-status',
      name: 'equipment-status',
      component: () => import('../views/equipment-status/EquipmentStatusView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/equipment-status/current-status',
      name: 'equipment-current-status',
      component: () => import('../views/equipment-status/CurrentStatusView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/equipment-status/storage',
      name: 'equipment-storage',
      component: () => import('../views/equipment-status/StorageView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/equipment-status/not_available',
      name: 'equipment-not-available',
      component: () => import('../views/equipment-status/NotAvailableView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/recipe-search',
      name: 'recipe-search',
      component: () => import('../views/RecipeSearchView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/device-statistics',
      name: 'device-statistics',
      component: () => import('../views/DeviceStatisticsView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/fail-issue',
      name: 'fail-issue',
      component: () => import('../views/FailIssueView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/hardware-management',
      name: 'hardware-management',
      component: () => import('../views/HardwareManagementView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/skewvoir',
      name: 'skewvoir',
      component: () => import('../views/general/SkewVoirView.vue'),
      // No fab requirement for SkewVoir
    },
  ],
})

// Navigation guard to check fab selection
router.beforeEach((to, from, next) => {
  const fabStore = useFabStore()
  
  // Check if the route requires fab selection
  if (to.meta.requiresFab && !fabStore.selectedFab) {
    // Redirect to main page with a query parameter to show message
    next({ 
      path: '/', 
      query: { needsFab: 'true' }
    })
  } else {
    next()
  }
})

export default router
