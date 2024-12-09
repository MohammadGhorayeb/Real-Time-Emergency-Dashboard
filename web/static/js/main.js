// Add your Mapbox token
mapboxgl.accessToken = 'pk.eyJ1IjoibW9lZ2hvIiwiYSI6ImNtNGd4N3QzcDAweW8ycnM4M2N0eHVtNHUifQ.3REc3fDp4EwQ6pFeCvH7Gg'; // Replace with your Mapbox token

// Initialize the map
const map = new mapboxgl.Map({
    container: 'map', // The container ID
    style: 'mapbox://styles/mapbox/satellite-v9', // Satellite 3D style
    center: [35.5018, 33.8938], // Default to Beirut [lng, lat]
    zoom: 12,
    pitch: 45, // Tilt for 3D view
    bearing: -17.6, // Orientation of the map
    antialias: true // Enable anti-aliasing for smoother rendering
});

map.on('load', () => {
    map.addSource('mapbox-dem', {
        type: 'raster-dem',
        url: 'mapbox://mapbox.mapbox-terrain-dem-v1',
        tileSize: 512,
        maxzoom: 14
    });

    map.setTerrain({ source: 'mapbox-dem', exaggeration: 1.5 });

    map.addLayer({
        id: 'sky',
        type: 'sky',
        paint: {
            'sky-type': 'atmosphere',
            'sky-atmosphere-sun': [0.0, 90.0],
            'sky-atmosphere-sun-intensity': 15
        }
    });
});

// Function to process text and update the map
async function processInputText() {
    const inputField = document.getElementById('user-input');
    const outputField = document.getElementById('output-box');
    
    // Get user input
    const userInput = inputField.value;

    // Make a POST request to the server
    const response = await fetch('/process_text', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_input=${encodeURIComponent(userInput)}`
    });

    const data = await response.json();

    // Update the output box with the processed text
    outputField.textContent = data.output_text;

    // Update the map with sub-locations
    const subLocations = data.sub_locations;
    subLocations.forEach((loc) => {
        new mapboxgl.Marker()
            .setLngLat([loc.lng, loc.lat])
            .setPopup(new mapboxgl.Popup().setHTML(`<b>${loc.name}</b>`)) // Add popup
            .addTo(map);
    });
}
