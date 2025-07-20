/**
 * Authentication utilities for frontend
 */

/**
 * Check if we're in development environment
 * @returns {boolean} True if in development mode
 */
export function isDevelopmentEnvironment() {
  // Check for explicit environment override
  const authMode = import.meta.env.VITE_AUTH_MODE;
  if (authMode === 'bypass') return true;
  if (authMode === 'enforce') return false;
  
  // Check if running in development mode
  if (import.meta.env.DEV) return true;
  
  // Check for localhost
  if (window.location.hostname === 'localhost' || 
      window.location.hostname === '127.0.0.1') {
    return true;
  }
  
  return false;
}

/**
 * Get a cookie value by name
 * @param {string} name - Cookie name
 * @returns {string|null} Cookie value or null if not found
 */
export function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

/**
 * Get LASTUSER from cookies
 * @returns {string|null} User ID or null if not found
 */
export function getLastUser() {
  return getCookie('LASTUSER');
}

/**
 * Check if user should be restricted based on their ID
 * @param {string} userId - User ID from LASTUSER cookie
 * @returns {boolean} True if user is restricted
 */
export function isRestrictedUser(userId) {
  if (!userId) return false;
  return userId.toLowerCase().startsWith('x');
}

/**
 * Check if current user has access to protected resources
 * @returns {object} Object with hasAccess boolean and userId string
 */
export function checkUserAccess() {
  // In development environment, bypass authentication
  if (isDevelopmentEnvironment()) {
    console.log('Development environment detected - bypassing frontend authentication');
    return {
      hasAccess: true,
      userId: 'dev_user'
    };
  }
  
  const userId = getLastUser();
  const hasAccess = !isRestrictedUser(userId);
  
  return {
    hasAccess,
    userId
  };
}

/**
 * Check if a route path is protected
 * @param {string} path - Route path
 * @returns {boolean} True if route is protected
 */
export function isProtectedRoute(path) {
  const protectedPaths = [
    '/equipment-status',
    '/device-statistics'
  ];
  
  return protectedPaths.some(protectedPath => 
    path.includes(protectedPath)
  );
}