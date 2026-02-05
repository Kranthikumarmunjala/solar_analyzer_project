// import './assets/main.css'

// import { createApp } from 'vue'
// import App from './App.vue'

// createApp(App).mount('#app')

// import { createApp } from 'vue'
// import App from './App.vue'

// createApp(App).mount('#app')

import { createApp } from 'vue'
import './style.css' // <--- ADD THIS LINE
import App from './App.vue'
import 'leaflet/dist/leaflet.css' // Ensure Leaflet CSS is imported here

createApp(App).mount('#app')