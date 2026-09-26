<script setup>
import { ref, onMounted } from 'vue'
import { showLinks, githubToken, isAdmin } from './store.js'

const links = ref([])
const showAddModal = ref(false)
const newName = ref('')
const newUrl = ref('')

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

function openAddModal() {
  if (!githubToken.value) {
    const token = prompt('Enter Admin Token to Add Link:')
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
  
  if (!githubToken.value) {
    return alert('Admin token is required')
  }

  const updatedLinks = [...links.value, { name: newName.value, url: newUrl.value }]
  
  try {
    const fileRes = await fetch('https://api.github.com/repos/akari310/personal-hub/contents/public/links.json', {
      headers: { Authorization: `token ${githubToken.value}` }
    })
    const fileData = await fileRes.json()

    const res = await fetch('https://api.github.com/repos/akari310/personal-hub/contents/public/links.json', {
      method: 'PUT',
      headers: {
        Authorization: `token ${githubToken.value}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: `Add link ${newName.value}`,
        content: btoa(unescape(encodeURIComponent(JSON.stringify(updatedLinks, null, 2)))),
        sha: fileData.sha
      })
    })

    if (res.ok) {
      links.value = updatedLinks
      newName.value = ''
      newUrl.value = ''
      showAddModal.value = false
    } else {
      const errorData = await res.json()
      alert('Failed to add link: ' + errorData.message)
    }
  } catch (e) {
    console.error(e)
    alert('Error adding link. See console.')
  }
}

onMounted(() => {
  fetchLinks()
})
</script>

<template>
  <div class="bookmarks-section" v-if="showLinks && links.length > 0">
    <div class="bento-grid">
      <a v-for="link in links" :key="link.url" :href="link.url" target="_blank" class="bento-card">
        <img :src="`https://www.google.com/s2/favicons?domain=${link.url}&sz=128`" :alt="link.name" class="bento-icon-img" />
        <span class="bento-name">{{ link.name }}</span>
      </a>
      <button class="bento-card add-btn" @click="openAddModal">
        <span class="bento-icon-img add-icon">➕</span>
        <span class="bento-name">Thêm link</span>
      </button>
    </div>

    <!-- Centered Add Link Modal -->
    <transition name="fade">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal">
          <h2>Thêm liên kết mới</h2>
          <div class="form-group">
            <label style="display:block; margin-bottom: 8px; color: #a6adc8; font-size: 0.9rem;">Tên web</label>
            <input v-model="newName" type="text" placeholder="VD: Github" />
          </div>
          <div class="form-group">
            <label style="display:block; margin-bottom: 8px; color: #a6adc8; font-size: 0.9rem;">URL</label>
            <input v-model="newUrl" type="url" placeholder="https://..." />
          </div>
          <div class="modal-actions" style="display:flex; justify-content:flex-end; gap: 12px; margin-top: 24px;">
            <button @click="showAddModal = false" class="btn-cancel" style="padding: 10px 20px; background: rgba(255,255,255,0.05); border: none; border-radius: 8px; color: #fff; cursor: pointer;">Hủy</button>
            <button @click="addLink" class="btn-save">Lưu Liên kết</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>
