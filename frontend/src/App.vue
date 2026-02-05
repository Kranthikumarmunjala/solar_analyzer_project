<template>
  <div class="flex h-screen w-screen bg-gray-50 font-sans overflow-hidden">
    <!-- Sidebar -->
    <div class="w-96 bg-white shadow-2xl z-10 overflow-y-auto border-r border-gray-200 flex flex-col shrink-0">
      <!-- Header -->
      <div class="p-6 bg-gradient-to-r from-blue-700 to-blue-900 text-white sticky top-0 z-20">
        <h1 class="text-2xl font-bold">Solar Site Analyzer</h1>
        <p class="text-xs mt-1 text-blue-100">Best solar locations in Tamil Nadu</p>
      </div>

      <!-- Weights -->
      <div class="p-6 border-b border-gray-100">
        <h2 class="text-sm uppercase tracking-wide text-gray-500 font-bold mb-4">Adjust Weights</h2>
        <div v-for="(val, key) in weights" :key="key" class="mb-4">
          <div class="flex justify-between mb-1">
            <span class="text-sm font-medium text-gray-700 capitalize">{{ key }}</span>
            <span class="text-sm font-bold text-blue-600">{{ val.toFixed(2) }}</span>
          </div>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            v-model.number="weights[key]"
            @input="fetchAnalysis"
            class="w-full h-2 bg-gray-200 rounded-lg cursor-pointer accent-blue-600"
          />
        </div>

        <div
          class="mt-2 p-2 rounded text-center text-xs font-bold border"
          :class="Math.abs(weightSum - 1.0) < 0.01 ? 'bg-green-50 text-green-700 border-green-200' : 'bg-red-50 text-red-700 border-red-200'"
        >
          Total Weight: {{ weightSum.toFixed(2) }} {{ Math.abs(weightSum - 1.0) >= 0.01 ? '(Must be 1.00)' : '✅' }}
        </div>
      </div>

      <!-- Sites List -->
      <div class="p-4 bg-gray-50 flex-1">
        <h2 class="text-sm uppercase tracking-wide text-gray-500 font-bold mb-3 pl-2">Top 10 Recommendations</h2>

        <div v-if="loading" class="text-center text-gray-500 py-10">Loading analysis...</div>
        <div v-else class="space-y-3">
          <div
            v-for="(site, index) in sortedSites.slice(0, 10)"
            :key="site.id"
            class="p-4 rounded-lg bg-white shadow-sm border border-gray-200 hover:shadow-md hover:border-blue-300 transition cursor-pointer group"
            @click="flyToSite(site)"
          >
            <div class="flex justify-between items-start">
              <div>
                <span class="inline-block px-2 py-0.5 rounded text-xs font-bold bg-gray-100 text-gray-600 mb-1">
                  #{{ index + 1 }}
                </span>
                <h3 class="font-bold text-gray-800 leading-tight group-hover:text-blue-600">
                  {{ site.site_name }}
                </h3>
              </div>
              <div class="text-right">
                <span class="block text-2xl font-bold leading-none" :class="getScoreColor(site.total)">
                  {{ site.total.toFixed(0) }}
                </span>
                <span class="text-[10px] text-gray-400 uppercase">Score</span>
              </div>
            </div>
            
            <div class="mt-3 pt-3 border-t border-gray-100 grid grid-cols-2 gap-y-1 gap-x-2 text-xs text-gray-600">
              <div class="flex items-center">
                <span class="w-4">☀️</span> {{ site.solar_irradiance_kwh }} kWh
              </div>
              <div class="flex items-center">
                <span class="w-4">📐</span> {{ (site.area_sqm / 10000).toFixed(1) }} ha
              </div>
              <div class="flex items-center">
                <span class="w-4">⚡</span> {{ site.grid_distance_km }} km
              </div>
              <div class="flex items-center">
                <span class="w-4">🛣️</span> {{ site.road_distance_km }} km
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Map Container -->
    <div class="flex-1 relative h-full bg-gray-200">
      <div id="map" class="absolute inset-0 z-0"></div>
      
      <!-- Legend Overlay -->
      <div class="absolute bottom-6 right-6 z-[1000] bg-white p-3 rounded-lg shadow-lg border border-gray-200 text-xs">
        <div class="font-bold mb-2 text-gray-700">Suitability Score</div>
        <div class="flex items-center mb-1"><span class="w-3 h-3 rounded-full bg-green-500 mr-2"></span> 80 - 100 (Excellent)</div>
        <div class="flex items-center mb-1"><span class="w-3 h-3 rounded-full bg-yellow-500 mr-2"></span> 60 - 79 (Good)</div>
        <div class="flex items-center"><span class="w-3 h-3 rounded-full bg-red-500 mr-2"></span> 0 - 59 (Poor)</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import L from 'leaflet'

// Reactive state
const sites = ref([])
const map = ref(null)
const markers = ref([])
const loading = ref(true)

const weights = ref({
  solar: 0.35,
  area: 0.25,
  grid: 0.20,
  slope: 0.15,
  infrastructure: 0.05,
})

// Computeds
const weightSum = computed(() => {
  const sum = Object.values(weights.value).reduce((a, b) => a + b, 0)
  return parseFloat(sum.toFixed(2))
})

const sortedSites = computed(() => {
  return [...sites.value].sort((a, b) => b.total - a.total)
})

// Lifecycle
onMounted(async () => {
  initMap()
  await fetchAnalysis()
})

const initMap = () => {
  // Center on Tamil Nadu
  map.value = L.map('map').setView([11.1271, 77.3661], 9)
  
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 20
  }).addTo(map.value)
}

const fetchAnalysis = async () => {
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/sites/', { weights: weights.value })
    sites.value = res.data
    updateMarkers()
    loading.value = false
  } catch (err) {
    console.error("API Error:", err)
    loading.value = false
  }
}

const updateMarkers = () => {
  if (!map.value) return

  // Clear existing markers
  markers.value.forEach((m) => map.value.removeLayer(m))
  markers.value = []

  sites.value.forEach((site) => {
    let color = '#ef4444' // red
    if (site.total >= 80) color = '#22c55e' // green
    else if (site.total >= 60) color = '#eab308' // yellow

    // IMPORTANT: Parse strings to floats for Leaflet
    const lat = parseFloat(site.latitude)
    const lng = parseFloat(site.longitude)

    const marker = L.circleMarker([lat, lng], {
      radius: 8,
      fillColor: color,
      color: '#fff',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.9,
    }).addTo(map.value)

    marker.bindPopup(`
      <div class="text-sm">
        <strong class="block text-base mb-1">${site.site_name}</strong>
        <span class="text-gray-600">Score:</span> <strong>${site.total.toFixed(1)}</strong><br>
        <span class="text-gray-600">Solar:</span> ${site.solar_irradiance_kwh} kWh<br>
        <span class="text-gray-600">Grid Dist:</span> ${site.grid_distance_km} km
      </div>
    `)
    
    // Add click event to marker to select it
    marker.on('click', () => {
       map.value.flyTo([lat, lng], 14)
    })

    markers.value.push(marker)
  })
}

const flyToSite = (site) => {
  // IMPORTANT: Parse strings to floats
  const lat = parseFloat(site.latitude)
  const lng = parseFloat(site.longitude)
  map.value.flyTo([lat, lng], 13, {
    duration: 1.5
  })
}

const getScoreColor = (score) => {
  if (score >= 80) return 'text-green-600'
  if (score >= 60) return 'text-yellow-600'
  return 'text-red-600'
}
</script>

<style>
/* Reset some basics just in case */
body, html { margin: 0; padding: 0; height: 100%; }
#app { height: 100%; width: 100%; display: block; max-width: none; padding: 0; }

/* Custom Scrollbar for Sidebar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #f1f1f1; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
</style>