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
  import geojson from "@/geojson";

  
    
  onMounted(() => {
    const map = L.map("map").setView([18.521289663269744, 73.85745376264134], 11);

    map.locate({ setView: true, maxZoom: 11 });

    function onLocationFound(e) {
      var radius = e.accuracy;

      L.marker(e.latlng).addTo(map)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

      L.circle(e.latlng, radius).addTo(map);

      // var myLines = [{
      //   "type": "LineString",
      //   "coordinates": [[e.latlng.lng, e.latlng.lat], [73.85982299372604, 18.386795709467325]]
      // }, {
      //   "type": "LineString",
      //   "coordinates": [[73.95046020305803, 18.480599280074593], [73.85982299372604, 18.386795709467325]]
      // }];

      // var myStyle = {
      //   "color": "#000000",
      //   "weight": 1,
      //   "opacity": 0.5
      // };

      // L.geoJSON(myLines, { style: myStyle }).addTo(map);
    }

    map.on('locationfound', onLocationFound);
    console.log(geojson);

function onLocationError(e) {
    alert(e.message);
}

map.on('locationerror', onLocationError);

  
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
      

    // var refurbishIcon = L.icon({
    // iconUrl: 'https://i.ibb.co/TqbNFsj5/refurbish-removebg-preview.png',
    // iconSize:     [35, 35], // size of the icon
    // iconAnchor:   [20, 39.5], // point of the icon which will correspond to marker's location
    // popupAnchor:  [-3, -40] // point from which the popup should open relative to the iconAnchor
    // });

    // var recycleIcon = L.icon({
    // iconUrl: 'https://i.ibb.co/JRFCRBq5/recycle-removebg-preview.png',
    // iconSize:     [35, 35], // size of the icon
    // iconAnchor:   [20, 39.5], // point of the icon which will correspond to marker's location
    // popupAnchor:  [-3, -40] // point from which the popup should open relative to the iconAnchor
    // });
    
    // var marker0 = L.marker([18.387594509567865, 73.85427772376208], {icon: recycleIcon}).addTo(map);
    // marker0.bindPopup("<b>Recycler!</b><br>Recycling center.")

    // var marker1 = L.marker([18.480599280074593, 73.95046020305803], {icon: refurbishIcon}).addTo(map);
    // marker1.bindPopup("<b>Refurbisher!</b><br>Refurbisher center.")
  
    // var popup = L.popup();
  
    // function onMapClick(e) {
    //   popup
    //     .setLatLng(e.latlng)
    //     .setContent("You clicked the map at " + e.latlng.toString())
    //     .openOn(map);
    // }
  
    // map.on('click', onMapClick);
  

    //geojson

    function onEachFeature(feature, layer) {
    // does this feature have a property named popupContent?
    if (feature.properties && feature.properties.popupContent) {
        layer.bindPopup(feature.properties.popupContent);
    }
}

    var geojsonFeatures = [{
    "type": "Feature",
    "properties": {
        "name": "Hitech Recycling",
        "amenity": "Recycler",
        "popupContent": "This is where we recycle electronics!"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [73.85982299372604, 18.386795709467325]
    }
    },
    {
    "type": "Feature",
    "properties": {
        "name": "Poona E-waste Solutions",
        "amenity": "Refurbisher",
        "popupContent": "This is where we refurbish electronics!"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [73.95046020305803, 18.480599280074593]
    }
    }];

    L.geoJSON(geojsonFeatures, {
    filter: function(feature, layer) {
        return feature.properties.amenity === "Refurbisher" || feature.properties.amenity === "Recycler";
    }
}).addTo(map);

    L.geoJSON(geojson).addTo(map);

    // var myLayer = L.geoJSON().addTo(map);

    //// popup on click
    // L.geoJSON(geojsonFeatures, {
    //     onEachFeature: onEachFeature
    // }).addTo(map);

    // myLayer.addData(geojsonFeature, {
    //     onEachFeature: onEachFeature
    // });
    // myLayer.addData(geojson1Feature);

    
   
  });
  </script>