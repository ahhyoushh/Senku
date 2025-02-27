import './assets/main.css'
import 'leaflet/dist/leaflet.css'

import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './registerServiceWorker'
import { register } from 'register-service-worker';

if (process.env.NODE_ENV === 'production') {
  register('/service-worker.js', {
    ready() {
      console.log('PWA is ready.');
    },
    registered() {
      console.log('Service worker registered.');
    },
    updated() {
      console.log('New content available, refresh needed.');
    }
  });
}

const app = createApp(App)

app.use(router);
app.use(Toast);


app.mount('#app')
