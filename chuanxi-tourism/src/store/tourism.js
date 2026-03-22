import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { getRoutes, getRouteDetail, getAttractions } from '@/api/tourism'

export const useTourismStore = defineStore('tourism', () => {
  // State
  const routes = ref([])
  const currentRoute = ref(null)
  const attractions = ref([])
  const loading = ref(false)
  
  // Booking state
  const booking = ref({
    routeId: null,
    date: null,
    adults: 2,
    children: 0,
    seniors: 0,
    soldiers: 0,
    discountType: null,
    accommodation: 'comfortable', // economic, comfortable, luxury
    vehicle: null // 5座 SUV, 7座商务, 15座中巴
  })
  
  // Computed
  const totalPrice = computed(() => {
    const route = currentRoute.value
    if (!route) return 0
    
    let price = route.adultPrice * booking.value.adults
    
    // Accommodation
    const accommodationPrices = {
      economic: route.economicPrice || 580,
      comfortable: route.comfortablePrice || 980,
      luxury: route.luxuryPrice || 1580
    }
    const accommodationPrice = accommodationPrices[booking.value.accommodation] || 980
    const nights = route.duration || 4
    price += accommodationPrice * nights
    
    // Vehicle
    const vehiclePrices = {
      '5座SUV': 1200,
      '7座商务': 1800,
      '15座中巴': 2500
    }
    if (booking.value.vehicle) {
      price += vehiclePrices[booking.value.vehicle] || 0
    }
    
    // Discounts (not stacked, use highest)
    const discounts = {
      'senior': 200,
      'child': 100,
      'soldier': 150
    }
    const discount = booking.value.discountType ? discounts[booking.value.discountType] : 0
    
    return price - discount
  })
  
  // Actions
  const fetchRoutes = async () => {
    loading.value = true
    try {
      const res = await getRoutes()
      routes.value = res.data
    } finally {
      loading.value = false
    }
  }
  
  const fetchRouteDetail = async (id) => {
    loading.value = true
    try {
      const res = await getRouteDetail(id)
      currentRoute.value = res.data
      booking.value.routeId = id
    } finally {
      loading.value = false
    }
  }
  
  const fetchAttractions = async () => {
    loading.value = true
    try {
      const res = await getAttractions()
      attractions.value = res.data
    } finally {
      loading.value = false
    }
  }
  
  const updateBooking = (data) => {
    booking.value = { ...booking.value, ...data }
  }
  
  const resetBooking = () => {
    booking.value = {
      routeId: null,
      date: null,
      adults: 2,
      children: 0,
      seniors: 0,
      soldiers: 0,
      discountType: null,
      accommodation: 'comfortable',
      vehicle: null
    }
    currentRoute.value = null
  }
  
  // Vehicle recommendation based on group size
  const recommendVehicle = computed(() => {
    const total = booking.value.adults + booking.value.children + booking.value.seniors + booking.value.soldiers
    if (total <= 4) return '5座SUV'
    if (total <= 6) return '7座商务'
    if (total <= 14) return '15座中巴'
    return null // 15+ need customer service
  })
  
  return {
    routes,
    currentRoute,
    attractions,
    loading,
    booking,
    totalPrice,
    recommendVehicle,
    fetchRoutes,
    fetchRouteDetail,
    fetchAttractions,
    updateBooking,
    resetBooking
  }
})
