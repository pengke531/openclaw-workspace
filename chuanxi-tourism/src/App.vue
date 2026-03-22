<template>
  <view class="app-container">
    <slot></slot>
  </view>
</template>

<script setup>
// App lifecycle
onLaunch(() => {
  console.log('App Launch')
  // Initialize app data
  initApp()
})

onShow(() => {
  console.log('App Show')
})

onHide(() => {
  console.log('App Hide')
})

// Initialize app
const initApp = () => {
  // Check login status
  const userStore = useUserStore()
  if (userStore.token) {
    userStore.checkAuth()
  }
}
</script>

<style lang="scss">
/* Global styles */
page {
  background-color: #F5F5F5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* Color variables */
:root {
  --primary: #2E7D32;
  --secondary: #FF8F00;
  --background: #F5F5F5;
  --surface: #FFFFFF;
  --text-primary: #212121;
  --text-secondary: #757575;
  --success: #4CAF50;
  --warning: #FF9800;
  --error: #F44336;
  --info: #2196F3;
}

/* Spacing */
$spacing-xs: 4px;
$spacing-sm: 8px;
$spacing-md: 16px;
$spacing-lg: 24px;
$spacing-xl: 32px;
</style>
