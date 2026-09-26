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
  <div class="go-page">
    <!-- Hub Navigation Buttons (Top Right) -->
    <div class="hub-nav">
      <a href="/" class="hub-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        Hub
      </a>
      <a href="/notes/" class="hub-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
        Notes
      </a>
    </div>

    <div class="go-header">
      <h1>🚀 Go Links</h1>
      <p>Quick access to my favorite spots.</p>
    </div>

    <div class="links-grid">
      <a v-for="link in links" :key="link.url" :href="link.url" target="_blank" class="link-card">
        <span class="link-icon">{{ link.icon }}</span>
        <span class="link-name">{{ link.name }}</span>
      </a>

      <!-- Admin Add Button -->
      <button v-if="isAdmin" class="link-card add-btn" @click="showAddModal = true">
        <span class="link-icon">➕</span>
        <span class="link-name">Add New Link</span>
      </button>
    </div>

    <!-- Add Link Modal -->
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
  </div>
</template>

<style scoped>
.go-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 80px 20px 40px; /* Increased top padding to avoid nav */
  min-height: 100vh;
}

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
  background-color: rgba(30, 30, 46, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #cdd6f4;
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  transition: all 0.2s ease;
}

.hub-btn:hover {
  background-color: rgba(203, 166, 247, 0.2);
  border-color: #cba6f7;
  color: #fff;
  transform: translateY(-2px);
}


.go-header {
  text-align: center;
  margin-bottom: 40px;
}

.go-header h1 {
  font-size: 2.5rem;
  background: -webkit-linear-gradient(45deg, #cba6f7, #89b4fa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 10px;
}

.links-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.link-card {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background-color: rgba(30, 30, 46, 0.7);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  text-decoration: none;
  color: #cdd6f4;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

.link-card:hover {
  transform: translateY(-5px);
  border-color: #cba6f7;
  box-shadow: 0 10px 20px rgba(203, 166, 247, 0.15);
}

.link-icon {
  font-size: 1.8rem;
}

.link-name {
  font-weight: 600;
  font-size: 1.1rem;
}

.add-btn {
  background-color: rgba(203, 166, 247, 0.1);
  border: 1px dashed #cba6f7;
  cursor: pointer;
  color: #cba6f7;
}

.add-btn:hover {
  background-color: rgba(203, 166, 247, 0.2);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(5px);
}

.modal {
  background: #1e1e2e;
  padding: 30px;
  border-radius: 16px;
  width: 100%;
  max-width: 400px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.modal h2 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #cdd6f4;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #a6adc8;
  font-size: 0.9rem;
}

.form-group input {
  width: 100%;
  padding: 10px 12px;
  background: #11111b;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #cdd6f4;
  outline: none;
}

.form-group input:focus {
  border-color: #cba6f7;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 25px;
}

.btn-cancel {
  padding: 8px 16px;
  background: transparent;
  border: none;
  color: #a6adc8;
  cursor: pointer;
}

.btn-save {
  padding: 8px 16px;
  background: #cba6f7;
  color: #11111b;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}
</style>
