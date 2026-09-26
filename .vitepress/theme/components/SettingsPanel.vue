<script setup>
import { showSettingsPanel, showWeather, showLinks } from './store.js'
</script>

<template>
  <transition name="slide-right">
    <div v-if="showSettingsPanel" class="settings-panel">
      <div class="panel-header">
        <h2>Cài đặt trang</h2>
        <button class="close-btn" @click="showSettingsPanel = false">
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
      </div>
    </div>
  </transition>
</template>
