import axios from 'axios'
import { useUserStore } from '@/store/user'

// Create axios instance
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'https://api.chuanxi-tourism.com',
  timeout: 10000,
  header: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  config => {
    const userStore = useUserStore()
    if (userStore.token) {
      config.headers.Authorization = `Bearer ${userStore.token}`
    }
    // Add common parameters
    config.params = {
      ...config.params,
      platform: 'mp-weixin',
      version: '1.0.0'
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  response => {
    const res = response.data
    
    // Success
    if (res.code === 200 || res.success) {
      return res
    }
    
    // Token expired
    if (res.code === 401) {
      const userStore = useUserStore()
      userStore.logout()
      // Redirect to login
      uni.showToast({
        title: '登录已过期，请重新登录',
        icon: 'none'
      })
      return Promise.reject(new Error(res.message || 'Unauthorized'))
    }
    
    // Other errors
    uni.showToast({
      title: res.message || '请求失败',
      icon: 'none'
    })
    return Promise.reject(new Error(res.message || 'Request failed'))
  },
  error => {
    console.error('Response error:', error)
    
    let message = '网络错误，请稍后重试'
    if (error.response) {
      switch (error.response.status) {
        case 400:
          message = '请求参数错误'
          break
        case 404:
          message = '请求资源不存在'
          break
        case 500:
          message = '服务器错误'
          break
        case 502:
          message = '网关错误'
          break
        case 503:
          message = '服务不可用'
          break
      }
    }
    
    uni.showToast({
      title: message,
      icon: 'none'
    })
    
    return Promise.reject(error)
  }
)

// Retry interceptor
api.interceptors.response.use(
  response => response,
  async error => {
    const config = error.config
    
    // Only retry once
    if (!config.__retryCount) {
      config.__retryCount = 1
      
      // Network error or timeout, retry
      if (!error.response || error.code === 'ECONNABORTED') {
        await new Promise(resolve => setTimeout(resolve, 1000))
        return api(config)
      }
    }
    
    return Promise.reject(error)
  }
)

export default api
