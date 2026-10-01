<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { showLinks, githubToken, isAdmin } from './store.js'

const links = ref([])
const showAddModal = ref(false)
const showEditModal = ref(false)
const newName = ref('')
const newUrl = ref('')
const editingIndex = ref(-1)

// Context menu state
const contextMenu = ref({
  show: false,
  x: 0,
  y: 0,
  link: null,
  index: -1
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

function openAddModal() {
  if (!githubToken.value) {
    const token = prompt('Enter Admin Token to Add Link:')
    if (token) {
      localStorage.setItem('gh_admin_token', token)
      githubToken.value = token
      isAdmin.value = true
      newName.value = ''
      newUrl.value = ''
      showAddModal.value = true
    }
  } else {
    newName.value = ''
    newUrl.value = ''
    showAddModal.value = true
  }
}

async function addLink() {
  if (!newName.value || !newUrl.value) return alert('Name and URL are required')
  
  const updatedLinks = [...links.value, { name: newName.value, url: newUrl.value }]
  const success = await saveLinksToGithub(updatedLinks, `Add link ${newName.value}`)
  
  if (success) {
    showAddModal.value = false
  }
}

function verifyAdminToken() {
  if (!githubToken.value) {
    const token = prompt('Nhập Admin Token để chỉnh sửa/xóa liên kết:')
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

function openContextMenu(event, link, index) {
  // Chỉ bung menu Sửa/Xóa nếu đã là Admin (đã có Token)
  if (!isAdmin.value) return
  
  event.preventDefault()
  contextMenu.value = {
    show: true,
    x: event.clientX,
    y: event.clientY,
    link,
    index
  }
}

function closeContextMenu() {
  contextMenu.value.show = false
}

function openEditModal() {
  if (!verifyAdminToken()) {
    closeContextMenu()
    return
  }
  const { link, index } = contextMenu.value
  newName.value = link.name
  newUrl.value = link.url
  editingIndex.value = index
  closeContextMenu()
  showEditModal.value = true
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

async function deleteLink() {
  if (!verifyAdminToken()) {
    closeContextMenu()
    return
  }
  const { link, index } = contextMenu.value
  if (confirm(`Bạn có chắc muốn xóa liên kết "${link.name}" không?`)) {
    const updatedLinks = [...links.value]
    updatedLinks.splice(index, 1)
    await saveLinksToGithub(updatedLinks, `Delete link ${link.name}`)
  }
  closeContextMenu()
}

onMounted(() => {
  fetchLinks()
  window.addEventListener('click', closeContextMenu)
  window.addEventListener('contextmenu', (e) => {
    // Close custom context menu if clicked outside
    if (contextMenu.value.show) {
      closeContextMenu()
    }
  })
})

onUnmounted(() => {
  window.removeEventListener('click', closeContextMenu)
})
</script>

<template>
  <div class="bookmarks-section" v-if="showLinks && links.length > 0">
    <div class="bento-grid">
      <a v-for="(link, index) in links" :key="link.url" :href="link.url" target="_blank" class="bento-card" @contextmenu.prevent="openContextMenu($event, link, index)">
        <img :src="`https://www.google.com/s2/favicons?domain=${link.url}&sz=128`" :alt="link.name" class="bento-icon-img" />
        <span class="bento-name">{{ link.name }}</span>
      </a>
      <button class="bento-card add-btn" @click="openAddModal" title="Thêm liên kết" style="min-width: 0; width: 48px; height: 48px; padding: 0; justify-content: center; border-radius: 50%;">
        <span class="bento-icon-img add-icon">➕</span>
      </button>
    </div>

    <!-- Context Menu -->
    <ClientOnly>
      <Teleport to="body">
        <div v-if="contextMenu.show" class="context-menu" :style="{ top: contextMenu.y + 'px', left: contextMenu.x + 'px' }" @click.stop>
          <div class="context-menu-item" @click="openEditModal">Sửa liên kết</div>
          <div class="context-menu-item delete" @click="deleteLink">Xóa liên kết</div>
        </div>
      </Teleport>
    </ClientOnly>

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
                <button @click="addLink" class="btn-save">Lưu Liên kết</button>
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

/* Context Menu */
.context-menu {
  position: fixed;
  background: rgba(30, 30, 46, 0.95);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  padding: 4px 0;
  z-index: 10001;
  min-width: 150px;
}

.context-menu-item {
  padding: 10px 16px;
  cursor: pointer;
  color: #cdd6f4;
  font-size: 0.9rem;
  transition: background 0.2s;
}

.context-menu-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

.context-menu-item.delete {
  color: #f38ba8;
}

.context-menu-item.delete:hover {
  background: rgba(243, 139, 168, 0.15);
}
</style>
