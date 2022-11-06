// import { List_of_places } from './script.js';

/////// Visual Representation
function initMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 4,
    center: { lat: 43.6532, lng: -79.3832 }, // Toronto.
  });
  const directionsService = new google.maps.DirectionsService();
  const directionsRenderer = new google.maps.DirectionsRenderer({
    draggable: true,
    map,
    panel: document.getElementById("panel"),
  });

  directionsRenderer.addListener("directions_changed", () => {
    const directions = directionsRenderer.getDirections();

    if (directions) {
      computeTotalDistance(directions);
    }
  });
  displayRoute(
    directionsService,
    directionsRenderer
  );
}

function displayRoute(service, display) {
  const List_of_places = localStorage.getItem('locations').split(',');
  const origin = List_of_places[0] + ' toronto';
  const destination = List_of_places[List_of_places.length-1] + ' toronto';

  const waypoints = []
  for (let i = 1; i < List_of_places.length - 1; i++) { 
    waypoints.push({
      location: List_of_places[i] + ' toronto'
    })
  }
  
  service
    .route({
      origin: origin,
      destination: destination,
      waypoints: waypoints,
      travelMode: google.maps.TravelMode.WALKING,
    })
    .then((result) => {
      console.log(result)
      display.setDirections(result);
    })
    .catch((e) => {
      alert("Could not display directions due to: " + e);
    });
}

function computeTotalDistance(result) {
  let total = 0;
  const myroute = result.routes[0];

  if (!myroute) {
    return;
  }

  for (let i = 0; i < myroute.legs.length; i++) {
    total += myroute.legs[i].distance.value;
  }

  total = total / 1000;
  document.getElementById("total").innerHTML = total + " km";
}

window.initMap = initMap;
