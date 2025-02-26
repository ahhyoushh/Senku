<template>
    <div id="map" class="map-container"></div>
  </template>
    
  <style>
  .map-container {
    height: 100vh;
    width: 100vw;
    margin: 0;
    padding: 0;
    position: fixed;
    top: 0;
    left: 0;
  }
  
  /* Ensure Leaflet controls don't get cut off */
  :global(.leaflet-control-container) {
    position: absolute;
    z-index: 1000;
  }
  </style>
  
  <script setup>
  import { onMounted } from "vue";
  import L from "leaflet";
    
  onMounted(() => {
    const map = L.map("map").setView([18.521289663269744, 73.85745376264134], 11    );

    map.locate({setView: true, maxZoom: 11});

    function onLocationFound(e) {
    var radius = e.accuracy;

    L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

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
      

    var refurbishIcon = L.icon({
    iconUrl: 'https://i.ibb.co/TqbNFsj5/refurbish-removebg-preview.png',
    iconSize:     [35, 35], // size of the icon
    iconAnchor:   [20, 39.5], // point of the icon which will correspond to marker's location
    popupAnchor:  [-3, -40] // point from which the popup should open relative to the iconAnchor
    });

    var recycleIcon = L.icon({
    iconUrl: 'https://i.ibb.co/JRFCRBq5/recycle-removebg-preview.png',
    iconSize:     [35, 35], // size of the icon
    iconAnchor:   [20, 39.5], // point of the icon which will correspond to marker's location
    popupAnchor:  [-3, -40] // point from which the popup should open relative to the iconAnchor
    });
    


    var marker0 = L.marker([18.387594509567865, 73.85427772376208], {icon: recycleIcon}).addTo(map);
    marker0.bindPopup("<b>Recycler!</b><br>Recycling center.")

    var marker1 = L.marker([18.480599280074593, 73.95046020305803], {icon: refurbishIcon}).addTo(map);
    marker1.bindPopup("<b>Refurbisher!</b><br>Refurbisher center.")
  
    var popup = L.popup();
  
    function onMapClick(e) {
      popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
    }
  
    map.on('click', onMapClick);
  
   
  });
  </script>