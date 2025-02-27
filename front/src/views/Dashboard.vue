<script setup>
import { ref, onMounted, computed } from "vue";
import { Trash2, RefreshCw, MapPin, Phone, Mail, Package, Info } from 'lucide-vue-next';

const userId = ref(null);
const items = ref([]);
const loading = ref(true);
const errorMessage = ref("");
const searchQuery = ref("");
const selectedFilter = ref("all");
const isRefreshing = ref(false);

// Computed properties for filtered items
const filteredItems = computed(() => {
  let filtered = items.value;
  
  // Filter by status
  if (selectedFilter.value === "listed") {
    filtered = filtered.filter(item => item.status === "Listed");
  } else if (selectedFilter.value === "unlisted") {
    filtered = filtered.filter(item => item.status !== "Listed");
  }
  
  // Filter by search query
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(item => 
      item.itemName.toLowerCase().includes(query) ||
      item.metadata.brand.toLowerCase().includes(query) ||
      item.metadata.EEE.toLowerCase().includes(query)
    );
  }
  
  return filtered;
});

const stats = computed(() => {
  const total = items.value.length;
  const listed = items.value.filter(item => item.status === "Listed").length;
  const refurbishable = items.value.filter(item => item.refurbishable).length;
  
  return { total, listed, refurbishable };
});

async function fetchItems() {
  // Retrieve UserId from localStorage
  const userData = JSON.parse(localStorage.getItem("username"));
  if (!userData) {
    errorMessage.value = "User not logged in.";
    loading.value = false;
    return;
  }

  userId.value = userData.uid;
  try {
    const response = await fetch(
      `https://senku-1e1b.onrender.com/get-items?UserId=${userId.value}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId: userId.value })
      }
    );

    if (!response.ok) throw new Error("Failed to fetch data");
    items.value = await response.json();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
  }
}

function refreshData() {
  isRefreshing.value = true;
  loading.value = true;
  errorMessage.value = "";
  
  fetchItems().finally(() => {
    setTimeout(() => {
      isRefreshing.value = false;
    }, 600); // Animation duration
  });
}

onMounted(fetchItems);
</script>

<template>
  <div class="dashboard-container">
   <button @click="$router.push('/')">Home</button>
    <div class="items-container">
      <div class="items-content">
        <!-- Header with Stats -->
        <header class="dashboard-header">
          <div class="header-content">
            <h1 class="text-2xl font-bold text-white">Your Recycling Dashboard</h1>
            <p class="text-gray-400">Manage and track your electronic items</p>
          </div>
          
          <button @click="refreshData" class="refresh-button" :class="{'refreshing': isRefreshing}">
            <RefreshCw :size="18" />
            <span>Refresh</span>
          </button>
        </header>
        
        <!-- Stats Cards -->
        <div class="stats-container" v-if="!loading && !errorMessage">
          <div class="stat-card">
            <div class="stat-icon total-icon">
              <Package :size="22" />
            </div>
            <div class="stat-content">
              <h3>Total Items</h3>
              <p>{{ stats.total }}</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon listed-icon">
              <Info :size="22" />
            </div>
            <div class="stat-content">
              <h3>Listed</h3>
              <p>{{ stats.listed }}</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon refurb-icon">
              <RefreshCw :size="22" />
            </div>
            <div class="stat-content">
              <h3>Refurbishable</h3>
              <p>{{ stats.refurbishable }}</p>
            </div>
          </div>
        </div>

        <!-- Search and Filters -->
        <div class="controls-container" v-if="!loading && items.length">
          <div class="search-container">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Search items..."
              class="search-input"
            />
          </div>
          
          <div class="filter-container">
            <select v-model="selectedFilter" class="filter-select">
              <option value="all">All Items</option>
              <option value="listed">Listed Only</option>
              <option value="unlisted">Unlisted Only</option>
            </select>
          </div>
        </div>

        <!-- Loading and Error States -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading your items...</p>
        </div>
        
        <div v-if="errorMessage" class="error-container">
          <p>{{ errorMessage }}</p>
          <button @click="refreshData" class="retry-button">Try Again</button>
        </div>

        <!-- Items List -->
        <div v-if="!loading && !errorMessage" class="items-list">
          <div v-if="filteredItems.length === 0" class="no-results">
            <p>No items found matching your criteria.</p>
          </div>
          
          <div v-for="item in filteredItems" :key="item.itemId" class="item-card">
            <!-- Status Badge -->
            <div class="status-badge" :class="item.status === 'Listed' ? 'status-listed' : 'status-unlisted'">
              {{ item.status }}
            </div>
            
            <!-- Item Header -->
            <div class="item-header">
              <div class="item-info">
                <h2>{{ item.itemName }}</h2>
                <div class="item-meta">
                  <span class="category-tag">{{ item.metadata.EEE }}</span>
                  <span class="metadata-pill">
                    <span class="metadata-label">Brand:</span> 
                    {{ item.metadata.brand }}
                  </span>
                  <span class="metadata-pill">
                    <span class="metadata-label">Weight:</span> 
                    {{ item.metadata.weight }} kg
                  </span>
                </div>
              </div>

              <!-- Refurbishable Status -->
              <div class="refurbish-container">
                <div
                  class="refurbish-indicator"
                  :class="item.refurbishable ? 'refurbishable' : 'not-refurbishable'"
                >
                  <span class="refurbish-label">{{ item.refurbishable ? 'Refurbishable' : 'Not Refurbishable' }}</span>
                </div>
              </div>
            </div>

            <!-- Nearest Center Info -->
            <div class="center-container">
              <h3 class="center-title">
                <MapPin :size="16" />
                Nearest Recycling Center
              </h3>
              
              <div class="center-content">
                <div class="center-header">
                  <span class="center-name">{{ item.nearest_center.Name }}</span>
                  <span class="center-type">{{ item.nearest_center.Type }}</span>
                </div>
                
                <address class="center-address">
                  {{ item.nearest_center.Address }}
                </address>
                
                <div class="center-contact">
                  <div class="contact-item">
                    <Phone :size="14" />
                    <span>{{ item.nearest_center["Contact Number"] }}</span>
                  </div>
                  <div class="contact-item">
                    <Mail :size="14" />
                    <span>{{ item.nearest_center["Email Address"] }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap");

.dashboard-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  color: white;
  font-family: "Poppins", sans-serif;
  display: flex;
  justify-content: center;
  padding: 2rem 1rem;
}

.items-container {
  width: 100%;
  display: flex;
  justify-content: center;
}

.items-content {
  width: 100%;
  max-width: 960px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* Header Styles */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.header-content h1 {
  margin-bottom: 0.25rem;
}

.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.refreshing {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Stats Cards */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-card {
  background: rgba(31, 41, 55, 0.6);
  border-radius: 12px;
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 12px;
}

.total-icon {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.listed-icon {
  background: linear-gradient(135deg, #10b981, #047857);
}

.refurb-icon {
  background: linear-gradient(135deg, #f59e0b, #b45309);
}

.stat-content h3 {
  font-size: 0.9rem;
  color: #94a3b8;
  margin-bottom: 0.25rem;
}

.stat-content p {
  font-size: 1.5rem;
  font-weight: 600;
}

/* Search and Filters */
.controls-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.search-container {
  flex-grow: 1;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(31, 41, 55, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: white;
  font-family: inherit;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.filter-select {
  padding: 0.75rem 1rem;
  background: rgba(31, 41, 55, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  color: white;
  font-family: inherit;
  cursor: pointer;
}

/* Loading and Error States */
.loading-container, .error-container, .no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: rgba(31, 41, 55, 0.6);
  border-radius: 12px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

/* Item Cards */
.items-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.item-card {
  position: relative;
  background: linear-gradient(145deg, #1f2937, #111827);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  overflow: hidden;
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.status-badge {
  position: absolute;
  top: 0;
  right: 1.5rem;
  padding: 0.25rem 0.75rem;
  border-radius: 0 0 6px 6px;
  font-size: 0.8rem;
  font-weight: 500;
}

.status-listed {
  background-color: #059669;
}

.status-unlisted {
  background-color: #6b7280;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.item-info {
  flex-grow: 1;
}

.item-info h2 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #f9fafb;
}

.item-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  align-items: center;
}

.category-tag {
  background: rgba(37, 99, 235, 0.2);
  color: #93c5fd;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.metadata-pill {
  background: rgba(255, 255, 255, 0.08);
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  color: #d1d5db;
}

.metadata-label {
  color: #9ca3af;
  margin-right: 0.25rem;
}

.refurbish-container {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.refurbish-indicator {
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.refurbishable {
  background-color: rgba(16, 185, 129, 0.2);
  color: #6ee7b7;
}

.not-refurbishable {
  background-color: rgba(239, 68, 68, 0.2);
  color: #fca5a5;
}

.refurbish-label {
  white-space: nowrap;
}

/* Center Information */
.center-container {
  background: rgba(31, 41, 55, 0.6);
  border-radius: 10px;
  overflow: hidden;
}

.center-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: rgba(16, 185, 129, 0.2);
  color: #6ee7b7;
  font-size: 0.95rem;
  font-weight: 500;
}

.center-content {
  padding: 1rem;
}

.center-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.center-name {
  font-weight: 600;
  color: #f9fafb;
}

.center-type {
  font-size: 0.8rem;
  padding: 0.2rem 0.5rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
  color: #d1d5db;
}

.center-address {
  color: #9ca3af;
  font-style: normal;
  margin-bottom: 0.75rem;
  font-size: 0.9rem;
  line-height: 1.5;
}

.center-contact {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #d1d5db;
  font-size: 0.9rem;
}

/* Animations */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.item-card {
  animation: fadeIn 0.3s ease-in-out;
}

/* Media Queries */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .controls-container {
    flex-direction: column;
  }
  
  .item-header {
    flex-direction: column;
  }
  
  .refurbish-container {
    width: 100%;
    justify-content: flex-start;
    margin-top: 0.5rem;
  }
}
</style>