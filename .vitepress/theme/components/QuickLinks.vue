<script setup>
import { ref, onMounted } from 'vue'
import { showLinks, githubToken, isAdmin } from './store.js'

const links = ref([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const isEditMode = ref(false)

const newName = ref('')
const newUrl = ref('')
const editingIndex = ref(-1)

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

async function saveLinksToGithub(updatedLinks, commitMessage) {
  if (!githubToken.value) {
    return alert('Admin token is required')
  }

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
        message: commitMessage,
        content: btoa(unescape(encodeURIComponent(JSON.stringify(updatedLinks, null, 2)))),
        sha: fileData.sha
      })
    })

    if (res.ok) {
      links.value = updatedLinks
      return true
    } else {
      const errorData = await res.json()
      alert('Failed to save links: ' + errorData.message)
      return false
    }
  } catch (e) {
    console.error(e)
    alert('Error saving links. See console.')
    return false
  }
}

function verifyAdminToken() {
  if (!githubToken.value) {
    const token = prompt('Nhập Admin Token (Github PAT) để thao tác:')
    if (token) {
      localStorage.setItem('gh_admin_token', token)
      githubToken.value = token
      isAdmin.value = true
      return true
    }
    return false
  }
  return true
}

function toggleEditMode() {
  if (!isEditMode.value) {
    if (!verifyAdminToken()) return
  }
  isEditMode.value = !isEditMode.value
}

function openAddModal() {
  if (!verifyAdminToken()) return
  newName.value = ''
  newUrl.value = ''
  showAddModal.value = true
}

async function addLink() {
  if (!newName.value || !newUrl.value) return alert('Name and URL are required')
  
  const updatedLinks = [...links.value, { name: newName.value, url: newUrl.value }]
  const success = await saveLinksToGithub(updatedLinks, `Add link ${newName.value}`)
  
  if (success) {
    showAddModal.value = false
  }
}

function handleLinkClick(event, link, index) {
  if (isEditMode.value) {
    event.preventDefault()
    newName.value = link.name
    newUrl.value = link.url
    editingIndex.value = index
    showEditModal.value = true
  }
}

async function editLink() {
  if (!newName.value || !newUrl.value) return alert('Name and URL are required')
  
  const updatedLinks = [...links.value]
  updatedLinks[editingIndex.value] = { name: newName.value, url: newUrl.value }
  
  const success = await saveLinksToGithub(updatedLinks, `Edit link ${newName.value}`)
  if (success) {
    showEditModal.value = false
  }
}

async function deleteLink(index, linkName) {
  if (confirm(`Bạn có chắc muốn xóa liên kết "${linkName}" không?`)) {
    const updatedLinks = [...links.value]
    updatedLinks.splice(index, 1)
    await saveLinksToGithub(updatedLinks, `Delete link ${linkName}`)
  }
}

onMounted(() => {
  fetchLinks()
})
</script>

<template>
  <div class="bookmarks-section" v-if="showLinks && (links.length > 0 || isEditMode)">
    <div class="bento-grid">
      <!-- Quick Links -->
      <div v-for="(link, index) in links" :key="link.url" class="bento-wrapper">
        <a :href="link.url" :target="isEditMode ? '_self' : '_blank'" class="bento-card" :class="{ 'edit-mode-active': isEditMode }" @click="handleLinkClick($event, link, index)">
          <img :src="`https://www.google.com/s2/favicons?domain=${link.url}&sz=128`" :alt="link.name" class="bento-icon-img" />
          <span class="bento-name">{{ link.name }}</span>
        </a>
        
        <!-- Delete Button (Only in Edit Mode) -->
        <button v-if="isEditMode" class="delete-badge" @click.stop="deleteLink(index, link.name)" title="Xóa">
          ✕
        </button>
      </div>

      <!-- Action Buttons -->
      <button class="bento-card action-btn" @click="openAddModal" title="Thêm liên kết">
        <span class="bento-icon-img add-icon">➕</span>
      </button>
      
      <button class="bento-card action-btn" :class="{ 'active': isEditMode }" @click="toggleEditMode" :title="isEditMode ? 'Hoàn tất' : 'Chỉnh sửa liên kết'">
        <span class="bento-icon-img add-icon">{{ isEditMode ? '✅' : '✏️' }}</span>
      </button>
    </div>

    <!-- Modals -->
    <ClientOnly>
      <Teleport to="body">
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
                <button @click="showAddModal = false" class="btn-cancel">Hủy</button>
                <button @click="addLink" class="btn-save">Thêm Mới</button>
              </div>
            </div>
          </div>
        </transition>
        
        <transition name="fade">
          <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
            <div class="modal">
              <h2>Sửa liên kết</h2>
              <div class="form-group">
                <label style="display:block; margin-bottom: 8px; color: #a6adc8; font-size: 0.9rem;">Tên web</label>
                <input v-model="newName" type="text" placeholder="VD: Github" />
              </div>
              <div class="form-group">
                <label style="display:block; margin-bottom: 8px; color: #a6adc8; font-size: 0.9rem;">URL</label>
                <input v-model="newUrl" type="url" placeholder="https://..." />
              </div>
              <div class="modal-actions" style="display:flex; justify-content:flex-end; gap: 12px; margin-top: 24px;">
                <button @click="showEditModal = false" class="btn-cancel">Hủy</button>
                <button @click="editLink" class="btn-save">Cập nhật</button>
              </div>
            </div>
          </div>
        </transition>
      </Teleport>
    </ClientOnly>
  </div>
</template>

<style scoped>
.bento-wrapper {
  position: relative;
  display: inline-block;
}

.bento-card.edit-mode-active {
  animation: jiggle 0.3s infinite alternate;
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(0, 0, 0, 0.7);
  cursor: pointer;
}

.bento-card.edit-mode-active:hover {
  transform: none; /* Disable lift effect in edit mode */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.delete-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  width: 20px;
  height: 20px;
  background: #f38ba8;
  color: white;
  border: none;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
  cursor: pointer;
  z-index: 10;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3);
  padding: 0;
  transition: transform 0.2s;
}

.delete-badge:hover {
  transform: scale(1.15);
  background: #ff5e83;
}

@keyframes jiggle {
  0% { transform: rotate(-1deg); }
  100% { transform: rotate(1deg); }
}

.action-btn {
  min-width: 0; 
  width: 48px; 
  height: 48px; 
  padding: 0; 
  justify-content: center; 
  border-radius: 50%;
}

.action-btn.active {
  background: rgba(0, 122, 255, 0.4);
  border-color: rgba(0, 122, 255, 0.8);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10000;
}

.modal {
  background: rgba(17, 17, 27, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
  border-radius: 16px;
  padding: 32px;
  width: 90%;
  max-width: 400px;
  color: #cdd6f4;
}

.modal h2 {
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 1.5rem;
  font-weight: 700;
  text-align: center;
  color: #fff;
}

.form-group {
  margin-bottom: 16px;
}

.form-group input {
  width: 100%;
  padding: 12px 16px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  outline: none;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: rgba(255, 255, 255, 0.3);
  background: rgba(0, 0, 0, 0.7);
}

.btn-cancel {
  padding: 10px 20px;
  background: rgba(255,255,255,0.05);
  border: none;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  font-weight: 600;
  transition: opacity 0.2s;
}

.btn-cancel:hover {
  background: rgba(255,255,255,0.1);
}

.btn-save {
  padding: 10px 20px;
  background: #007aff;
  border: none;
  border-radius: 8px;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-save:hover {
  opacity: 0.9;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
