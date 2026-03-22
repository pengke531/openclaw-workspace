<template>
  <view class="route-card" @click="handleClick">
    <view class="card-image">
      <image :src="route.coverImage" mode="aspectFill" />
    </view>
    <view class="card-content">
      <view class="title-row">
        <text class="name">{{ route.name }}</text>
      </view>
      <view class="itinerary-row">
        <text class="itinerary">{{ route.itinerary }}</text>
      </view>
      <view class="price-row">
        <text class="label">成人价:</text>
        <text class="price">¥{{ route.adultPrice }}/人</text>
        <van-button type="primary" size="small" round @click.stop="handleBook">预订</van-button>
      </view>
    </view>
  </view>
</template>

<script setup>
const props = defineProps({
  route: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click', 'book'])

const handleClick = () => {
  emit('click', props.route)
}

const handleBook = () => {
  emit('book', props.route)
}
</script>

<style lang="scss" scoped>
.route-card {
  background: #FFFFFF;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 16px;
  
  .card-image {
    height: 200px;
    
    image {
      width: 100%;
      height: 100%;
    }
  }
  
  .card-content {
    padding: 12px;
    
    .title-row {
      .name {
        font-size: 18px;
        font-weight: 600;
        color: #212121;
      }
    }
    
    .itinerary-row {
      margin-top: 4px;
      
      .itinerary {
        font-size: 14px;
        color: #757575;
      }
    }
    
    .price-row {
      margin-top: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      
      .label {
        font-size: 14px;
        color: #757575;
      }
      
      .price {
        font-size: 18px;
        font-weight: 600;
        color: #FF8F00;
        flex: 1;
      }
    }
  }
}
</style>
