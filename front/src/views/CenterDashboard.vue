<script setup>
import { ref, computed, onMounted } from "vue";
import { CheckCircle, X, RefreshCw, Package, Filter, ArrowUp, ArrowDown, AlertTriangle, Trash2 } from 'lucide-vue-next';

// State management
const centerId = ref(null);
const items = ref([]);
const loading = ref(true);
const errorMessage = ref("");
const isRefreshing = ref(false);
const searchQuery = ref("");
const sortField = ref("itemName");
const sortDirection = ref("asc");
const filterStatus = ref("all");
const confirmDelete = ref(null);

// Computed properties
const filteredItems = computed(() => {
  let result = [...items.value];
  
  // Apply search filter
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(item => 
      (item.itemName?.toLowerCase().includes(query)) || 
      (item.metadata?.EEE?.toLowerCase().includes(query)) ||
      (item.metadata?.brand?.toLowerCase().includes(query))
    );
  }
  
  // Apply status filter
  if (filterStatus.value !== "all") {
    result = result.filter(item => item.status === filterStatus.value);
  }
  
  // Apply sorting
  result.sort((a, b) => {
    let valA, valB;
    
    if (sortField.value === "itemName") {
      valA = a.itemName || "";
      valB = b.itemName || "";
    } else if (sortField.value === "status") {
      valA = a.status || "";
      valB = b.status || "";
    } else if (sortField.value === "weight") {
      valA = parseFloat(a.metadata?.weight || 0);
      valB = parseFloat(b.metadata?.weight || 0);
    } else if (sortField.value === "lifespan") {
      valA = parseFloat(a.metadata?.lifespan || 0);
      valB = parseFloat(b.metadata?.lifespan || 0);
    }
    
    // Handle string comparison
    if (typeof valA === 'string' && typeof valB === 'string') {
      return sortDirection.value === 'asc' 
        ? valA.localeCompare(valB) 
        : valB.localeCompare(valA);
    }
    
    // Handle numeric comparison
    return sortDirection.value === 'asc' 
      ? valA - valB 
      : valB - valA;
  });
  
  return result;
});

const statusCounts = computed(() => {
  const counts = {
    total: items.value.length,
    pending: items.value.filter(item => item.status !== 'Approved').length,
    approved: items.value.filter(item => item.status === 'Approved').length,
    refurbishable: items.value.filter(item => item.refurbishable).length
  };
  return counts;
});

// Methods
const toggleSort = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDirection.value = 'asc';
  }
};

const deleteItem = async (itemId) => {
  if (confirmDelete.value === itemId) {
    try {
      const response = await fetch(
        `https://senku-1e1b.onrender.com/centers/delete-item`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ itemId })
        }
      );

      if (!response.ok) throw new Error("Failed to delete item");
      
      // Remove the item from the local state
      items.value = items.value.filter(item => item.itemId !== itemId);
      confirmDelete.value = null;
    } catch (error) {
      errorMessage.value = `Failed to delete item: ${error.message}`;
    }
  } else {
    // First click - ask for confirmation
    confirmDelete.value = itemId;
    
    // Auto-reset confirmation after 5 seconds
    setTimeout(() => {
      if (confirmDelete.value === itemId) {
        confirmDelete.value = null;
      }
    }, 5000);
  }
};

const approveItem = async (itemId) => {
  try {
    const response = await fetch(
      `https://senku-1e1b.onrender.com/centers/approve`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ itemId })
      }
    );

    if (!response.ok) throw new Error("Failed to approve item");
    
    // Update the item's status in the local state
    const item = items.value.find(item => item.itemId === itemId);
    if (item) {
      item.status = "Approved";
    }
  } catch (error) {
    errorMessage.value = `Failed to approve item: ${error.message}`;
  }
};

const refreshData = async () => {
  if (isRefreshing.value) return;
  
  errorMessage.value = "";
  isRefreshing.value = true;
  loading.value = true;
  
  try {
    const response = await fetch(
      `https://senku-1e1b.onrender.com/centers/get-items`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ centerId: centerId.value })
      }
    );

    if (!response.ok) throw new Error("Failed to fetch data");
    items.value = await response.json();
  } catch (error) {
    errorMessage.value = error.message;
  } finally {
    loading.value = false;
    setTimeout(() => {
      isRefreshing.value = false;
    }, 500);
  }
};

onMounted(async () => {
  // Retrieve centerId from localStorage
  const storedCenterId = localStorage.getItem("centerId");

  if (!storedCenterId) {
    errorMessage.value = "User not logged in.";
    loading.value = false;
    return;
  }

  centerId.value = storedCenterId;
  await refreshData();
});
</script>

<template>
  <div class="dashboard-container">
    <div class="items-container">
      <div class="items-content">
        <!-- Header with stats -->
        <header class="dashboard-header">
          <div class="header-content">
            <h1 class="text-2xl font-bold text-white">Recycling Center Dashboard</h1>
            <p class="text-gray-400">Manage and process incoming recycling items</p>
          </div>
          
          <button @click="refreshData" class="refresh-button" :class="{'refreshing': isRefreshing}" :disabled="isRefreshing">
            <RefreshCw size="18" />
            <span>Refresh</span>
          </button>
        </header>
        
        <!-- Stats overview -->
        <div class="stats-container" v-if="!loading && !errorMessage && items.length">
          <div class="stat-card">
            <div class="stat-icon total-icon">
              <Package size="20" />
            </div>
            <div class="stat-content">
              <h3>Total Items</h3>
              <p>{{ statusCounts.total }}</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon pending-icon">
              <AlertTriangle size="20" />
            </div>
            <div class="stat-content">
              <h3>Pending Approval</h3>
              <p>{{ statusCounts.pending }}</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon approved-icon">
              <CheckCircle size="20" />
            </div>
            <div class="stat-content">
              <h3>Approved</h3>
              <p>{{ statusCounts.approved }}</p>
            </div>
          </div>
          
          <div class="stat-card">
            <div class="stat-icon refurb-icon">
              <RefreshCw size="20" />
            </div>
            <div class="stat-content">
              <h3>Refurbishable</h3>
              <p>{{ statusCounts.refurbishable }}</p>
            </div>
          </div>
        </div>
        
        <!-- Search and filters -->
        <div class="controls-container" v-if="!loading && items.length">
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Search by name, brand, or EEE code..."
              class="search-input"
            />
          </div>
          
          <div class="filter-box">
            <Filter size="16" />
            <select v-model="filterStatus" class="filter-select">
              <option value="all">All Statuses</option>
              <option value="Pending">Pending</option>
              <option value="Approved">Approved</option>
            </select>
          </div>
        </div>
        
        <!-- Loading and error states -->
        <div v-if="loading" class="loading-container">
          <div class="loading-spinner"></div>
          <p>Loading items...</p>
        </div>
        
        <div v-if="errorMessage" class="error-container">
          <div class="error-icon">!</div>
          <p>{{ errorMessage }}</p>
          <button @click="refreshData" class="retry-button">
            <RefreshCw size="14" />
            <span>Try Again</span>
          </button>
        </div>
        
        <!-- Empty state -->
        <div v-if="!loading && !errorMessage && items.length === 0" class="empty-container">
          <div class="empty-icon">
            <Package size="40" />
          </div>
          <h2>No Items Found</h2>
          <p>There are currently no recycling items in your center.</p>
          <button @click="refreshData" class="refresh-button">
            <RefreshCw size="16" />
            <span>Refresh</span>
          </button>
        </div>
        
        <!-- Sort bar -->
        <div class="sort-bar" v-if="!loading && !errorMessage && filteredItems.length > 0">
          <div class="sort-container">
            <span class="sort-label">Sort by:</span>
            
            <button 
              @click="toggleSort('itemName')" 
              class="sort-button" 
              :class="{ 'sort-active': sortField === 'itemName' }"
            >
              Name
              <ArrowUp v-if="sortField === 'itemName' && sortDirection === 'asc'" size="14" />
              <ArrowDown v-if="sortField === 'itemName' && sortDirection === 'desc'" size="14" />
            </button>
            
            <button 
              @click="toggleSort('status')" 
              class="sort-button" 
              :class="{ 'sort-active': sortField === 'status' }"
            >
              Status
              <ArrowUp v-if="sortField === 'status' && sortDirection === 'asc'" size="14" />
              <ArrowDown v-if="sortField === 'status' && sortDirection === 'desc'" size="14" />
            </button>
            
            <button 
              @click="toggleSort('weight')" 
              class="sort-button" 
              :class="{ 'sort-active': sortField === 'weight' }"
            >
              Weight
              <ArrowUp v-if="sortField === 'weight' && sortDirection === 'asc'" size="14" />
              <ArrowDown v-if="sortField === 'weight' && sortDirection === 'desc'" size="14" />
            </button>
            
            <button 
              @click="toggleSort('lifespan')" 
              class="sort-button" 
              :class="{ 'sort-active': sortField === 'lifespan' }"
            >
              Lifespan
              <ArrowUp v-if="sortField === 'lifespan' && sortDirection === 'asc'" size="14" />
              <ArrowDown v-if="sortField === 'lifespan' && sortDirection === 'desc'" size="14" />
            </button>
          </div>
          
          <div class="results-count">
            {{ filteredItems.length }} item{{ filteredItems.length !== 1 ? 's' : '' }}
          </div>
        </div>
        
        <!-- Items list -->
        <div v-if="!loading && !errorMessage && filteredItems.length > 0" class="items-list">
          <div 
            v-for="item in filteredItems" 
            :key="item.itemId" 
            class="item-card"
            :class="{'approved-item': item.status === 'Approved'}"
          >
            <!-- Status badge -->
            <div 
              class="status-badge" 
              :class="item.status === 'Approved' ? 'status-approved' : 'status-pending'"
            >
              {{ item.status }}
            </div>
            
            <!-- Item Header -->
            <div class="item-header">
              <div class="item-info">
                <h2>{{ item.itemName || 'Unnamed Item' }}</h2>
                <div class="item-meta">
                  <span class="metadata-tag">{{ item.metadata?.EEE || 'No EEE' }}</span>
                  <span class="metadata-pill">Brand: {{ item.metadata?.brand || 'Unknown' }}</span>
                </div>
              </div>

              <div class="status-actions">
                <!-- Refurbish Status Box with tooltip -->
                <div class="refurbish-status">
                  <div
                    class="refurbish-box"
                    :class="item.refurbishable ? 'refurbish-yes' : 'refurbish-no'"
                  ></div>
                  <span class="refurbish-tooltip">{{ item.refurbishable ? 'Refurbishable' : 'Not Refurbishable' }}</span>
                </div>
                
                <!-- Approve Button -->
                <button 
                  v-if="item.status !== 'Approved'"
                  @click="approveItem(item.itemId)"
                  class="action-btn approve-btn"
                  title="Approve item"
                >
                  <CheckCircle size="16" />
                </button>
                
                <!-- Delete Button -->
                <button 
                  @click="deleteItem(item.itemId)"
                  class="action-btn delete-btn"
                  :class="{'confirm-delete': confirmDelete === item.itemId}"
                  :title="confirmDelete === item.itemId ? 'Click again to confirm deletion' : 'Delete item'"
                >
                  <Trash2 v-if="confirmDelete !== item.itemId" size="16" />
                  <X v-else size="16" />
                </button>
              </div>
            </div>

            <!-- Item Details -->
            <div class="item-details">
              <div class="details-grid">
                <div class="detail-item">
                  <span class="detail-label">EEE Code</span>
                  <span class="detail-value">{{ item.metadata?.EEE || 'N/A' }}</span>
                </div>
                
                <div class="detail-item">
                  <span class="detail-label">Weight</span>
                  <span class="detail-value">{{ item.metadata?.weight || '0' }} kg</span>
                </div>
                
                <div class="detail-item">
                  <span class="detail-label">Lifespan</span>
                  <span class="detail-value">{{ item.metadata?.lifespan || '0' }} years</span>
                </div>
                
                <div class="detail-item">
                  <span class="detail-label">Status</span>
                  <span class="detail-value status-text" :class="item.status === 'Approved' ? 'text-green-400' : 'text-yellow-400'">
                    {{ item.status }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- No search results -->
        <div v-if="!loading && !errorMessage && items.length > 0 && filteredItems.length === 0" class="no-results">
          <p>No items match your search criteria.</p>
          <button @click="searchQuery = ''; filterStatus = 'all'" class="clear-button">
            Clear Filters
          </button>
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
  background: linear-gradient(135deg, rgb(17, 24, 39), rgb(30, 41, 59));
  color: white;
  padding: 2rem 1rem;
  display: flex;
  justify-content: center;
  font-family: "Poppins", sans-serif;
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

.refresh-button:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.2);
}

.refresh-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.refreshing {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Stats Container */
.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
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

.pending-icon {
  background: linear-gradient(135deg, #f59e0b, #b45309);
}

.approved-icon {
  background: linear-gradient(135deg, #10b981, #047857);
}

.refurb-icon {
  background: linear-gradient(135deg, #8b5cf6, #6d28d9);
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
}

.search-box {
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

.filter-box {
  display: flex;
  align-items: center;
  background: rgba(31, 41, 55, 0.6);
  padding: 0 0.75rem;
  border-radius: 6px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  gap: 0.5rem;
}

.filter-select {
  background: transparent;
  border: none;
  color: white;
  padding: 0.75rem 0.5rem;
  font-family: inherit;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
}

/* Sort bar */
.sort-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background: rgba(31, 41, 55, 0.6);
  border-radius: 6px;
}

.sort-container {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.sort-label {
  color: #94a3b8;
  font-size: 0.9rem;
}

.sort-button {
  background: transparent;
  border: none;
  color: white;
  padding: 0.25rem 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.sort-button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.sort-active {
  background: rgba(59, 130, 246, 0.2);
  color: #93c5fd;
}

.results-count {
  color: #94a3b8;
  font-size: 0.9rem;
}

/* Loading and Error States */
.loading-container, .error-container, .empty-container, .no-results {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  background: rgba(31, 41, 55, 0.6);
  border-radius: 12px;
  text-align: center;
  gap: 1rem;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s linear infinite;
}

.error-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
  font-size: 24px;
  font-weight: bold;
}

.empty-icon {
  color: #94a3b8;
  margin-bottom: 1rem;
}

.retry-button, .clear-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
}

.retry-button:hover, .clear-button:hover {
  background: #2563eb;
}

/* Items List */
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
  animation: fadeIn 0.3s ease-out;
}

.item-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
}

.approved-item {
  border-left: 4px solid #10b981;
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

.status-approved {
  background: #10b981;
}

.status-pending {
  background: #f59e0b;
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
  gap: 0.5rem;
  align-items: center;
}

.metadata-tag {
  background: rgba(59, 130, 246, 0.2);
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

.status-actions {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.refurbish-status {
  position: relative;
  display: inline-block;
}

.refurbish-box {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  cursor: pointer;
}

.refurbish-tooltip {
  visibility: hidden;
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.8);
  color: white;
  text-align: center;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  z-index: 1;
  white-space: nowrap;
  font-size: 0.8rem;
  opacity: 0;
  transition: opacity 0.3s;
  pointer-events: none;
  margin-top: 5px;
}

.refurbish-status:hover .refurbish-tooltip {
  visibility: visible;
  opacity: 1;
}

.refurbish-yes {
  background-color: #10b981;
}

.refurbish-no {
  background-color: #ef4444;
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  cursor: pointer;
  transition: all 0.2s;
}

.approve-btn {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.approve-btn:hover {
  background: rgba(16, 185, 129, 0.3);
  transform: scale(1.05);
}

.delete-btn {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.delete-btn:hover {
  background: rgba(239, 68, 68, 0.3);
  transform: scale(1.05);
}

.confirm-delete {
  background: #ef4444;
  color: white;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.1); }
  100% { transform: scale(1); }
}

/* Item Details */
.item-details {
  background: rgba(31, 41, 55, 0.5);
  border-radius: 8px;
  padding: 1rem;
  margin-top: 0.5rem;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-label {
  font-size: 0.8rem;
  color: #94a3b8;
  font-weight: 500;
}

.detail-value {
  font-size: 1rem;
  color: #e5e7eb;
  font-weight: 500;
}

.status-text {
  font-weight: 600;
}

.text-green-400 {
  color: #4ade80;
}

.text-yellow-400 {
  color: #facc15;
}

/* Animation keyframes */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

/* Media queries for responsive design */
@media (max-width: 768px) {
  .stats-container {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .item-header {
    flex-direction: column;
  }
  
  .status-actions {
    align-self: flex-end;
    margin-top: 0.5rem;
  }
  
  .details-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 480px) {
  .stats-container {
    grid-template-columns: 1fr;
  }
  
  .controls-container {
    flex-direction: column;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .sort-container {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .results-count {
    display: none;
  }
}

</style>