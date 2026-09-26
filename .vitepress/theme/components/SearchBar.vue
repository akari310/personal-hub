<script setup>
import { ref } from 'vue'

const query = ref('')

const handleSearch = () => {
  const q = query.value.trim().toLowerCase()
  if (!q) return

  // Danh sách các lối tắt (shortcuts) sang mạng xã hội/web phổ biến
  const shortcuts = [
    'github', 'gh', 
    'ytb', 'yt', 'youtube', 
    'ytm', 
    'fb', 'face', 'facebook', 
    'ig', 'insta', 'instagram', 
    'tw', 'x', 'twitter', 
    'msg', 'messenger', 
    'rd', 'reddit', 
    'gpt', 'chatgpt'
  ]

  // Nếu người dùng nhập chuẩn 1 trong các từ khóa trên
  if (shortcuts.includes(q)) {
    // Chuyển hướng sang subdomain go để nó xử lý
    window.location.href = `https://go.akari.nx.kg/${q}`
    return
  }

  // Nếu không phải lối tắt thì tìm kiếm bằng Google
  window.location.href = 'https://www.google.com/search?q=' + encodeURIComponent(query.value.trim())
}
</script>

<template>
  <div class="search-bar">
    <div class="search-icon">
      <svg focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" fill="#9aa0a6"></path></svg>
    </div>
    <input 
      v-model="query" 
      @keyup.enter="handleSearch"
      type="text" 
      placeholder="Tìm kiếm trên web" 
      autofocus
    />
    <div class="mic-icon">
      <svg focusable="false" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="m12 15c1.66 0 3-1.31 3-2.97v-7.02c0-1.66-1.34-3.01-3-3.01s-3 1.34-3 3.01v7.02c0 1.66 1.34 2.97 3 2.97z" fill="#4285f4"></path><path d="m11 18.08h2v3.92h-2z" fill="#34a853"></path><path d="m7.05 16.87c-1.27-1.33-2.05-2.8-2.05-4.67h2c0 1.45.56 2.42 1.47 3.38v.32l-1.15 1.18z" fill="#f4b400"></path><path d="m12 16.93a4.97 4.97 0 0 1 -3.54-1.55l-1.41 1.49c1.26 1.34 3.02 2.13 4.95 2.13 3.87 0 6.99-2.92 6.99-7h-1.99c0 2.92-2.24 4.93-5 4.93z" fill="#ea4335"></path></svg>
    </div>
  </div>
</template>

<style scoped>
.search-bar {
  width: 100%;
  display: flex;
  align-items: center;
  background: #2b2b2b; /* Dark mode background */
  border-radius: 24px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.4);
  padding: 0 14px;
  height: 48px;
  transition: all 0.2s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.search-bar:hover, .search-bar:focus-within {
  background: #333333;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.6);
  border-color: rgba(255, 255, 255, 0.15);
}

.search-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
  width: 20px;
  height: 20px;
}

.search-icon svg {
  width: 100%;
  height: 100%;
}

.mic-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 12px;
  width: 24px;
  height: 24px;
  cursor: pointer;
}

.mic-icon svg {
  width: 100%;
  height: 100%;
}

.search-bar input {
  flex: 1;
  font-size: 16px;
  border: none;
  background: transparent;
  color: #e8eaed; /* Dark mode text */
  outline: none;
  height: 100%;
}

.search-bar input::placeholder {
  color: #9aa0a6; /* Dark mode placeholder */
}
</style>
