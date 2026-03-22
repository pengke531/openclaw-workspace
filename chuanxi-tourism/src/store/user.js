import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getUserProfile, login } from '@/api/user'

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref(uni.getStorageSync('token') || '')
  const userInfo = ref(null)
  const isLoggedIn = computed(() => !!token.value)
  
  // Actions
  const setToken = (newToken) => {
    token.value = newToken
    uni.setStorageSync('token', newToken)
  }
  
  const setUserInfo = (info) => {
    userInfo.value = info
  }
  
  const loginAction = async (code) => {
    try {
      const res = await login({ code })
      setToken(res.data.token)
      setUserInfo(res.data.userInfo)
      return res
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }
  
  const checkAuth = async () => {
    try {
      const res = await getUserProfile()
      setUserInfo(res.data)
    } catch (error) {
      // Token expired, clear auth
      logout()
    }
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync('token')
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    setToken,
    setUserInfo,
    loginAction,
    checkAuth,
    logout
  }
})
