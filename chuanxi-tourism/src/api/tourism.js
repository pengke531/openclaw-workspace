import api from './index'

// Tourism API endpoints

/**
 * Get tourism routes list
 */
export const getRoutes = (params) => {
  return api({
    url: '/api/tourism/routes',
    method: 'GET',
    params: {
      page: 1,
      pageSize: 20,
      ...params
    }
  })
}

/**
 * Get route detail
 */
export const getRouteDetail = (id) => {
  return api({
    url: `/api/tourism/routes/${id}`,
    method: 'GET'
  })
}

/**
 * Get attractions list
 */
export const getAttractions = (params) => {
  return api({
    url: '/api/tourism/attractions',
    method: 'GET',
    params: {
      page: 1,
      pageSize: 50,
      ...params
    }
  })
}

/**
 * Get attraction detail
 */
export const getAttractionDetail = (id) => {
  return api({
    url: `/api/tourism/attractions/${id}`,
    method: 'GET'
  })
}

/**
 * Create booking order
 */
export const createOrder = (data) => {
  return api({
    url: '/api/tourism/orders',
    method: 'POST',
    data
  })
}

/**
 * Get order list
 */
export const getOrders = (params) => {
  return api({
    url: '/api/tourism/orders',
    method: 'GET',
    params: {
      page: 1,
      pageSize: 20,
      ...params
    }
  })
}

/**
 * Get order detail
 */
export const getOrderDetail = (id) => {
  return api({
    url: `/api/tourism/orders/${id}`,
    method: 'GET'
  })
}

/**
 * Cancel order
 */
export const cancelOrder = (id, reason) => {
  return api({
    url: `/api/tourism/orders/${id}/cancel`,
    method: 'POST',
    data: { reason }
  })
}

/**
 * Get available dates for booking
 */
export const getAvailableDates = (routeId, month) => {
  return api({
    url: `/api/tourism/routes/${routeId}/availability`,
    method: 'GET',
    params: { month }
  })
}
