import { createSSRApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  const pinia = createPinia()
  
  app.use(pinia)
  
  // Global error handler
  app.config.errorHandler = (err, vm, info) => {
    console.error('Global error:', err)
    console.error('Error info:', info)
    // Report to error tracking service
  }
  
  return { app }
}
