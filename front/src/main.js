import './assets/main.css'
import 'leaflet/dist/leaflet.css'

import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(router);
app.use(Toast);


app.mount('#app')
