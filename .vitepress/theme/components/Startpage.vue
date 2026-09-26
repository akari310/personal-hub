<script setup>
import { ref, onMounted, watch } from 'vue'
import SearchBar from './SearchBar.vue'

const links = ref([])
const isAdmin = ref(false)
const showAddModal = ref(false)
const githubToken = ref('')
const newName = ref('')
const newUrl = ref('')

const showWeather = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('showWeather') !== 'false' : true)
const showLinks = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('showLinks') !== 'false' : true)

if (typeof window !== 'undefined') {
  watch(showWeather, (val) => localStorage.setItem('showWeather', val.toString()))
  watch(showLinks, (val) => localStorage.setItem('showLinks', val.toString()))
}

const newIcon = ref('🔗')
const repoOwner = 'akari310'
const repoName = 'personal-hub'
const filePath = 'public/links.json'

// Clock and Weather
const timeString = ref('')
const weatherTemp = ref('--')
const weatherIconUrl = ref('https://assets.msn.com/weathermapdata/1/static/weather/Icons/taskbar_v10/Condition_Card/MostlySunnyDay.svg')
const msnLink = 'https://www.msn.com/vi-vn/weather/forecast/in-Y%C3%AAn-B%C3%A1i,Vi%E1%BB%87t-Nam'

function updateClock() {
  const now = new Date()
  timeString.value = now.toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit', hour12: false })
}

async function fetchWeather() {
  try {
    const res = await fetch('https://api.open-meteo.com/v1/forecast?latitude=21.7167&longitude=104.8833&current_weather=true')
    const data = await res.json()
    if (data.current_weather) {
      weatherTemp.value = Math.round(data.current_weather.temperature)
      const code = data.current_weather.weathercode
      const isDay = data.current_weather.is_day === 1
      
      let icon = isDay ? 'SunnyDayV3.svg' : 'ClearNightV3.svg'
      if (code === 1 || code === 2) icon = isDay ? 'PartlyCloudyDayV3.svg' : 'PartlyCloudyNightV3.svg'
      else if (code === 3) icon = 'CloudyV3.svg'
      else if (code >= 45 && code <= 48) icon = 'FogV3.svg'
      else if (code >= 51 && code <= 67) icon = 'LightRainV3.svg'
      else if (code >= 80 && code <= 82) icon = isDay ? 'RainShowersDayV3.svg' : 'RainShowersNightV3.svg'
      else if (code >= 95) icon = 'ThunderstormsV3.svg'
      
      weatherIconUrl.value = `https://assets.msn.com/weathermapdata/1/static/weather/Icons/taskbar_v10/Condition_Card/${icon}`
    }
  } catch(e) {
    console.error('Weather error:', e)
  }
}

onMounted(async () => {
  updateClock()
  setInterval(updateClock, 1000)
  fetchWeather()
  
  // Smart redirect if they accidentally land on the old note domain
  const host = window.location.hostname
  const path = window.location.pathname
  
  if (host.startsWith('note') && path === '/') {
    window.location.href = 'https://home.akari.nx.kg/notes/'
  }
  
  await fetchLinks()
  
  // Check if token exists in localStorage
  const token = localStorage.getItem('gh_admin_token')
  if (token) {
    githubToken.value = token
    isAdmin.value = true
  }

  // Hidden admin mode trigger (Ctrl+Shift+A)
  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.shiftKey && e.key === 'A') {
      const input = prompt('Enter Admin Token:')
      if (input) {
        localStorage.setItem('gh_admin_token', input)
        githubToken.value = input
        isAdmin.value = true
        alert('Admin mode activated!')
      }
    }
  })
})

async function fetchLinks() {
  try {
    const res = await fetch('/links.json?t=' + Date.now())
    if (res.ok) {
      links.value = await res.json()
    }
  } catch (e) {
    console.error('Failed to load links:', e)
  }
}

function openSettings() {
  if (!githubToken.value) {
    const token = prompt('Enter Admin Token to Unlock Settings:')
    if (token) {
      localStorage.setItem('gh_admin_token', token)
      githubToken.value = token
      isAdmin.value = true
      showAddModal.value = true
    }
  } else {
    showAddModal.value = true
  }
}

async function addLink() {
  if (!newName.value || !newUrl.value) return alert('Name and URL are required')
  
  const newLink = {
    name: newName.value,
    url: newUrl.value
  }

  const updatedLinks = [...links.value, newLink]
  const contentBase64 = btoa(unescape(encodeURIComponent(JSON.stringify(updatedLinks, null, 2))))
  
  try {
    const apiUrl = `https://api.github.com/repos/${repoOwner}/${repoName}/contents/${filePath}`
    const getRes = await fetch(apiUrl, {
      headers: {
        'Authorization': `token ${githubToken.value}`,
        'Accept': 'application/vnd.github.v3+json'
      }
    })
    
    if (!getRes.ok) throw new Error('Failed to get current file metadata (Token might be invalid)')
    
    const fileData = await getRes.json()
    const sha = fileData.sha

    const putRes = await fetch(apiUrl, {
      method: 'PUT',
      headers: {
        'Authorization': `token ${githubToken.value}`,
        'Accept': 'application/vnd.github.v3+json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: `feat: add link ${newLink.name} via admin panel`,
        content: contentBase64,
        sha: sha
      })
    })

    if (putRes.ok) {
      links.value = updatedLinks
      showAddModal.value = false
      newName.value = ''
      newUrl.value = ''
      newIcon.value = '🔗'
      alert('Link added successfully! It will take a minute to deploy.')
    } else {
      const err = await putRes.json()
      throw new Error(err.message || 'Failed to update file')
    }
  } catch (e) {
    alert(e.message)
    console.error(e)
  }
}
</script>

<template>
  <div class="startpage-overlay">
    <!-- Clock and Weather (Top Left) -->
    <div v-if="showWeather" class="top-left-widget">
      <div class="clock-display">{{ timeString }}</div>
      <a :href="msnLink" target="_blank" class="weather-widget">
        <span class="weather-location">Yên Bái</span>
        <img :src="weatherIconUrl" class="weather-icon" alt="Weather" />
        <span class="weather-temp">{{ weatherTemp }}°C</span>
      </a>
    </div>

    <!-- Hub Navigation Buttons (Top Right) -->
    <div class="hub-nav">
      <a href="https://akari.nx.kg" class="hub-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
        Bio
      </a>
      <a href="/notes/" class="hub-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
        Notes
      </a>
      <button @click="openSettings" class="hub-btn icon-btn" title="Page Settings">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
      </button>
    </div>

    <div class="content-wrapper">
      <div class="search-section">
        <SearchBar />
      </div>

      <!-- Quick Links Grid integrated smoothly -->
      <div class="bookmarks-section" v-if="showLinks && links.length > 0">
        <div class="bento-grid">
          <a v-for="link in links" :key="link.url" :href="link.url" target="_blank" class="bento-card">
            <img :src="`https://www.google.com/s2/favicons?domain=${link.url}&sz=128`" :alt="link.name" class="bento-icon-img" />
            <span class="bento-name">{{ link.name }}</span>
          </a>
        </div>
      </div>
    </div>
    
    <!-- Edge Style Settings Panel -->
    <transition name="slide-right">
      <div v-if="showAddModal" class="settings-panel">
        <div class="panel-header">
          <h2>Cài đặt trang</h2>
          <button class="close-btn" @click="showAddModal = false">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
          </button>
        </div>
        
        <div class="panel-content">
          <div class="setting-item">
            <span>Hiển thị thời tiết</span>
            <label class="toggle-switch">
              <input type="checkbox" v-model="showWeather">
              <span class="slider"></span>
            </label>
          </div>
          
          <div class="setting-item">
            <span>Các liên kết nhanh</span>
            <label class="toggle-switch">
              <input type="checkbox" v-model="showLinks">
              <span class="slider"></span>
            </label>
          </div>

          <div class="settings-section">
            <h3 style="margin-top: 16px; font-size: 0.95rem;">Thêm liên kết (Tùy chỉnh Edge)</h3>
            <div class="form-group">
              <input v-model="newName" type="text" placeholder="Tên web (VD: Github)" />
            </div>
            <div class="form-group">
              <input v-model="newUrl" type="url" placeholder="URL (https://...)" />
            </div>
            <button @click="addLink" class="btn-save" style="width: 100%">Lưu Liên kết</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.startpage-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-image: url('/bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 9999;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  overflow-y: auto;
}

.startpage-overlay::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(30,30,46,0.2) 0%, rgba(17,17,27,0.8) 100%);
  pointer-events: none;
  z-index: 0;
}

.content-wrapper {
  position: relative;
  z-index: 10;
  width: 100%;
  max-width: 680px;
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 15vh;
  padding: 0 24px 60px;
  gap: 36px;
}

.search-section {
  width: 100%;
}

.bookmarks-section {
  width: 100%;
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.bento-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  width: 100%;
}

.bento-card {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 12px;
  padding: 8px 16px 8px 8px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 100px; /* Pill shape */
  text-decoration: none;
  color: #cdd6f4;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 140px;
}

.bento-card:hover {
  transform: translateY(-3px) scale(1.02);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.bento-icon-img {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  background-color: white; 
  padding: 3px; 
  flex-shrink: 0;
}

.bento-card:hover .bento-icon-img {
  transform: scale(1.1);
}

.add-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  background-color: transparent;
  box-shadow: none;
  padding: 0;
}

.bento-name {
  font-weight: 600;
  font-size: 0.9rem;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: 0.01em;
  padding-right: 8px;
}

/* Nav */
.hub-nav {
  position: absolute;
  top: 24px;
  right: 32px;
  display: flex;
  align-items: center;
  gap: 12px;
  z-index: 100;
}

.hub-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 18px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 100px;
  color: #cdd6f4;
  font-weight: 600;
  font-size: 0.85rem;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  box-sizing: border-box;
}

.hub-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #fff;
  transform: translateY(-2px);
}

/* Top Left Widget */
.top-left-widget {
  position: absolute;
  top: 24px;
  left: 32px;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 16px;
  z-index: 100;
  color: #cdd6f4;
}

.clock-display {
  font-size: 1.5rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-shadow: 0 2px 8px rgba(0,0,0,0.4);
}

.weather-widget {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 100px;
  text-decoration: none;
  color: #cdd6f4;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.weather-widget:hover {
  background: rgba(203, 166, 247, 0.25);
  transform: translateY(-2px);
}

.weather-location {
  opacity: 0.9;
}

.weather-icon {
  width: 24px;
  height: 24px;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Settings Panel (Edge Style) */
.settings-panel {
  position: fixed;
  top: 72px;
  right: 16px;
  width: 320px;
  background: rgba(36, 36, 36, 0.85);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  color: #fff;
  z-index: 10000;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.panel-header h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-btn {
  background: transparent;
  border: none;
  color: #a6adc8;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }

.panel-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(255,255,255,0.2);
  transition: .3s;
  border-radius: 22px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
}
input:checked + .slider { background-color: #0078d4; }
input:checked + .slider:before { transform: translateX(18px); }

.slide-right-enter-active, .slide-right-leave-active { transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1); }
.slide-right-enter-from, .slide-right-leave-to { opacity: 0; transform: translateX(20px); }

.form-group {
  margin-bottom: 12px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  background: rgba(0,0,0,0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  outline: none;
  font-size: 0.9rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #0078d4;
}

.btn-save {
  padding: 10px 24px;
  background: #0078d4;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-save:hover {
  opacity: 0.9;
}

</style>

.icon-btn { width: 40px; height: 40px; padding: 0; display: flex; align-items: center; justify-content: center; border-radius: 50%; cursor: pointer; flex-shrink: 0; }

