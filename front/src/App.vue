<!-- App.vue -->
<script setup>
import { RouterView } from 'vue-router';
</script>

<template>
  <div class="root-container">
    <RouterView />
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  min-height: 100vh; /* Ensures it expands */
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  background-color: rgb(17, 24, 39);
  color: white;
}


.root-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

#app {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>