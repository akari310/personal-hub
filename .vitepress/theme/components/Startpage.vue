<script setup>
import SearchBar from './SearchBar.vue'
</script>

<template>
  <div class="startpage-overlay">
    <div class="search-container">
      <SearchBar />
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
}
</style>
