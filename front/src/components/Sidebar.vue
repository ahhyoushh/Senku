<template>
  <div class="sidebar-container" :class="{ 'sidebar-open': isOpen }">
    <div class="sidebar-backdrop" @click="toggleSidebar" v-if="isOpen"></div>
    
    <div class="sidebar" :class="{ 'sidebar-open': isOpen }">
      <button class="sidebar-toggle" @click="toggleSidebar" :class="{ 'sidebar-open': isOpen }">
        <span class="toggle-icon">{{ isOpen ? '←' : '→' }}</span>
      </button>
      
      <div class="sidebar-header">
        <h2>Submit Item</h2>
      </div>
      
      <div class="sidebar-content">
        <form @submit.prevent="handleSubmit" class="item-form">
          <div class="form-group">
            <label for="itemName">Item Name</label>
            <input type="text" id="itemName" v-model="formData.itemName" required class="form-input" />
          </div>

          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input type="checkbox" v-model="formData.refurbishable" />
              <span class="checkbox-text">Item can be refurbished</span>
            </label>
          </div>

          <div class="form-group">
            <label for="itemCount">Item Count</label>
            <input type="number" id="itemCount" v-model="formData.itemCount" min="1" required class="form-input" />
          </div>

          <div class="form-group">
            <label>Coordinates</label>
            <div class="coordinates-display">
              {{ coordinates ? `[${coordinates[0].toFixed(4)}, ${coordinates[1].toFixed(4)}]` : 'Click on map to set location' }}
            </div>
          </div>

          <div class="submit-button-container">
            <button 
              type="submit" 
              class="submit-button" 
              :disabled="!coordinates || isSubmitting"
              :class="{ 'is-loading': isSubmitting }"
            >
              <span v-if="!isSubmitting">Submit Item</span>
              <span v-else class="loading-spinner"></span>
            </button>
          </div>
        </form>
        
        <slot></slot>
      
        <div class="navigation-links">
          <a href="/dashboard" class="dashboard-link">Go to Dashboard</a>
          <a href="/login" class="login-link">Login</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue';
import { useToast } from 'vue-toastification';

const userData = JSON.parse(localStorage.getItem('username'));
const props = defineProps({ coordinates: { type: Array, default: null } });
const isOpen = ref(false);
const isSubmitting = ref(false);
const formData = ref({ 
  userId: userData?.uid || '', 
  userEmail: userData?.email,
  itemName: '', 
  refurbishable: false, 
  itemCount: 1 
});

const toast = useToast();

const toggleSidebar = () => { 
  isOpen.value = !isOpen.value; 
};

const handleSubmit = async () => {
  if (isSubmitting.value) return;
  
  isSubmitting.value = true;
  try {
    const dataToSend = { ...formData.value, userCoordinates: props.coordinates };
    const response = await fetch('http://localhost:8080/list-item', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dataToSend)
    });
    
    if (!response.ok) throw new Error('Network response was not ok');
    
    formData.value = { 
      userId: userData?.uid || '', 
      userEmail: userData?.email, 
      itemName: 'apple iphone', 
      refurbishable: false, 
      itemCount: 1 
    };
    toast.success('Item submitted successfully!');
  } catch (error) {
    console.error('Error:', error);
    toast.error('Error submitting item. Please try again.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

.sidebar-container {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  pointer-events: none;
  z-index: 1000;
}

.sidebar-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(3px);
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: auto;
}

.sidebar-open .sidebar-backdrop {
  opacity: 1;
}

.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 360px;
  background-color: #1a1a1a;
  color: #ffffff;
  box-shadow: 0 0 30px rgba(0, 0, 0, 0.5);
  transform: translateX(-100%);
  transition: transform 0.3s ease;
  pointer-events: auto;
  display: flex;
  flex-direction: column;
  font-family: 'Inter', sans-serif;
}

.sidebar-open .sidebar {
  transform: translateX(0);
}

.sidebar-toggle {
  position: absolute;
  left: calc(100% - 10px);
  top: 20px;
  width: 36px;
  height: 36px;
  background-color: #4CAF50;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s ease, left 0.3s ease;
  z-index: 1100;
}

.sidebar-toggle.sidebar-open {
  left: calc(100% - 50px);
}

.sidebar-toggle:hover {
  background-color: #45a049;
}

.toggle-icon {
  font-size: 16px;
  line-height: 1;
}

.sidebar-header {
  padding: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  background-color: rgba(0, 0, 0, 0.2);
}

.sidebar-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 500;
  color: #fff;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
  font-size: 13px;
}

.checkbox-group {
  margin: 12px 0;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-text {
  margin-left: 8px;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.9);
}

.form-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  background-color: rgba(255, 255, 255, 0.03);
  color: #fff;
  font-size: 13px;
  transition: all 0.2s ease;
}

.form-input:focus {
  outline: none;
  border-color: #4CAF50;
  background-color: rgba(255, 255, 255, 0.05);
}

.coordinates-display {
  padding: 8px 12px;
  background-color: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  font-family: 'Monaco', 'Consolas', monospace;
  color: rgba(255, 255, 255, 0.9);
  font-size: 13px;
}

.submit-button-container {
  margin: 24px 0 40px;
  display: flex;
  justify-content: flex-start;
}

.submit-button {
  width: auto;
  min-width: 120px;
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.submit-button.is-loading {
  background-color: #45a049;
  color: transparent;
}

.loading-spinner {
  width: 15px;
  height: 15px;
  border: 2px solid #ffffff;
  border-radius: 50%;
  border-top-color: transparent;
  position: absolute;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.submit-button:hover:not(:disabled) {
  min-width: 120px;
  background-color: #45a049;
  transform: translateY(-1px);
}

.submit-button:disabled {
  background-color: #555;
  cursor: not-allowed;
  opacity: 0.7;
}

.navigation-links {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding: 12px 0;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.dashboard-link {
  display: inline-block;
  color: #4CAF50;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  transition: color 0.2s ease;
}

.dashboard-link:hover {
  color: #45a049;
}

.login-link {
  display: inline-block;
  color: #fff;
  text-decoration: none;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 12px;
  background-color: #333;
  border-radius: 4px;
  transition: all 0.2s ease;
}

.login-link:hover {
  background-color: #444;
}
</style>