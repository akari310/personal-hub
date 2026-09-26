<script setup>
import { ref, onMounted } from 'vue'
import SearchBar from './SearchBar.vue'

const links = ref([])
const isAdmin = ref(false)
const showAddModal = ref(false)
const githubToken = ref('')
const newName = ref('')
const newUrl = ref('')
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
    <div class="top-left-widget">
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
      <div class="bookmarks-section" v-if="links.length > 0">
        <div class="bento-grid">
          <a v-for="link in links" :key="link.url" :href="link.url" target="_blank" class="bento-card">
            <img :src="`https://www.google.com/s2/favicons?domain=${link.url}&sz=128`" :alt="link.name" class="bento-icon-img" />
            <span class="bento-name">{{ link.name }}</span>
          </a>
        </div>
      </div>
    </div>
    
    <!-- Settings / Add Link Modal -->
    <transition name="fade">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal">
          <h2>Page Settings</h2>
          
          <div class="settings-section">
            <h3>Add Quick Link</h3>
            <div class="form-group">
              <label>Name</label>
              <input v-model="newName" type="text" placeholder="e.g. My Repo" />
            </div>
            <div class="form-group">
              <label>URL</label>
              <input v-model="newUrl" type="url" placeholder="https://..." />
            </div>
          </div>
          
          <div class="modal-actions">
            <button @click="showAddModal = false" class="btn-cancel">Close</button>
            <button @click="addLink" class="btn-save">Add Link</button>
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
  background: rgba(30, 30, 46, 0.45);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 100px; /* Pill shape */
  text-decoration: none;
  color: #cdd6f4;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 140px;
}

.bento-card:hover {
  transform: translateY(-3px) scale(1.02);
  background: rgba(49, 50, 68, 0.7);
  border-color: rgba(203, 166, 247, 0.4);
  box-shadow: 0 8px 20px rgba(203, 166, 247, 0.2);
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
  gap: 12px;
  z-index: 100;
}

.hub-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 18px;
  background: rgba(30, 30, 46, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 100px;
  color: #cdd6f4;
  font-weight: 600;
  font-size: 0.85rem;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

.hub-btn:hover {
  background: rgba(203, 166, 247, 0.25);
  border-color: rgba(203, 166, 247, 0.5);
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
  background: rgba(30, 30, 46, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
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

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(12px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal {
  background: #1e1e2e;
  padding: 32px;
  border-radius: 24px;
  width: 90%;
  max-width: 400px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 24px 48px rgba(0,0,0,0.4);
  transform: scale(0.95);
  animation: modalIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
  text-align: left;
}

@keyframes modalIn {
  to { transform: scale(1); }
}

.modal h2 {
  margin-top: 0;
  margin-bottom: 24px;
  color: #cdd6f4;
  font-size: 1.5rem;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #a6adc8;
  font-size: 0.9rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  background: #11111b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #cdd6f4;
  outline: none;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #cba6f7;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 30px;
}

.btn-cancel {
  padding: 10px 20px;
  background: rgba(255,255,255,0.05);
  border: none;
  border-radius: 10px;
  color: #cdd6f4;
  cursor: pointer;
  font-weight: 600;
  transition: background 0.2s;
}

.btn-cancel:hover {
  background: rgba(255,255,255,0.1);
}

.btn-save {
  padding: 10px 24px;
  background: #cba6f7;
  color: #11111b;
  border: none;
  border-radius: 10px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.2s, background 0.2s;
}

.btn-save:hover {
  background: #b4befe;
  transform: translateY(-2px);
}

.icon-btn {
  padding: 10px;
  border-radius: 50%;
  cursor: pointer;
}

.settings-section h3 {
  font-size: 1.05rem;
  color: #cdd6f4;
  margin-top: 0;
  margin-bottom: 16px;
  border-bottom: 1px solid rgba(255,255,255,0.08);
  padding-bottom: 8px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
