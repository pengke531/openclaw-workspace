<template>
  <view class="home-page">
    <!-- Banner -->
    <view class="banner">
      <swiper indicator-dots autoplay circular>
        <swiper-item v-for="(banner, index) in banners" :key="index">
          <image :src="banner.image" mode="aspectFill" />
        </swiper-item>
      </swiper>
    </view>
    
    <!-- Search -->
    <view class="search-bar">
      <van-search
        v-model="keyword"
        placeholder="搜索路线/景点"
        @search="handleSearch"
      />
    </view>
    
    <!-- Attractions -->
    <view class="section">
      <view class="section-header">
        <text class="title">热门景点</text>
      </view>
      <view class="attractions-grid">
        <AttractionCard
          v-for="attraction in attractions"
          :key="attraction.id"
          :attraction="attraction"
          @click="goToAttraction"
        />
      </view>
    </view>
    
    <!-- Routes -->
    <view class="section">
      <view class="section-header">
        <text class="title">精选路线</text>
        <text class="more" @click="goToRoutes">更多 ></text>
      </view>
      <view class="routes-list">
        <RouteCard
          v-for="route in routes"
          :key="route.id"
          :route="route"
          @click="goToRouteDetail"
          @book="goToBooking"
        />
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useTourismStore } from '@/store/tourism'
import AttractionCard from '@/components/AttractionCard.vue'
import RouteCard from '@/components/RouteCard.vue'

const tourismStore = useTourismStore()

const keyword = ref('')
const banners = ref([
  { image: 'https://cdn.example.com/banner1.jpg' },
  { image: 'https://cdn.example.com/banner2.jpg' }
])

const attractions = ref([])
const routes = ref([])

onMounted(async () => {
  // Fetch data
  await Promise.all([
    tourismStore.fetchAttractions(),
    tourismStore.fetchRoutes()
  ])
  
  attractions.value = tourismStore.attractions
  routes.value = tourismStore.routes
})

const handleSearch = () => {
  console.log('Search:', keyword.value)
}

const goToAttraction = (attraction) => {
  uni.navigateTo({
    url: `/pages/attraction/detail?id=${attraction.id}`
  })
}

const goToRoutes = () => {
  uni.navigateTo({
    url: '/pages/routes/list'
  })
}

const goToRouteDetail = (route) => {
  uni.navigateTo({
    url: `/pages/routes/detail?id=${route.id}`
  })
}

const goToBooking = (route) => {
  uni.navigateTo({
    url: `/pages/booking/index?id=${route.id}`
  })
}
</script>

<style lang="scss" scoped>
.home-page {
  min-height: 100vh;
  background: #F5F5F5;
  padding-bottom: 50px;
}

.banner {
  swiper {
    height: 200px;
    
    image {
      width: 100%;
      height: 100%;
    }
  }
}

.search-bar {
  background: #FFFFFF;
  padding: 8px 16px;
}

.section {
  margin-top: 16px;
  padding: 0 16px;
  
  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    
    .title {
      font-size: 18px;
      font-weight: 600;
      color: #212121;
    }
    
    .more {
      font-size: 14px;
      color: #757575;
    }
  }
}

.attractions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.routes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
</style>
