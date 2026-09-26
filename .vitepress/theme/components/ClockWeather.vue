<script setup>
import { ref, onMounted } from 'vue'
import { showWeather } from './store.js'

const timeStr = ref('00:00')
const weather = ref({ temp: '--', condition: 'Unknown', icon: '❓' })

function updateTime() {
  const now = new Date()
  const hh = String(now.getHours()).padStart(2, '0')
  const mm = String(now.getMinutes()).padStart(2, '0')
  timeStr.value = `${hh}:${mm}`
}

async function fetchWeather() {
  try {
    const lat = 21.7053, lon = 104.875
    const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current_weather=true`)
    const data = await res.json()
    if (data.current_weather) {
      weather.value.temp = Math.round(data.current_weather.temperature)
      const code = data.current_weather.weathercode
      if (code <= 1) weather.value.icon = '☀️'
      else if (code <= 3) weather.value.icon = '⛅'
      else if (code <= 49) weather.value.icon = '☁️'
      else if (code <= 69) weather.value.icon = '🌧️'
      else if (code <= 79) weather.value.icon = '❄️'
      else weather.value.icon = '⛈️'
      weather.value.condition = 'Yên Bái'
    }
  } catch(e) {
    console.error(e)
  }
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 1000)
  fetchWeather()
})
</script>

<template>
  <div v-if="showWeather" class="top-left-widget">
    <div class="clock-display">{{ timeStr }}</div>
    <a href="https://www.msn.com/vi-vn/weather" target="_blank" class="weather-widget" title="Nhấp để xem dự báo thời tiết MSN">
      <span class="weather-icon">{{ weather.icon }}</span>
      <span class="weather-location">{{ weather.condition }} • {{ weather.temp }}°C</span>
    </a>
  </div>
</template>
