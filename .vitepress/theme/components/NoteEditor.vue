<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useData } from 'vitepress'

const { page } = useData()
const showEditor = ref(false)
const markdownContent = ref('')
const isLoading = ref(false)
const githubToken = ref(typeof window !== 'undefined' ? localStorage.getItem('gh_admin_token') || '' : '')
let currentSha = null

async function handleShortcut(e) {
  // Phím tắt Ctrl + Shift + E để bật tắt khung chỉnh sửa
  if (e.ctrlKey && e.shiftKey && e.key.toLowerCase() === 'e') {
    e.preventDefault()
    if (!showEditor.value) {
      await openEditor()
    } else {
      showEditor.value = false
    }
  }
}

async function openEditor() {
  if (!githubToken.value) {
    const token = prompt('Nhập Github Admin Token để cấp quyền sửa Note:')
    if (token) {
      localStorage.setItem('gh_admin_token', token)
      githubToken.value = token
    } else {
      return
    }
  }

  const relativePath = page.value.relativePath
  if (!relativePath) {
    alert('Không thể xác định file hiện tại!')
    return
  }

  isLoading.value = true
  showEditor.value = true

  try {
    const res = await fetch(`https://api.github.com/repos/akari310/personal-hub/contents/${relativePath}`, {
      headers: { Authorization: `token ${githubToken.value}` },
      cache: 'no-store'
    })
    
    if (res.ok) {
      const data = await res.json()
      currentSha = data.sha
      // Xử lý Unicode chuẩn xác để không bị lỗi tiếng Việt
      markdownContent.value = decodeURIComponent(escape(atob(data.content)))
    } else {
      alert('Không thể tải nội dung file từ Github.')
      showEditor.value = false
    }
  } catch (error) {
    console.error(error)
    alert('Lỗi khi tải file.')
    showEditor.value = false
  } finally {
    isLoading.value = false
  }
}

async function saveNote() {
  if (!markdownContent.value) return
  isLoading.value = true
  
  const relativePath = page.value.relativePath

  try {
    const res = await fetch(`https://api.github.com/repos/akari310/personal-hub/contents/${relativePath}`, {
      method: 'PUT',
      headers: {
        Authorization: `token ${githubToken.value}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: `Update note: ${relativePath}`,
        content: btoa(unescape(encodeURIComponent(markdownContent.value))),
        sha: currentSha
      })
    })

    if (res.ok) {
      const data = await res.json()
      currentSha = data.content.sha
      alert('Đã lưu siêu tốc lên Github! Vui lòng đợi khoảng 1 phút cho máy chủ Cloudflare Build xong, sau đó F5 để thấy bài viết mới.')
      showEditor.value = false
    } else {
      const errorData = await res.json()
      alert('Lỗi lưu file: ' + errorData.message)
    }
  } catch (error) {
    console.error(error)
    alert('Lỗi khi lưu file.')
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleShortcut)
})
onUnmounted(() => {
  window.removeEventListener('keydown', handleShortcut)
})
</script>

<template>
  <ClientOnly>
    <Teleport to="body">
      <div v-if="showEditor" class="note-editor-overlay">
        <div class="note-editor-container">
          <div class="editor-header">
            <div class="title-group">
              <span class="pulse-icon">✏️</span>
              <h3>Đang sửa: {{ page.relativePath }}</h3>
            </div>
            <div class="editor-actions">
              <button class="btn cancel" @click="showEditor = false" :disabled="isLoading">Hủy</button>
              <button class="btn save" @click="saveNote" :disabled="isLoading">
                {{ isLoading ? 'Đang lưu lên mây...' : 'Lưu lại' }}
              </button>
            </div>
          </div>
          <div class="editor-body">
            <textarea v-model="markdownContent" :disabled="isLoading" spellcheck="false" placeholder="Nhập mã Markdown vào đây..."></textarea>
          </div>
        </div>
      </div>
    </Teleport>
  </ClientOnly>
</template>

<style scoped>
.note-editor-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(17, 17, 27, 0.95);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  z-index: 100000;
  display: flex;
  align-items: center;
  justify-content: center;
}
.note-editor-container {
  width: 95%;
  max-width: 1300px;
  height: 90vh;
  background: #1e1e2e;
  border-radius: 12px;
  border: 1px solid rgba(255,255,255,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 20px 50px rgba(0,0,0,0.6);
  animation: slideUp 0.3s cubic-bezier(0.25, 1, 0.5, 1);
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
.editor-header {
  padding: 16px 24px;
  background: #181825;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.title-group {
  display: flex;
  align-items: center;
  gap: 12px;
}
.pulse-icon {
  animation: pulse 2s infinite;
}
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}
.editor-header h3 {
  margin: 0;
  color: #cdd6f4;
  font-size: 1.1rem;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
}
.editor-actions {
  display: flex;
  gap: 12px;
}
.btn {
  padding: 8px 20px;
  border-radius: 8px;
  border: none;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s;
}
.btn:hover { transform: translateY(-1px); opacity: 0.9; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
.btn:active { transform: translateY(1px); }
.btn:disabled { opacity: 0.5; cursor: not-allowed; transform: none; box-shadow: none; }
.btn.cancel { background: rgba(255,255,255,0.1); color: #fff; }
.btn.save { background: #0078d4; color: #fff; }

.editor-body {
  flex: 1;
  display: flex;
}
.editor-body textarea {
  flex: 1;
  width: 100%;
  padding: 32px;
  background: transparent;
  border: none;
  color: #cdd6f4;
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 1.1rem;
  line-height: 1.7;
  resize: none;
  outline: none;
}
</style>
