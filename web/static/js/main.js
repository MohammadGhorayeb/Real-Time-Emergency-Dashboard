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



async function processInputText() {
    const inputField = document.getElementById('user-input');
    const outputField = document.getElementById('output-box');

    const userInput = inputField.value;

    try {
        const response = await fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `user_input=${encodeURIComponent(userInput)}`
        });

        const data = await response.json();
        console.log("Response from process_text:", data);

        // Update the output box
        outputField.textContent = `Class: ${data.Class}, Description: ${data.Description}`;

        // Add markers to the map
        const subLocations = data.SubLocations;

        // Clear existing markers (if needed)
        document.querySelectorAll('.mapboxgl-marker').forEach(marker => marker.remove());

        // Add new markers
        subLocations.forEach((loc) => {
            console.log("Adding marker for location:", loc);

            // Check if lat/lng are valid numbers
            if (loc.lat && loc.lng) {
                new mapboxgl.Marker()
                    .setLngLat([loc.lng, loc.lat])  // Longitude, Latitude
                    .setPopup(new mapboxgl.Popup().setHTML(`<b>${loc.name}</b>`))  // Popup with name
                    .addTo(map);
            } else {
                console.warn("Invalid coordinates for location:", loc);
            }
        });
    } catch (error) {
        console.error("Error processing input:", error);
        outputField.textContent = "An error occurred while processing the input.";
    }
}

// Fetch and display locations from the server
async function fetchAndDisplayLocations() {
    try {
        // Fetch location data from the Flask API
        const response = await fetch('/get_sub_locations');
        const locations = await response.json();

        // Loop through the locations and add them to the map
        locations.forEach((loc) => {
            new mapboxgl.Marker()  // Create a new marker
                .setLngLat([loc.lng, loc.lat])  // Set marker position
                .setPopup(new mapboxgl.Popup().setHTML(`<b>${loc.name}</b>`))  // Add popup with location name
                .addTo(map);  // Add marker to the map
        });
    } catch (error) {
        console.error("Error fetching or displaying locations:", error);
    }
}
// Initialize the map and load locations
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

    // Fetch and display locations on the map
    fetchAndDisplayLocations();
});

