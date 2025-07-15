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
      path: '/skewvoir',
      name: 'skewvoir',
      component: () => import('../views/general/SkewVoirView.vue'),
      // No fab requirement for SkewVoir
    },
    // Routes with fac_id parameter
    {
      path: '/:fac_id',
      name: 'fab-main',
      component: MainView,
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/equipment-status',
      name: 'equipment-status',
      component: () => import('../views/equipment-status/EquipmentStatusView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/equipment-status/current-status',
      name: 'equipment-current-status',
      component: () => import('../views/equipment-status/CurrentStatusView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/equipment-status/storage',
      name: 'equipment-storage',
      component: () => import('../views/equipment-status/StorageView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/equipment-status/not_available',
      name: 'equipment-not-available',
      component: () => import('../views/equipment-status/NotAvailableView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/recipe-search',
      name: 'recipe-search',
      component: () => import('../views/recipe-search/RecipeSearchView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/recipe-search/open',
      name: 'recipe-open',
      component: () => import('../views/recipe-search/RecipeOpenView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/recipe-search/horizontal-check',
      name: 'recipe-horizontal-check',
      component: () => import('../views/recipe-search/RecipeHorizontalCheckView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/recipe-search/measurement-history',
      name: 'recipe-measurement-history',
      component: () => import('../views/recipe-search/RecipeMeasurementHistoryView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/device-statistics',
      name: 'device-statistics',
      component: () => import('../views/DeviceStatisticsView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/fail-issue',
      name: 'fail-issue',
      component: () => import('../views/FailIssueView.vue'),
      meta: { requiresFab: true }
    },
    {
      path: '/:fac_id/hardware-management',
      name: 'hardware-management',
      component: () => import('../views/HardwareManagementView.vue'),
      meta: { requiresFab: true }
    },
  ],
})

// Navigation guard to check fab selection
router.beforeEach((to, from, next) => {
  const fabStore = useFabStore()
  
  // Check if the route requires fab selection
  if (to.meta.requiresFab) {
    const fac_id = to.params.fac_id
    
    // If fac_id is provided in the URL
    if (fac_id) {
      // Get the fab list (handle reactivity)
      const fabList = fabStore.fabList.value || fabStore.fabList || ['R3', 'M16', 'M14', 'M15', 'M11', 'M10']
      
      // Case-insensitive comparison
      const upperFacId = fac_id.toUpperCase()
      const validFab = fabList.find(fab => fab.toUpperCase() === upperFacId)
      
      // Debug logging
      console.log('Navigation guard - fac_id:', fac_id)
      console.log('Navigation guard - upperFacId:', upperFacId)
      console.log('Navigation guard - fabList:', fabList)
      console.log('Navigation guard - validFab:', validFab)
      
      // Check if the fac_id is valid (case-insensitive)
      if (validFab) {
        // Auto-select the fab from URL (use the correct case from fabList)
        fabStore.setSelectedFab(validFab)
        next()
      } else {
        // Invalid fac_id, redirect to main page
        next({ 
          path: '/', 
          query: { invalidFab: fac_id }
        })
      }
    } else {
      // No fac_id in URL, redirect to main page
      next({ 
        path: '/', 
        query: { needsFab: 'true' }
      })
    }
  } else {
    next()
  }
})

export default router
