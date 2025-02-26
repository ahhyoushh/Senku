<template>
    <div class="flex items-center justify-center h-screen bg-gray-900 text-white">
      <div class="p-6 bg-gray-800 shadow-lg rounded-lg text-center">
        <input v-model="name" type="text" placeholder="Enter name" class="px-3 py-2 border rounded mb-4 bg-gray-700 text-white">
        <button @click="sendVerification" class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">
          Send Verification
        </button>
        <div v-if="success" class="mt-4 text-green-400 text-2xl">
          E-mail sent successfully ✔
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        success: false,
        name: "econnect",
      };
    },
    methods: {
      async sendVerification() {
        try {
          const response = await fetch(`https://senku-1e1b.onrender.com/centers/send-verification`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ Name: this.name || "econnect" }),
          });
          const data = await response.json();
          if (data.message === "Email sent successfully!") {
            this.success = true;
          }
        } catch (error) {
          console.error("Error sending verification:", error);
        }
      },
    },
  };
  </script>
  
  <style>
  body {
    background-color:  rgb(17, 24, 39);
    color: white;
  }
  </style>
  
