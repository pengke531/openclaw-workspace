import api from './index'

/**
 * WeChat login
 */
export const login = (data) => {
  return api({
    url: '/api/user/login',
    method: 'POST',
    data
  })
}

/**
 * Get user profile
 */
export const getUserProfile = () => {
  return api({
    url: '/api/user/profile',
    method: 'GET'
  })
}

/**
 * Update user profile
 */
export const updateUserProfile = (data) => {
  return api({
    url: '/api/user/profile',
    method: 'PUT',
    data
  })
}

/**
 * Get user coupons
 */
export const getUserCoupons = (params) => {
  return api({
    url: '/api/user/coupons',
    method: 'GET',
    params
  })
}

/**
 * Get favorite routes
 */
export const getFavorites = () => {
  return api({
    url: '/api/user/favorites',
    method: 'GET'
  })
}

/**
 * Add to favorites
 */
export const addFavorite = (routeId) => {
  return api({
    url: '/api/user/favorites',
    method: 'POST',
    data: { routeId }
  })
}

/**
 * Remove from favorites
 */
export const removeFavorite = (routeId) => {
  return api({
    url: `/api/user/favorites/${routeId}`,
    method: 'DELETE'
  })
}
