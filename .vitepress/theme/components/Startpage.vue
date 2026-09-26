<script setup>
import SearchBar from './SearchBar.vue'
import ClockWeather from './ClockWeather.vue'
import TopNav from './TopNav.vue'
import SettingsPanel from './SettingsPanel.vue'
import QuickLinks from './QuickLinks.vue'
</script>

<template>
  <div class="startpage-overlay">
    <TopNav />
    <ClockWeather />
    
    <div class="content-wrapper">
      <div class="search-section">
        <SearchBar />
      </div>
      <QuickLinks />
    </div>
    
    <SettingsPanel />
  </div>
</template>

<style>
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
  background: radial-gradient(circle at center, rgba(30,30,46,0) 0%, rgba(17,17,27,0.4) 100%);
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
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.05);
  border-radius: 100px; /* Pill shape */
  text-decoration: none;
  color: #cdd6f4;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  min-width: 140px;
}

.bento-card:hover {
  transform: translateY(-3px) scale(1.02);
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  color: #fff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.8);
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
  align-items: center;
  gap: 12px;
  z-index: 100;
}

.hub-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 40px;
  padding: 0 18px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 100px;
  color: #cdd6f4;
  font-weight: 600;
  font-size: 0.85rem;
  text-decoration: none;
  transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  box-sizing: border-box;
}

.hub-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #fff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.8);
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
  height: 40px;
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
  height: 40px;
  box-sizing: border-box;
  padding: 0 12px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 100px;
  text-decoration: none;
  color: #cdd6f4;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.weather-widget:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  color: #fff;
  text-shadow: 0 1px 4px rgba(0,0,0,0.8);
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

/* Settings Panel (Edge Style) */
.settings-panel {
  position: fixed;
  top: 72px;
  right: 16px;
  width: 320px;
  background: rgba(36, 36, 36, 0.85);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.5);
  color: #fff;
  z-index: 10000;
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.panel-header h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 600;
}

.close-btn {
  background: transparent;
  border: none;
  color: #a6adc8;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.close-btn:hover { background: rgba(255,255,255,0.1); color: #fff; }

.panel-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

/* Toggle Switch */
.toggle-switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 22px;
}
.toggle-switch input { opacity: 0; width: 0; height: 0; }
.slider {
  position: absolute;
  cursor: pointer;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(255,255,255,0.2);
  transition: .3s;
  border-radius: 22px;
}
.slider:before {
  position: absolute;
  content: "";
  height: 16px;
  width: 16px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
  border-radius: 50%;
}
input:checked + .slider { background-color: #0078d4; }
input:checked + .slider:before { transform: translateX(18px); }

.slide-right-enter-active, .slide-right-leave-active { transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1); }
.slide-right-enter-from, .slide-right-leave-to { opacity: 0; transform: translateX(20px); }

.form-group {
  margin-bottom: 12px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  background: rgba(0,0,0,0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  color: #fff;
  outline: none;
  font-size: 0.9rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.form-group input:focus {
  border-color: #0078d4;
}

.btn-save {
  padding: 10px 24px;
  background: #0078d4;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn-save:hover {
  opacity: 0.9;
}

</style>