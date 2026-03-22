<template>
  <view class="price-summary">
    <view class="section-title">价格明细</view>
    
    <view class="price-items">
      <!-- Adult price -->
      <view class="price-item" v-if="booking.adults > 0">
        <text class="label">成人 × {{ booking.adults }}</text>
        <text class="value">¥{{ adultTotal }}</text>
      </view>
      
      <!-- Accommodation -->
      <view class="price-item" v-if="nights > 0">
        <text class="label">住宿 × {{ nights }}晚</text>
        <text class="value">¥{{ accommodationTotal }}</text>
      </view>
      
      <!-- Vehicle -->
      <view class="price-item" v-if="booking.vehicle">
        <text class="label">车辆</text>
        <text class="value">¥{{ vehicleTotal }}</text>
      </view>
    </view>
    
    <!-- Discount -->
    <view class="discount-section" v-if="discount > 0">
      <view class="divider"></view>
      <view class="price-item discount">
        <text class="label">优惠折扣</text>
        <text class="value">-¥{{ discount }}</text>
      </view>
    </view>
    
    <!-- Total -->
    <view class="divider"></view>
    <view class="total-section">
      <text class="label">总价:</text>
      <text class="total-price">¥{{ total }}</text>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useTourismStore } from '@/store/tourism'

const tourismStore = useTourismStore()

const booking = computed(() => tourismStore.booking)
const route = computed(() => tourismStore.currentRoute)

// Calculate prices
const adultTotal = computed(() => {
  if (!route.value) return 0
  return route.value.adultPrice * booking.value.adults
})

const accommodationPrices = {
  economic: 580,
  comfortable: 980,
  luxury: 1580
}

const accommodationTotal = computed(() => {
  if (!route.value) return 0
  const price = accommodationPrices[booking.value.accommodation] || 980
  return price * (route.value.duration || 4)
})

const vehiclePrices = {
  '5座SUV': 1200,
  '7座商务': 1800,
  '15座中巴': 2500
}

const vehicleTotal = computed(() => {
  return booking.value.vehicle ? (vehiclePrices[booking.value.vehicle] || 0) : 0
})

const nights = computed(() => {
  return route.value?.duration || 4
})

const discounts = {
  senior: 200,
  child: 100,
  soldier: 150
}

const discount = computed(() => {
  return booking.value.discountType ? discounts[booking.value.discountType] : 0
})

const total = computed(() => tourismStore.totalPrice)
</script>

<style lang="scss" scoped>
.price-summary {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  
  .section-title {
    font-size: 16px;
    font-weight: 600;
    color: #212121;
    margin-bottom: 12px;
  }
  
  .price-items {
    .price-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px 0;
      
      .label {
        font-size: 14px;
        color: #757575;
      }
      
      .value {
        font-size: 14px;
        color: #212121;
      }
      
      &.discount .value {
        color: #4CAF50;
      }
    }
  }
  
  .divider {
    height: 1px;
    background: #E0E0E0;
    margin: 8px 0;
  }
  
  .discount-section {
    .price-item {
      &.discount {
        .label {
          color: #4CAF50;
        }
      }
    }
  }
  
  .total-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 8px;
    
    .label {
      font-size: 16px;
      font-weight: 500;
      color: #212121;
    }
    
    .total-price {
      font-size: 24px;
      font-weight: 700;
      color: #FF8F00;
    }
  }
}
</style>
