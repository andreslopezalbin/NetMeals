// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.

function initAutocomplete() {
  // if (navigator.geolocation) {
  //   navigator.geolocation.getCurrentPosition(function(position) {
  //     var pos = {
  //       lat: position.coords.latitude,
  //       lng: position.coords.longitude
  //     };
  //
  //     infoWindow.setPosition(pos);
  //     infoWindow.setContent('Location found.');
  //     map.setCenter(pos);
  //   }, function() {
  //     handleLocationError(true, infoWindow, map.getCenter());
  //   });
  // } else {
  //   // Browser doesn't support Geolocation
  //   handleLocationError(false, infoWindow, map.getCenter());
  // }

  var ini_lat = parseFloat($('#id_latitude').val());
  var ini_lng = parseFloat($('#id_longitude').val());
  if(!ini_lat || !ini_lng){
    ini_lat = 40.4167754;
    ini_lng = -3.7037901999999576;
  }
  var map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: ini_lat, lng: ini_lng},
    zoom: 17,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  });

  map.setOptions({draggable: false, zoomControl: false, scrollwheel: false, disableDoubleClickZoom: true});

  var name = $('#id_name').val();
  var places = {
    type: 'Feature',
    geometry: {type: 'Point', coordinates: [ini_lng, ini_lat]},
    properties: {name: name}
  };
  // Add some markers to the map.
  map.data.setStyle(function(feature) {
    return {
      title: feature.getProperty('name'),
      optimized: false
    };
  });
  map.data.addGeoJson(places);

  // Create the search box and link it to the UI element.
  var input = document.getElementById('id_place');
  var searchBox = new google.maps.places.SearchBox(input);
  // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', function() {
    searchBox.setBounds(map.getBounds());
  });

  var markers = [];
  // [START region_getplaces]
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener('places_changed', function() {
    var places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach(function(marker) {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    var bounds = new google.maps.LatLngBounds();
    places.forEach(function(place) {
      var icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };

      // Create a marker for each place.
      markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
      }));

      var lat = place.geometry.location.lat();
      var lng = place.geometry.location.lng();
      $('#id_latitude').val(lat);
      $('#id_longitude').val(lng);

      console.log("latitud: " + lat + ", longitud: " + lng);

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
  // [END region_getplaces]
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}
