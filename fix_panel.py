import re

with open('.vitepress/theme/components/Startpage.vue', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Imports
content = content.replace("import { ref, onMounted } from 'vue'", "import { ref, onMounted, watch } from 'vue'")

# 2. Add showWeather, showLinks
state_add = """
const showWeather = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('showWeather') !== 'false' : true)
const showLinks = ref(typeof localStorage !== 'undefined' ? localStorage.getItem('showLinks') !== 'false' : true)

if (typeof window !== 'undefined') {
  watch(showWeather, (val) => localStorage.setItem('showWeather', val.toString()))
  watch(showLinks, (val) => localStorage.setItem('showLinks', val.toString()))
}
"""
content = content.replace("const newUrl = ref('')", "const newUrl = ref('')\n" + state_add)

# 3. v-if="showWeather"
content = content.replace('<div class="top-left-widget">', '<div v-if="showWeather" class="top-left-widget">')

# 4. v-if="showLinks"
content = content.replace('<div class="bookmarks-section" v-if="links.length > 0">', '<div class="bookmarks-section" v-if="showLinks && links.length > 0">')

# 5. Modal HTML replace
old_modal = """    <!-- Settings / Add Link Modal -->
    <transition name="fade">
      <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
        <div class="modal">
          <h2>Page Settings</h2>
          
          <div class="settings-section">
            <h3>Add Quick Link</h3>
            <div class="form-group">
              <label>Name</label>
              <input v-model="newName" type="text" placeholder="e.g. My Repo" />
            </div>
            <div class="form-group">
              <label>URL</label>
              <input v-model="newUrl" type="url" placeholder="https://..." />
            </div>
          </div>
          
          <div class="modal-actions">
            <button @click="showAddModal = false" class="btn-cancel">Close</button>
            <button @click="addLink" class="btn-save">Add Link</button>
          </div>
        </div>
      </div>
    </transition>"""

new_panel = """    <!-- Edge Style Settings Panel -->
    <transition name="slide-right">
      <div v-if="showAddModal" class="settings-panel">
        <div class="panel-header">
          <h2>Cài đặt trang</h2>
          <button class="close-btn" @click="showAddModal = false">
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

          <div class="settings-section">
            <h3 style="margin-top: 16px; font-size: 0.95rem;">Thêm liên kết (Tùy chỉnh Edge)</h3>
            <div class="form-group">
              <input v-model="newName" type="text" placeholder="Tên web (VD: Github)" />
            </div>
            <div class="form-group">
              <input v-model="newUrl" type="url" placeholder="URL (https://...)" />
            </div>
            <button @click="addLink" class="btn-save" style="width: 100%">Lưu Liên kết</button>
          </div>
        </div>
      </div>
    </transition>"""

content = content.replace(old_modal, new_panel)

# 6. Modal CSS replace
css_start = "/* Modal */"
css_end = ".fade-leave-to {\n  opacity: 0;\n}"
import sys
idx_start = content.find(css_start)
idx_end = content.find(css_end)
if idx_start == -1 or idx_end == -1:
    print("Could not find CSS markers!")
    sys.exit(1)

new_css = """/* Settings Panel (Edge Style) */
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
"""

content = content[:idx_start] + new_css + content[idx_end + len(css_end):]

with open('.vitepress/theme/components/Startpage.vue', 'w', encoding='utf-8') as f:
    f.write(content)

print("Panel updated!")
