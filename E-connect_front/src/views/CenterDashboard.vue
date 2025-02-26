<script setup>
import { ref, onMounted } from "vue";

const centerId = ref(null);
const items = ref([]);
const loading = ref(true);
const errorMessage = ref("");

const deleteItem = async (itemId) => {
  try {
    const response = await fetch(
      `http://localhost:8080/centers/delete-item`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ itemId })
      }
    );

    if (!response.ok) throw new Error("Failed to delete item");
    
    // Remove the item from the local state
    items.value = items.value.filter(item => item.itemId !== itemId);
  } catch (error) {
    errorMessage.value = `Failed to delete item: ${error.message}`;
  }
};

const approveItem = async (itemId) => {
  try {
    const response = await fetch(
      `http://localhost:8080/centers/approve`,
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

onMounted(async () => {
  // Retrieve centerId from localStorage
  const storedCenterId = localStorage.getItem("centerId");
  console.log(storedCenterId);

  if (!storedCenterId) {
    errorMessage.value = "User not logged in.";
    loading.value = false;
    return;
  }

  centerId.value = storedCenterId;

  try {
    const response = await fetch(
      `http://localhost:8080/centers/get-items`,
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
  }
});
</script>

<template>
  <div class="dashboard-container">
    <div class="items-container">
      <div class="items-content">
        <h1 class="text-2xl font-bold text-white mb-6 pt-6">Your items</h1>

        <p v-if="loading" class="text-gray-400">Loading items...</p>
        <p v-if="errorMessage" class="text-red-400">{{ errorMessage }}</p>

        <div v-if="items.length" class="space-y-4">
          <div 
            v-for="item in items" 
            :key="item.itemId" 
            class="item-card"
          >
            <!-- Item Header -->
            <div class="item-header">
              <div class="item-info">
                <h2>{{ item.itemName }} ({{ item.metadata?.EEE }})</h2>
                <p>Brand: {{ item.metadata?.brand }} </p>
              </div>

              <div class="status-actions">
                <!-- Refurbish Status Box -->
                <div
                  class="refurbish-box"
                  :class="item.refurbishable ? 'refurbish-yes' : 'refurbish-no'"
                ></div>
                <!-- Approve Button -->
                <button 
                  v-if="item.status !== 'Approved'"
                  @click="approveItem(item.itemId)"
                  class="action-btn approve-btn"
                  title="Approve item"
                >
                  ✓
                </button>
                <!-- Delete Button -->
                <button 
                  @click="deleteItem(item.itemId)"
                  class="action-btn delete-btn"
                  title="Delete item"
                >
                  ×
                </button>
              </div>
            </div>

            <!-- Item Details -->
            <div class="item-details">
              <h3 class="text-md font-bold text-green-400">Item Details:</h3>
              <p class="text-sm text-white">EEE code: {{ item.metadata?.EEE }}</p>
              <p class="text-sm text-white">Weight: {{ item.metadata?.weight }} kg</p>
              <p class="text-sm text-white">Lifespan: {{ item.metadata?.lifespan }} years</p>
              <p class="text-sm" :class="item.status === 'Approved' ? 'text-green-400' : 'text-yellow-400'">
                Status: {{ item.status }}
              </p>
            </div>
          </div>
        </div>

        <p v-else-if="!loading" class="text-gray-400">No items found.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap");

.dashboard-container {
  min-height: 100vh;
  width: 100%;
  background: linear-gradient(135deg, rgb(17, 24, 39), rgb(30, 41, 59));
  color: white;
  padding-top: 2rem;
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
  max-width: 900px;
  padding: 0 1rem;
}

.item-card {
  background: linear-gradient(145deg, #1f2937, #111827);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: transform 0.2s, box-shadow 0.2s;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
}

.item-card:hover {
  transform: scale(1.02);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.5);
}

.item-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.item-info {
  text-align: center;
  flex-grow: 1;
}

.item-info h2 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
}

.item-info p {
  font-size: 0.9rem;
  color: rgb(156, 163, 175);
}

.status-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.refurbish-box {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.refurbish-yes {
  background-color: #10b981;
}

.refurbish-no {
  background-color: #ef4444;
}

.action-btn {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 18px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.approve-btn {
  background-color: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.approve-btn:hover {
  background-color: rgba(16, 185, 129, 0.3);
  transform: scale(1.1);
}

.delete-btn {
  background-color: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.delete-btn:hover {
  background-color: rgba(239, 68, 68, 0.3);
  transform: scale(1.1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>