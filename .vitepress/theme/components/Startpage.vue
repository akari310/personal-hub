<script setup>
import { ref, onMounted } from 'vue'
import SearchBar from './SearchBar.vue'

onMounted(() => {
  // Thông minh chuyển hướng dựa trên tên miền hiện tại
  const host = window.location.hostname
  const path = window.location.pathname
  
  if (host.startsWith('note') && path === '/') {
    window.location.href = 'https://note.akari.nx.kg/notes/'
  } else if (host.startsWith('go') && path === '/') {
    window.location.href = 'https://go.akari.nx.kg/go/'
  }
})
</script>

<template>
  <div class="startpage-overlay">
    <div class="search-container">
      <SearchBar />
    </div>

    <!-- Hub Navigation Buttons (Top Right) -->
    <div class="hub-nav">
      <a href="https://note.akari.nx.kg" class="hub-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20"/></svg>
        Notes
      </a>
      <a href="https://go.akari.nx.kg" class="hub-btn">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>
        Go Links
      </a>
    </div>
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
  /* Move search bar up to match Edge (about 25-30% from the top) */
  padding-top: 25vh;
  z-index: 9999;
}

.search-container {
  width: 100%;
  max-width: 650px;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
  gap: 24px;
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
  padding: 12px 24px;
  background-color: rgba(30, 30, 46, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  color: #cdd6f4;
  font-weight: 600;
  font-size: 1rem;
  text-decoration: none;
  transition: all 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.hub-btn:hover {
  background-color: rgba(203, 166, 247, 0.2);
  border-color: #cba6f7;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(203, 166, 247, 0.2);
}
</style>
