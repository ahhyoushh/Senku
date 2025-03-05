<template>
  <div id="map" class="map-container"></div>
</template>

<script setup>
import { onMounted, defineEmits } from "vue";
import L from "leaflet";
import geojson from "@/geojson";

const emit = defineEmits(['coordinatesUpdate']);

onMounted(() => {
  const map = L.map("map").setView([18.521289663269744, 73.85745376264134], 11);

  // Update coordinates on map click
  map.on('click', (e) => {
    const { lat, lng } = e.latlng;
    emit('coordinatesUpdate', [lng, lat]);
  });

  map.locate({ setView: true, maxZoom: 11 });

  function onLocationFound(e) {
    var radius = e.accuracy;
    emit('coordinatesUpdate', [e.latlng.lng, e.latlng.lat]);
    L.marker(e.latlng, {icon: userIcon})
      .addTo(map)
      .bindPopup("You are within " + radius + " meters from this point")
      .openPopup();
    L.circle(e.latlng, radius).addTo(map);
  }

  map.on('locationfound', onLocationFound);

  function onLocationError(e) {
    alert(e.message);
  }

  map.on('locationerror', onLocationError);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  function createCustomPopupContent(feature) {
    const properties = feature.properties;
    return `
      <div class="custom-popup">
        <h3 class="popup-title">${properties.name || properties.Type}</h3>
        ${properties.Name ? `<p class="popup-name"><strong></strong> ${properties.Name}</p>` : ''}
        ${properties.phone ? `<p class="popup-phone"><strong>Phone:</strong> ${properties.phone}</p>` : ''}
        ${properties.Email  ? `<a href="${properties.website}" target="_blank" class="popup-link">Visit Website</a>` : ''}
        ${properties.description ? `<p class="popup-description">${properties.description}</p>` : ''}
      </div>
    `;
  }

  function onEachFeature(feature, layer) {
    if (feature.properties) {
      const popupContent = createCustomPopupContent(feature);
      const popupOptions = {
        maxWidth: 300,
        className: 'custom-popup-container',
        closeButton: true,
        autoPan: true
      };
      
      layer.bindPopup(popupContent, popupOptions);
      
      // Add hover effect
      layer.on({
        mouseover: function(e) {
          const layer = e.target;
          layer.openPopup();
        },
        mouseout: function(e) {
          const layer = e.target;
          // Uncomment the next line if you want popups to close on mouseout
          // layer.closePopup();
        },
        click: function(e) {
          const layer = e.target;
          map.setView(layer.getLatLng(), 14);
        }
      });
    }
  }

  // Your existing icon definitions
  var userIcon = new L.icon({
    iconUrl: 'https://i.ibb.co/B2WvF3vm/image.png',
    iconSize: [35, 49.28],
    iconAnchor: [20, 39.5],
    popupAnchor: [-3, -40]
  });
  
  var refurbishIcon = new L.icon({
    iconUrl: 'https://i.ibb.co/HTVSvSnx/image-removebg-preview.png',
    iconSize: [35, 49.28],
    iconAnchor: [20, 39.5],
    popupAnchor: [-3, -40]
  });

  var recycleIcon = new L.icon({
    iconUrl: 'https://i.ibb.co/Wvr9ndwz/image-removebg-preview-1.png',
    iconSize: [35, 49.28],
    iconAnchor: [20, 39.5],
    popupAnchor: [-3, -40]
  });

  var dismantlerIcon = new L.icon({
    iconUrl: 'https://i.ibb.co/RGmkWpZV/image-removebg-preview-2.png',
    iconSize: [35, 49.28],
    iconAnchor: [20, 39.5],
    popupAnchor: [-3, -40]
  });

  L.geoJSON(geojson, {
    pointToLayer: function(feature, latlng) {
      let icon;
      switch (feature.properties.Type) {
        case 'Refurbisher':
          icon = refurbishIcon;
          break;
        case 'Recycler':
          icon = recycleIcon;
          break;
        case 'Dismantler':
          icon = dismantlerIcon;
          break;
        default:
          icon = new L.Icon.Default();
      }
      return L.marker(latlng, {icon: icon});
    },
    onEachFeature: onEachFeature,
    filter: function(feature) {
      return ['Refurbisher', 'Recycler', 'Dismantler'].includes(feature.properties.Type);
    }
  }).addTo(map);
});
</script>

<style scoped>
.map-container {
  height: 100%;
  width: 100%;
}

/* Custom popup styles */
:global(.custom-popup-container) {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

:global(.custom-popup) {
  padding: 12px;
}

:global(.popup-title) {
  margin: 0 0 8px 0;
  color: #333;
  font-size: 1.2em;
  font-weight: bold;
}

:global(.popup-address),
:global(.popup-phone),
:global(.popup-type) {
  margin: 4px 0;
  color: #666;
  font-size: 0.9em;
}

:global(.popup-description) {
  margin: 8px 0;
  color: #444;
  font-size: 0.9em;
}

:global(.popup-link) {
  display: inline-block;
  margin: 8px 0;
  padding: 6px 12px;
  background-color: #4CAF50;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.9em;
}

:global(.popup-link:hover) {
  background-color: #45a049;
}

/* Ensure Leaflet controls don't get cut off */
:global(.leaflet-control-container) {
  position: absolute;
  z-index: 900;
}
</style>
