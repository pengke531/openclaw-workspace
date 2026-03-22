<template>
  <view class="attraction-card" @click="handleClick">
    <view class="card-image">
      <image :src="attraction.coverImage" mode="aspectFill" />
      <view class="rating" v-if="attraction.rating">
        <text class="star">★</text>
        <text>{{ attraction.rating }}</text>
      </view>
    </view>
    <view class="card-content">
      <view class="title-row">
        <text class="name">{{ attraction.name }}</text>
      </view>
      <view class="location-row">
        <text class="location">{{ attraction.location }}</text>
      </view>
      <view class="price-row" v-if="attraction.ticketPrice">
        <text class="label">门票:</text>
        <text class="price">¥{{ attraction.ticketPrice }}起</text>
      </view>
    </view>
  </view>
</template>

<script setup>
const props = defineProps({
  attraction: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['click'])

const handleClick = () => {
  emit('click', props.attraction)
}
</script>

<style lang="scss" scoped>
.attraction-card {
  background: #FFFFFF;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 16px;
  
  .card-image {
    position: relative;
    height: 180px;
    
    image {
      width: 100%;
      height: 100%;
    }
    
    .rating {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(0, 0, 0, 0.6);
      color: #FFD700;
      padding: 4px 8px;
      border-radius: 4px;
      font-size: 12px;
      display: flex;
      align-items: center;
      gap: 2px;
      
      .star {
        font-size: 14px;
      }
    }
  }
  
  .card-content {
    padding: 12px;
    
    .title-row {
      .name {
        font-size: 16px;
        font-weight: 600;
        color: #212121;
      }
    }
    
    .location-row {
      margin-top: 4px;
      
      .location {
        font-size: 14px;
        color: #757575;
      }
    }
    
    .price-row {
      margin-top: 8px;
      display: flex;
      align-items: baseline;
      gap: 4px;
      
      .label {
        font-size: 12px;
        color: #757575;
      }
      
      .price {
        font-size: 16px;
        font-weight: 600;
        color: #FF8F00;
      }
    }
  }
}
</style>
