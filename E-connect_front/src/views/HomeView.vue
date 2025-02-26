<template>
  <div class="home">
    <div class="map-wrapper">
      <Sidebar :coordinates="selectedCoordinates">
        <!-- Legend and other content -->
        <div class="sidebar-section">
          <div class="legend-item">
            
            <img src="https://i.ibb.co/HTVSvSnx/image-removebg-preview.png" alt="Refurbisher" class="legend-icon" />
            <span>Refurbisher</span>
          </div>
          <div class="legend-item">
            <img src="https://i.ibb.co/Wvr9ndwz/image-removebg-preview-1.png" alt="Recycler" class="legend-icon" />
            <span>Recycler</span>
          </div>
          <div class="legend-item">
            <img src="https://i.ibb.co/RGmkWpZV/image-removebg-preview-2.png" alt="Dismantler" class="legend-icon" />
            <span>Dismantler</span>
          </div>
        </div>
      </Sidebar>
      
      <LeafletMap2 @coordinates-update="updateCoordinates" />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import LeafletMap2 from '@/components/LeafletMap2.vue';
import Sidebar from '@/components/Sidebar.vue';

const selectedCoordinates = ref(null);

const updateCoordinates = (coordinates) => {
  selectedCoordinates.value = coordinates;
};
</script>

  
  <style scoped>
  .home {
    height: 100vh;
    width: 100vw;
    position: relative;
    overflow: hidden;
  }
  
  .map-wrapper {
    height: 100%;
    width: 100%;
    position: relative;
  }
  
  .sidebar-section {
    margin-bottom: 24px;
  }
  
  .sidebar-section h3 {
    margin-bottom: 16px;
    color: #333;
  }
  
  .legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
  }
  
  .legend-icon {
    width: 24px;
    height: 24px;
    margin-right: 12px;
    object-fit: contain;
  }
  </style>