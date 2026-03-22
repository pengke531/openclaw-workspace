<template>
  <view class="people-counter">
    <view class="title">出行人数</view>
    
    <view class="counter-item">
      <view class="label">成人</view>
      <view class="counter">
        <van-icon name="minus" @click="decrement('adults')" :disabled="adults <= 1" />
        <text class="count">{{ adults }}</text>
        <van-icon name="plus" @click="increment('adults')" />
      </view>
    </view>
    
    <view class="counter-item">
      <view class="label">儿童</view>
      <view class="counter">
        <van-icon name="minus" @click="decrement('children')" :disabled="children <= 0" />
        <text class="count">{{ children }}</text>
        <van-icon name="plus" @click="increment('children')" />
      </view>
    </view>
    
    <view class="counter-item">
      <view class="label">老人</view>
      <view class="counter">
        <van-icon name="minus" @click="decrement('seniors')" :disabled="seniors <= 0" />
        <text class="count">{{ seniors }}</text>
        <van-icon name="plus" @click="increment('seniors')" />
      </view>
    </view>
    
    <view class="counter-item">
      <view class="label">军人</view>
      <view class="counter">
        <van-icon name="minus" @click="decrement('soldiers')" :disabled="soldiers <= 0" />
        <text class="count">{{ soldiers }}</text>
        <van-icon name="plus" @click="increment('soldiers')" />
      </view>
    </view>
    
    <view class="total">
      <text class="label">合计:</text>
      <text class="count">{{ total }}</text>
      <text class="unit">人</text>
    </view>
  </view>
</template>

<script setup>
import { computed } from 'vue'
import { useTourismStore } from '@/store/tourism'

const tourismStore = useTourismStore()

const booking = computed(() => tourismStore.booking)

const adults = computed({
  get: () => booking.value.adults,
  set: (val) => tourismStore.updateBooking({ adults: val })
})

const children = computed({
  get: () => booking.value.children,
  set: (val) => tourismStore.updateBooking({ children: val })
})

const seniors = computed({
  get: () => booking.value.seniors,
  set: (val) => tourismStore.updateBooking({ seniors: val })
})

const soldiers = computed({
  get: () => booking.value.soldiers,
  set: (val) => tourismStore.updateBooking({ soldiers: val })
})

const total = computed(() => {
  return adults.value + children.value + seniors.value + soldiers.value
})

const increment = (field) => {
  tourismStore.updateBooking({ [field]: booking.value[field] + 1 })
}

const decrement = (field) => {
  const minValues = { adults: 1, children: 0, seniors: 0, soldiers: 0 }
  if (booking.value[field] > minValues[field]) {
    tourismStore.updateBooking({ [field]: booking.value[field] - 1 })
  }
}
</script>

<style lang="scss" scoped>
.people-counter {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 16px;
  
  .title {
    font-size: 16px;
    font-weight: 600;
    color: #212121;
    margin-bottom: 16px;
  }
  
  .counter-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #F0F0F0;
    
    &:last-of-type {
      border-bottom: none;
    }
    
    .label {
      font-size: 14px;
      color: #212121;
    }
    
    .counter {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .count {
        font-size: 16px;
        font-weight: 600;
        min-width: 32px;
        text-align: center;
      }
    }
  }
  
  .total {
    margin-top: 16px;
    padding-top: 16px;
    border-top: 1px solid #E0E0E0;
    display: flex;
    align-items: baseline;
    justify-content: flex-end;
    gap: 4px;
    
    .label {
      font-size: 14px;
      color: #757575;
    }
    
    .count {
      font-size: 24px;
      font-weight: 700;
      color: #2E7D32;
    }
    
    .unit {
      font-size: 14px;
      color: #757575;
    }
  }
}
</style>
