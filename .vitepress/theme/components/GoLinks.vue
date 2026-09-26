<script setup>
import { ref, onMounted } from 'vue'

const links = ref([])
const isAdmin = ref(false)
const showAddModal = ref(false)
const githubToken = ref('')

// Form state
const newName = ref('')
const newUrl = ref('')
const newIcon = ref('🔗')

const repoOwner = 'akari310'
const repoName = 'personal-hub'
const filePath = 'public/links.json'

onMounted(async () => {
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
    // Fetch directly from the deployed static file to avoid rate limits
    const res = await fetch('/links.json?t=' + Date.now())
    if (res.ok) {
      links.value = await res.json()
    }
  } catch (e) {
    console.error('Failed to load links:', e)
  }
}

async function addLink() {
  if (!newName.value || !newUrl.value) return alert('Name and URL are required')
  
  const newLink = {
    name: newName.value,
    url: newUrl.value,
    icon: newIcon.value || '🔗'
  }

  const updatedLinks = [...links.value, newLink]
  const contentBase64 = btoa(unescape(encodeURIComponent(JSON.stringify(updatedLinks, null, 2))))
  
  try {
    // 1. Get current file SHA
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

    // 2. Update file
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
  <div class="go-page-container">
    <!-- Beautiful Background matching the Bio and Hub -->
    <div class="go-page-bg"></div>
    <div class="go-page-overlay"></div>

    <div class="go-page">
      <!-- Hub Navigation Buttons (Top Right) -->
      <div class="hub-nav">
        <a href="https://home.akari.nx.kg" class="hub-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          Hub
        </a>
        <a href="/notes/" class="hub-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
          Notes
        </a>
      </div>

      <div class="go-header">
        <div class="go-icon-wrapper">🚀</div>
        <h1>Go Links</h1>
        <p>Your beautiful personal bookmarks, accessible anywhere.</p>
      </div>

      <div class="links-grid">
        <a v-for="link in links" :key="link.url" :href="link.url" target="_blank" class="link-card">
          <div class="link-icon">{{ link.icon }}</div>
          <div class="link-info">
            <span class="link-name">{{ link.name }}</span>
            <span class="link-url">{{ link.url.replace(/^https?:\/\//,'').replace(/\/$/, '') }}</span>
          </div>
          <div class="link-arrow">
             <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
          </div>
        </a>

        <!-- Admin Add Button -->
        <button v-if="isAdmin" class="link-card add-btn" @click="showAddModal = true">
          <div class="link-icon add-icon">➕</div>
          <div class="link-info">
            <span class="link-name">Add New Link</span>
            <span class="link-url">Admin Mode Active</span>
          </div>
        </button>
      </div>

      <!-- Add Link Modal -->
      <transition name="fade">
        <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
          <div class="modal">
            <h2>Add Quick Link</h2>
            <div class="form-group">
              <label>Icon (Emoji)</label>
              <input v-model="newIcon" type="text" placeholder="🔗" />
            </div>
            <div class="form-group">
              <label>Name</label>
              <input v-model="newName" type="text" placeholder="e.g. My Repo" />
            </div>
            <div class="form-group">
              <label>URL</label>
              <input v-model="newUrl" type="url" placeholder="https://..." />
            </div>
            <div class="modal-actions">
              <button @click="showAddModal = false" class="btn-cancel">Cancel</button>
              <button @click="addLink" class="btn-save">Save to GitHub</button>
            </div>
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.go-page-container {
  position: relative;
  min-height: 100vh;
  width: 100vw;
  overflow-x: hidden;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.go-page-bg {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('/bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -2;
}

.go-page-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(30,30,46,0.5) 0%, rgba(17,17,27,0.85) 100%);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  z-index: -1;
}

.go-page {
  max-width: 900px;
  margin: 0 auto;
  padding: 80px 20px 80px;
  position: relative;
  z-index: 10;
}

/* Nav */
.hub-nav {
  position: absolute;
  top: 24px;
  right: 24px;
  display: flex;
  gap: 16px;
  z-index: 100;
}

.hub-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(30, 30, 46, 0.4);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #cdd6f4;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}

.hub-btn:hover {
  background: rgba(203, 166, 247, 0.2);
  border-color: rgba(203, 166, 247, 0.5);
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(203, 166, 247, 0.15);
}

/* Header */
.go-header {
  text-align: center;
  margin-bottom: 60px;
  animation: fadeInDown 0.8s ease-out;
}

.go-icon-wrapper {
  font-size: 3rem;
  margin-bottom: 16px;
  display: inline-block;
  background: rgba(255,255,255,0.05);
  padding: 16px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.1);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

.go-header h1 {
  font-size: 3rem;
  font-weight: 800;
  background: linear-gradient(135deg, #cba6f7, #f38ba8, #fab387);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 12px;
  letter-spacing: -0.02em;
}

.go-header p {
  font-size: 1.1rem;
  color: #a6adc8;
  max-width: 500px;
  margin: 0 auto;
  line-height: 1.5;
}

/* Grid */
.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 20px;
}

@media (max-width: 768px) {
  .links-grid {
    grid-template-columns: 1fr;
  }
}

.link-card {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  background: rgba(30, 30, 46, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  text-decoration: none;
  color: #cdd6f4;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  animation: fadeInUp 0.6s ease-out backwards;
}

/* Stagger animation */
.link-card:nth-child(1) { animation-delay: 0.05s; }
.link-card:nth-child(2) { animation-delay: 0.1s; }
.link-card:nth-child(3) { animation-delay: 0.15s; }
.link-card:nth-child(4) { animation-delay: 0.2s; }
.link-card:nth-child(5) { animation-delay: 0.25s; }
.link-card:nth-child(6) { animation-delay: 0.3s; }
.link-card:nth-child(7) { animation-delay: 0.35s; }
.link-card:nth-child(8) { animation-delay: 0.4s; }

.link-card:hover {
  transform: translateY(-4px) scale(1.02);
  background: rgba(49, 50, 68, 0.6);
  border-color: rgba(203, 166, 247, 0.4);
  box-shadow: 0 12px 24px rgba(203, 166, 247, 0.15);
}

.link-icon {
  font-size: 2rem;
  margin-right: 20px;
  width: 54px;
  height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 14px;
  border: 1px solid rgba(255,255,255,0.05);
  flex-shrink: 0;
}

.link-info {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow: hidden;
  text-align: left;
}

.link-name {
  font-weight: 700;
  font-size: 1.15rem;
  color: #cdd6f4;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.link-url {
  font-size: 0.85rem;
  color: #a6adc8;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: 0.8;
}

.link-arrow {
  margin-left: 12px;
  color: #a6adc8;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.link-card:hover .link-arrow {
  opacity: 1;
  transform: translateX(0);
  color: #cba6f7;
}

/* Admin Add Button */
.add-btn {
  background: rgba(203, 166, 247, 0.05);
  border: 2px dashed rgba(203, 166, 247, 0.3);
  cursor: pointer;
  width: 100%;
}
.add-btn:hover {
  background: rgba(203, 166, 247, 0.15);
  border-style: solid;
}
.add-icon {
  background: transparent;
  border: none;
}

/* Animations */
@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
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

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
