<script setup>
import { ref, onMounted } from "vue";

const userId = ref(null);
const items = ref([]);
const loading = ref(true);
const errorMessage = ref("");

onMounted(async () => {
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
});
</script>

<template>
  <div class="dashboard-container">
   <button @click="$router.push('/')">Home</button>
    <div class="items-container">
      <div class="items-content">
        <h1 class="text-2xl font-bold text-white mb-6 pt-6">Your Items</h1>

        <p v-if="loading" class="text-gray-400">Loading items...</p>
        <p v-if="errorMessage" class="text-red-400">{{ errorMessage }}</p>

        <div v-if="items.length" class="space-y-4">
          <div v-for="item in items.filter(item => item.status === 'Listed')" :key="item.itemId" class="item-card">
            <!-- Item Header -->
            <div class="item-header">
              <div class="item-info">
                <h2>{{ item.itemName }} ({{ item.metadata.EEE }})</h2>
                <p>Brand: {{ item.metadata.brand }}  | Weight: {{ item.metadata.weight }} kg</p>
              </div>

              <!-- Small Square Box Instead of Text -->
              <div
                class="refurbish-box"
                :class="item.refurbishable ? 'refurbish-yes' : 'refurbish-no'"
              ></div>
            </div>

            <!-- Nearest Center Info (Now Below) -->
            <div class="nearest-center">
              <h3 class="text-md font-bold text-green-400">Nearest Center:</h3>
              <p class="text-sm text-white">
                <span class="font-semibold">{{ item.nearest_center.Name }}</span> - {{ item.nearest_center.Type }}
              </p>
              <p class="text-sm text-gray-400">{{ item.nearest_center.Address }}</p>
              <p class="text-sm text-blue-400">📞 {{ item.nearest_center["Contact Number"] }}</p>
              <p class="text-sm text-gray-400">📧 {{ item.nearest_center["Email Address"] }}</p>
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

/* Item Card */
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
/* Centered Item Info */
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

/* Refurbishable Status Box */
.refurbish-box {
  width: 16px;
  height: 16px;
  border-radius: 4px;
}

.refurbish-yes {
  background-color: #10b981; /* Green */
}


.refurbish-no {
  background-color: #ef4444; /* Red */
}
/* Nearest Center Below */
.nearest-center {
  background: rgba(31, 41, 55, 0.8);
  border-left: 4px solid #10b981;
  border-radius: 10px;
  padding: 1rem;
}

.nearest-center:hover {
  background: rgba(31, 41, 55, 1);
}


/* Fade-in Animation */
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
