<template>
  <div class="booking-page">
    <!-- 步骤条 -->
    <van-steps :steps="steps" :active="currentStep" />

    <!-- 步骤1: 选择日期 -->
    <div v-if="currentStep === 0" class="step-content">
      <van-cell-group>
        <van-cell title="出发日期" :value="selectedDate" is-link @click="showDatePicker = true" />
      </van-cell-group>
      <van-calendar
        v-model:show="showDatePicker"
        @confirm="onDateConfirm"
        :min-date="minDate"
        color="#2E7D32"
      />
    </div>

    <!-- 步骤2: 人数选择 -->
    <div v-if="currentStep === 1" class="step-content">
      <van-cell-group>
        <van-cell title="成人">
          <van-stepper v-model="people.adult" :min="1" :max="20" slot="label" />
        </van-cell>
        <van-cell title="儿童 (1.2m以下)">
          <van-stepper v-model="people.child" :min="0" :max="10" slot="label" />
        </van-cell>
        <van-cell title="老人 (60岁以上)">
          <van-stepper v-model="people.senior" :min="0" :max="10" slot="label" />
        </van-cell>
        <van-cell title="军人">
          <van-stepper v-model="people.military" :min="0" :max="5" slot="label" />
        </van-cell>
      </van-cell-group>
      
      <div class="people-summary">
        <van-tag type="primary">总人数: {{ totalPeople }}</van-tag>
      </div>
    </div>

    <!-- 步骤3: 优惠选择 -->
    <div v-if="currentStep === 2" class="step-content">
      <van-radio-group v-model="selectedDiscount">
        <van-cell-group>
          <van-cell clickable @click="selectedDiscount = 'none'">
            <template #title>
              <span>不享受优惠</span>
            </template>
            <van-radio slot="right-icon" name="none" />
          </van-cell>
          <van-cell clickable @click="selectedDiscount = 'senior'" v-if="people.senior > 0">
            <template #title>
              <span>老年票 ({{ people.senior }}人)</span>
            </template>
            <template #label>
              <span class="discount-label">60岁以上 -¥200/人</span>
            </template>
            <van-radio slot="right-icon" name="senior" />
          </van-cell>
          <van-cell clickable @click="selectedDiscount = 'child'" v-if="people.child > 0">
            <template #title>
              <span>儿童票 ({{ people.child }}人)</span>
            </template>
            <template #label>
              <span class="discount-label">1.2m以下 -¥100/人</span>
            </template>
            <van-radio slot="right-icon" name="child" />
          </van-cell>
          <van-cell clickable @click="selectedDiscount = 'military'" v-if="people.military > 0">
            <template #title>
              <span>军人票 ({{ people.military }}人)</span>
            </template>
            <template #label>
              <span class="discount-label">凭有效证件 -¥150/人</span>
            </template>
            <van-radio slot="right-icon" name="military" />
          </van-cell>
        </van-cell-group>
      </van-radio-group>
    </div>

    <!-- 步骤4: 住宿选择 -->
    <div v-if="currentStep === 3" class="step-content">
      <van-radio-group v-model="selectedAccommodation">
        <van-cell-group>
          <van-cell clickable @click="selectedAccommodation = 'budget'">
            <template #title>
              <div class="accommodation-title">
                <span>经济型</span>
                <van-tag type="success" size="small">最实惠</van-tag>
              </div>
            </template>
            <template #label>
              <span>¥580/晚 · 干净舒适</span>
            </template>
            <van-radio slot="right-icon" name="budget" />
          </van-cell>
          <van-cell clickable @click="selectedAccommodation = 'comfort'">
            <template #title>
              <div class="accommodation-title">
                <span>舒适型</span>
                <van-tag type="primary" size="small">推荐</van-tag>
              </div>
            </template>
            <template #label>
              <span>¥980/晚 · 品质保障</span>
            </template>
            <van-radio slot="right-icon" name="comfort" />
          </van-cell>
          <van-cell clickable @click="selectedAccommodation = 'luxury'">
            <template #title>
              <span>豪华型</span>
            </template>
            <template #label>
              <span>¥1580/晚 · 尊享体验</span>
            </template>
            <van-radio slot="right-icon" name="luxury" />
          </van-cell>
        </van-cell-group>
      </van-radio-group>
    </div>

    <!-- 步骤5: 车辆推荐 -->
    <div v-if="currentStep === 4" class="step-content">
      <van-radio-group v-model="selectedVehicle">
        <van-cell-group>
          <van-cell clickable @click="selectedVehicle = 'suv'" :disabled="totalPeople > 4">
            <template #title>
              <span>5座 SUV</span>
              <van-tag v-if="totalPeople <= 4" type="success" size="small">推荐</van-tag>
            </template>
            <template #label>
              <span>适合2-4人 · 空间宽敞</span>
            </template>
            <van-radio slot="right-icon" name="suv" :disabled="totalPeople > 4" />
          </van-cell>
          <van-cell clickable @click="selectedVehicle = 'business'" :disabled="totalPeople < 5 || totalPeople > 6">
            <template #title>
              <span>7座商务</span>
              <van-tag v-if="totalPeople >= 5 && totalPeople <= 6" type="primary" size="small">推荐</van-tag>
            </template>
            <template #label>
              <span>适合5-6人 · 舒适乘坐</span>
            </template>
            <van-radio slot="right-icon" name="business" :disabled="totalPeople < 5 || totalPeople > 6" />
          </van-cell>
          <van-cell clickable @click="selectedVehicle = 'bus'" :disabled="totalPeople < 7 || totalPeople > 14">
            <template #title>
              <span>15座中巴</span>
              <van-tag v-if="totalPeople >= 7 && totalPeople <= 14" type="warning" size="small">推荐</van-tag>
            </template>
            <template #label>
              <span>适合7-14人 · 团体首选</span>
            </template>
            <van-radio slot="right-icon" name="bus" :disabled="totalPeople < 7 || totalPeople > 14" />
          </van-cell>
        </van-cell-group>
      </van-radio-group>

      <van-notice-bar 
        v-if="totalPeople > 14" 
        text="出行人数超过14人，请联系客服安排" 
        left-icon="warning-o"
      />
    </div>

    <!-- 步骤6: 价格汇总 -->
    <div v-if="currentStep === 5" class="step-content">
      <van-cell-group>
        <van-cell title="成人 × {{ people.adult }}">
          <span>¥{{ people.adult * adultPrice }}</span>
        </van-cell>
        <van-cell title="儿童 × {{ people.child }}">
          <span>¥{{ people.child * childPrice }}</span>
        </van-cell>
        <van-cell title="住宿 ({{ accommodationNights }}晚)">
          <span>¥{{ accommodationPrice }}</span>
        </van-cell>
        <van-cell title="车辆">
          <span>¥{{ vehiclePrice }}</span>
        </van-cell>
        <van-cell title="优惠折扣" type="success">
          <span class="discount">-¥{{ discountAmount }}</span>
        </van-cell>
        <van-cell title="总价" type="primary">
          <span class="total-price">¥{{ totalPrice }}</span>
        </van-cell>
      </van-cell-group>
    </div>

    <!-- 底部操作栏 -->
    <div class="bottom-bar">
      <van-button 
        v-if="currentStep > 0" 
        type="default" 
        @click="prevStep"
        class="prev-btn"
      >
        上一步
      </van-button>
      <van-button 
        v-if="currentStep < steps.length - 1" 
        type="primary" 
        @click="nextStep"
        class="next-btn"
        color="#2E7D32"
      >
        下一步
      </van-button>
      <van-button 
        v-if="currentStep === steps.length - 1" 
        type="primary" 
        @click="submitOrder"
        class="submit-btn"
        color="#2E7D32"
      >
        提交订单
      </van-button>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

export default {
  name: 'BookingPage',
  setup() {
    // 步骤配置
    const steps = [
      { text: '选择日期', icon: 'calender-o' },
      { text: '出行人数', icon: 'user-o' },
      { text: '优惠选择', icon: 'coupon-o' },
      { text: '住宿选择', icon: 'hotel-o' },
      { text: '车辆推荐', icon: 'car-o' },
      { text: '价格汇总', icon: 'balance-o' }
    ]

    const currentStep = ref(0)
    
    // 日期选择
    const showDatePicker = ref(false)
    const selectedDate = ref('请选择出发日期')
    const minDate = new Date()
    
    const onDateConfirm = (date) => {
      selectedDate.value = `${date.getMonth() + 1}月${date.getDate()}日`
      showDatePicker.value = false
    }

    // 人数选择
    const people = ref({
      adult: 2,
      child: 0,
      senior: 0,
      military: 0
    })

    const totalPeople = computed(() => {
      return people.value.adult + people.value.child + 
             people.value.senior + people.value.military
    })

    // 优惠选择
    const selectedDiscount = ref('none')

    // 住宿选择
    const selectedAccommodation = ref('comfort')
    const accommodationNights = 4 // 默认4晚

    const accommodationPrices = {
      budget: 580,
      comfort: 980,
      luxury: 1580
    }

    const accommodationPrice = computed(() => {
      return accommodationPrices[selectedAccommodation.value] * accommodationNights
    })

    // 车辆推荐
    const selectedVehicle = ref('suv')

    const vehiclePrices = {
      suv: 800,
      business: 1200,
      bus: 2000
    }

    const vehiclePrice = computed(() => {
      return vehiclePrices[selectedVehicle.value]
    })

    // 价格计算
    const adultPrice = 2580
    const childPrice = 1290 // 儿童半价

    const discountAmount = computed(() => {
      switch (selectedDiscount.value) {
        case 'senior':
          return people.value.senior * 200
        case 'child':
          return people.value.child * 100
        case 'military':
          return people.value.military * 150
        default:
          return 0
      }
    })

    const totalPrice = computed(() => {
      const basePrice = people.value.adult * adultPrice + 
                       people.value.child * childPrice +
                       accommodationPrice.value + 
                       vehiclePrice.value
      return basePrice - discountAmount.value
    })

    // 导航
    const nextStep = () => {
      if (currentStep.value < steps.length - 1) {
        currentStep.value++
      }
    }

    const prevStep = () => {
      if (currentStep.value > 0) {
        currentStep.value--
      }
    }

    // 提交订单
    const submitOrder = () => {
      uni.showToast({
        title: '订单提交成功',
        icon: 'success'
      })
      // TODO: 调用后端接口
    }

    return {
      steps,
      currentStep,
      showDatePicker,
      selectedDate,
      minDate,
      onDateConfirm,
      people,
      totalPeople,
      selectedDiscount,
      selectedAccommodation,
      accommodationNights,
      accommodationPrice,
      selectedVehicle,
      vehiclePrice,
      adultPrice,
      childPrice,
      discountAmount,
      totalPrice,
      nextStep,
      prevStep,
      submitOrder
    }
  }
}
</script>

<style scoped>
.booking-page {
  padding-bottom: 120rpx;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.step-content {
  padding: 16rpx;
}

.people-summary {
  text-align: center;
  padding: 24rpx;
}

.discount-label {
  color: #FF8F00;
  font-size: 12px;
}

.accommodation-title {
  display: flex;
  align-items: center;
  gap: 12rpx;
}

.discount {
  color: #4CAF50;
}

.total-price {
  font-size: 18px;
  font-weight: 600;
  color: #FF8F00;
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  padding: 20rpx;
  background: #fff;
  box-shadow: 0 -2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.prev-btn {
  flex: 1;
  margin-right: 20rpx;
}

.next-btn,
.submit-btn {
  flex: 2;
}
</style>
