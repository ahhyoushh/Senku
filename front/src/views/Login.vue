<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Welcome</h1>
      <!-- Show user info after login -->
      <div v-if="currentUser" class="user-info">
        <div class="profile-container">
          <img :src="currentUser.photoURL" alt="Profile" class="profile-pic">
        </div>
        <p style="color: black;">Welcome, {{ currentUser.displayName }}</p>
        <p class="email">{{ currentUser.email }}</p>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
      <!-- Login button if not logged in -->
      <div v-else>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <button 
          @click="signInWithGoogle" 
          class="google-btn"
          :disabled="loading"
        >
          <img 
            src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" 
            alt="Google Logo"
          >
          {{ loading ? 'Signing in...' : 'Sign in with Google' }}
        </button>
      </div>
    </div>
    <a href="/" class="home-link">Go to Home</a>
  </div>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: rgb(17, 24, 39);
  flex-direction: column;
  gap: 1rem;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 100%;
  max-width: 400px;
}

.home-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: opacity 0.2s;
}

.home-link:hover {
  opacity: 0.8;
}

.user-info {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-container {
  width: 100%;
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.profile-pic {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
}

.email {
  color: #666;
  margin-bottom: 1rem;
}

.google-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  background: white;
  border: 1px solid #dadce0;
  border-radius: 4px;
  padding: 12px 24px;
  font-size: 16px;
  color: #3c4043;
  cursor: pointer;
  transition: background-color 0.2s;
  width: 100%;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  min-width: 100px;
}

.google-btn:hover {
  background-color: #f8f9fa;
}

.google-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.google-btn img {
  width: 18px;
  height: 18px;
}

.error-message {
  color: #d93025;
  margin-bottom: 1rem;
  font-size: 14px;
}

h1 {
  color: #202124;
  margin-bottom: 1.5rem;
}
</style>

<script setup>
import { ref, provide, onMounted } from 'vue';
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.3.1/firebase-app.js";
import { 
  getAuth, 
  GoogleAuthProvider, 
  signInWithPopup,
  signOut,
  onAuthStateChanged 
} from "https://www.gstatic.com/firebasejs/11.3.1/firebase-auth.js";

const loading = ref(false);
const errorMessage = ref('');
const currentUser = ref(null);
const accessToken = ref(null);

const firebaseConfig = {
  apiKey: "AIzaSyAZRNNUaK82H26vbgC7qFJev0LXUmpBi5A",
  authDomain: "e-connect-f1e2c.firebaseapp.com",
  projectId: "e-connect-f1e2c",
  storageBucket: "e-connect-f1e2c.firebasestorage.app",
  messagingSenderId: "370695789277",
  appId: "1:370695789277:web:50a9b81e8a9fd171fc9934",
  measurementId: "G-F3B7E7XZSG"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

provide("currentUser", currentUser);

onMounted(() => {
  onAuthStateChanged(auth, (user) => {
    currentUser.value = user ? {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL
    } : null;
    provide("currentUser", currentUser);
  });
});

const signInWithGoogle = async () => {
  try {
    loading.value = true;
    errorMessage.value = '';
    
    const result = await signInWithPopup(auth, provider);
    
    const credential = GoogleAuthProvider.credentialFromResult(result);
    accessToken.value = credential.accessToken;
    
    const user = result.user;
    localStorage.setItem('username', JSON.stringify({
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL
    }));
    console.log('User Data:', {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL,
      accessToken: accessToken.value
    });

  } catch (error) {
    console.error('Login error:', error);
    errorMessage.value = error.message || 'An error occurred during sign in';
  } finally {
    loading.value = false;
  }
};

const logout = async () => {
  try {
    await signOut(auth);
    accessToken.value = null;
    localStorage.removeItem('user');
  } catch (error) {
    console.error('Logout error:', error);
  }
};

const sendTokenToBackend = async (token) => {
  try {
    const response = await fetch('YOUR_BACKEND_URL/auth', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ token })
    });
    const data = await response.json();
    console.log('Backend response:', data);
  } catch (error) {
    console.error('Error sending token to backend:', error);
  }
};
</script>