/**
 * Common utility functions
 */

/**
 * Format price
 */
export const formatPrice = (price) => {
  return `¥${Number(price).toFixed(2)}`
}

/**
 * Format date
 */
export const formatDate = (date, format = 'YYYY-MM-DD') => {
  if (!date) return ''
  const d = new Date(date)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  
  return format
    .replace('YYYY', year)
    .replace('MM', month)
    .replace('DD', day)
}

/**
 * Format relative time
 */
export const formatRelativeTime = (date) => {
  if (!date) return ''
  const now = Date.now()
  const timestamp = new Date(date).getTime()
  const diff = now - timestamp
  
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return '刚刚'
  if (minutes < 60) return `${minutes}分钟前`
  if (hours < 24) return `${hours}小时前`
  if (days < 7) return `${days}天前`
  
  return formatDate(date)
}

/**
 * Debounce function
 */
export const debounce = (fn, delay = 300) => {
  let timer = null
  return function (...args) {
    if (timer) clearTimeout(timer)
    timer = setTimeout(() => {
      fn.apply(this, args)
    }, delay)
  }
}

/**
 * Throttle function
 */
export const throttle = (fn, delay = 300) => {
  let last = 0
  return function (...args) {
    const now = Date.now()
    if (now - last >= delay) {
      last = now
      fn.apply(this, args)
    }
  }
}

/**
 * Validate phone number
 */
export const validatePhone = (phone) => {
  return /^1[3-9]\d{9}$/.test(phone)
}

/**
 * Validate ID card
 */
export const validateIdCard = (idCard) => {
  return /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/.test(idCard)
}

/**
 * Generate unique ID
 */
export const generateId = () => {
  return `${Date.now()}${Math.random().toString(36).substr(2, 9)}`
}

/**
 * Storage utilities
 */
export const storage = {
  get: (key, defaultValue = null) => {
    try {
      const value = uni.getStorageSync(key)
      return value || defaultValue
    } catch (e) {
      return defaultValue
    }
  },
  
  set: (key, value) => {
    try {
      uni.setStorageSync(key, value)
      return true
    } catch (e) {
      return false
    }
  },
  
  remove: (key) => {
    try {
      uni.removeStorageSync(key)
      return true
    } catch (e) {
      return false
    }
  },
  
  clear: () => {
    try {
      uni.clearStorageSync()
      return true
    } catch (e) {
      return false
    }
  }
}

/**
 * Show loading
 */
export const showLoading = (title = '加载中...') => {
  uni.showLoading({
    title,
    mask: true
  })
}

/**
 * Hide loading
 */
export const hideLoading = () => {
  uni.hideLoading()
}

/**
 * Show toast
 */
export const showToast = (title, icon = 'none') => {
  uni.showToast({
    title,
    icon
  })
}

/**
 * Show confirm dialog
 */
export const showConfirm = (title, content) => {
  return new Promise((resolve, reject) => {
    uni.showModal({
      title,
      content,
      success: (res) => {
        resolve(res.confirm)
      },
      fail: () => {
        reject(new Error('Modal closed'))
      }
    })
  })
}
