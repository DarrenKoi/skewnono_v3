import { createRouter, createWebHistory } from 'vue-router'
import MainView from '../views/general/MainView.vue'
import { useFabStore } from '@/stores/fab'
import { checkUserAccess, isProtectedRoute } from '@/utils/auth'

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
    // Routes with fac_id parameter
    {
      path: '/:fac_id',
      name: 'fab-main',
      component: MainView,
      meta: { requiresFab: true },
    },
    // SkewVoir routes
    {
      path: '/:fac_id/skewvoir',
      name: 'skewvoir',
      component: () => import('../views/SkewVoir/SkewVoirView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/skewvoir/cd-sem',
      name: 'skewvoir-cd-sem',
      component: () => import('../views/SkewVoir/cd-sem/CdSemSkewVoirView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/skewvoir/hv-sem',
      name: 'skewvoir-hv-sem',
      component: () => import('../views/SkewVoir/hv-sem/HvSemSkewVoirView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/skewvoir/verity',
      name: 'skewvoir-verity',
      component: () => import('../views/SkewVoir/verity/VeritySkewVoirView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/skewvoir/provision',
      name: 'skewvoir-provision',
      component: () => import('../views/SkewVoir/provision/ProvisionSkewVoirView.vue'),
      meta: { requiresFab: true },
    },
    // Equipment Status routes
    {
      path: '/:fac_id/equipment-status',
      name: 'equipment-status',
      component: () => import('../views/equipment-status/EquipmentStatusView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/equipment-status/current-status',
      name: 'equipment-current-status',
      component: () => import('../views/equipment-status/CurrentStatusView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/equipment-status/storage',
      name: 'equipment-storage',
      component: () => import('../views/equipment-status/StorageView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/equipment-status/not_available',
      name: 'equipment-not-available',
      component: () => import('../views/equipment-status/NotAvailableView.vue'),
      meta: { requiresFab: true },
    },
    // Recipe Search routes
    {
      path: '/:fac_id/recipe-search',
      name: 'recipe-search',
      component: () => import('../views/recipe-search/RecipeSearchView.vue'),
      meta: { requiresFab: true },
    },
    // Tool-specific search views removed - now handled by main RecipeSearchView
    // The main view now includes both tool selection and feature selection
    {
      path: '/:fac_id/recipe-search/cd-sem/open',
      name: 'recipe-open',
      component: () => import('../views/recipe-search/cd-sem/RecipeOpenView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/recipe-search/cd-sem/horizontal-check',
      name: 'recipe-horizontal-check',
      component: () => import('../views/recipe-search/cd-sem/RecipeHorizontalCheckView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/recipe-search/cd-sem/measurement-history',
      name: 'recipe-measurement-history',
      component: () => import('../views/recipe-search/cd-sem/RecipeMeasurementHistoryView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/recipe-search/hv-sem/open',
      name: 'hv-sem-recipe-open',
      component: () => import('../views/recipe-search/hv-sem/HvSemRecipeOpenView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/recipe-search/hv-sem/horizontal-check',
      name: 'hv-sem-recipe-horizontal-check',
      component: () => import('../views/recipe-search/hv-sem/HvSemRecipeHorizontalCheckView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/recipe-search/hv-sem/measurement-history',
      name: 'hv-sem-recipe-measurement-history',
      component: () => import('../views/recipe-search/hv-sem/HvSemRecipeMeasurementHistoryView.vue'),
      meta: { requiresFab: true },
    },
    // Device Statistics routes - redirect to cd-sem since it's the only active tool
    {
      path: '/:fac_id/device-statistics',
      redirect: to => `${to.path}/cd-sem`,
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/device-statistics/cd-sem',
      name: 'device-statistics-cd-sem',
      component: () => import('../views/device-statistics/cd-sem/CdSemDeviceStatisticsView.vue'),
      meta: { requiresFab: true },
    },
    // Note: Only cd-sem is currently functional. Other tool categories removed to simplify flow.
    {
      path: '/R3/device-statistics/cd-sem/current-status',
      name: 'device-statistics-current-status-r3',
      component: () => import('../views/device-statistics/cd-sem/facR3/CurrentStatusView.vue'),
    },
    {
      path: '/R3/device-statistics/cd-sem/weekly-trend',
      name: 'device-statistics-weekly-trend-r3',
      component: () => import('../views/device-statistics/cd-sem/facR3/WeeklyTrendView.vue'),
    },
    // Other facilities device statistics routes
    {
      path: '/:fac_id/device-statistics/cd-sem/current-status',
      name: 'device-statistics-current-status',
      component: () => import('../views/device-statistics/cd-sem/facOthers/CurrentStatusView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/device-statistics/cd-sem/weekly-trend',
      name: 'device-statistics-weekly-trend',
      component: () => import('../views/device-statistics/cd-sem/facOthers/WeeklyTrendView.vue'),
      meta: { requiresFab: true },
    },
    // Fail Issue routes
    {
      path: '/:fac_id/fail-issue',
      name: 'fail-issue',
      component: () => import('../views/fail-issue/FailIssueView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/fail-issue/cd-sem',
      name: 'fail-issue-cd-sem',
      component: () => import('../views/fail-issue/cd-sem/CdSemFailIssueView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/fail-issue/hv-sem',
      name: 'fail-issue-hv-sem',
      component: () => import('../views/fail-issue/hv-sem/HvSemFailIssueView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/fail-issue/verity',
      name: 'fail-issue-verity',
      component: () => import('../views/fail-issue/verity/VerityFailIssueView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/fail-issue/provision',
      name: 'fail-issue-provision',
      component: () => import('../views/fail-issue/provision/ProvisionFailIssueView.vue'),
      meta: { requiresFab: true },
    },
    // Hardware Management routes
    {
      path: '/:fac_id/hardware-management',
      name: 'hardware-management',
      component: () => import('../views/hardware-management/HardwareManagementView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/hardware-management/cd-sem',
      name: 'hardware-management-cd-sem',
      component: () => import('../views/hardware-management/cd-sem/CdSemHardwareManagementView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/hardware-management/hv-sem',
      name: 'hardware-management-hv-sem',
      component: () => import('../views/hardware-management/hv-sem/HvSemHardwareManagementView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/hardware-management/verity',
      name: 'hardware-management-verity',
      component: () => import('../views/hardware-management/verity/VerityHardwareManagementView.vue'),
      meta: { requiresFab: true },
    },
    {
      path: '/:fac_id/hardware-management/provision',
      name: 'hardware-management-provision',
      component: () => import('../views/hardware-management/provision/ProvisionHardwareManagementView.vue'),
      meta: { requiresFab: true },
    },
  ],
})

// Navigation guard to check fab selection and user access
router.beforeEach(async (to, from, next) => {
  const fabStore = useFabStore()

  // Check user access for protected routes
  if (isProtectedRoute(to.path)) {
    const { hasAccess, userId } = checkUserAccess()
    
    if (!hasAccess) {
      console.warn(`Access denied for user ${userId} to protected route: ${to.path}`)
      next({
        path: '/',
        query: { 
          accessDenied: 'true',
          reason: 'insufficient_permissions'
        }
      })
      return
    }
  }

  // Check if the route requires fab selection
  if (to.meta.requiresFab) {
    const fac_id = to.params.fac_id

    // If fac_id is provided in the URL
    if (fac_id) {
      // Wait for fab list to be loaded if it's still loading
      let attempts = 0
      const maxAttempts = 50 // 5 seconds total (50 * 100ms)

      while (fabStore.fabListLoading && attempts < maxAttempts) {
        await new Promise((resolve) => setTimeout(resolve, 100))
        attempts++
      }

      // Get the fab list (handle reactivity)
      // fabStore.fabList is already a computed ref that returns the value
      const fabList = fabStore.fabList || ['R3', 'M16', 'M14', 'M15', 'M11', 'M10']

      // Case-insensitive comparison
      const upperFacId = fac_id.toUpperCase()
      const validFab = fabList.find((fab) => fab.toUpperCase() === upperFacId)

      // Debug logging
      console.log('Navigation guard - fabList:', fabList)
      console.log('Navigation guard - validFab:', validFab)
      console.log('Navigation guard - loading status:', fabStore.fabListLoading)

      // Check if the fac_id is valid (case-insensitive)
      if (validFab) {
        // Auto-select the fab from URL (use the correct case from fabList)
        fabStore.setSelectedFab(validFab)
        next()
      } else {
        // Invalid fac_id, redirect to main page
        next({
          path: '/',
          query: { invalidFab: fac_id },
        })
      }
    } else {
      // No fac_id in URL, redirect to main page
      next({
        path: '/',
        query: { needsFab: 'true' },
      })
    }
  } else {
    next()
  }
})

export default router