//////////////////////////////////// START COLLAPSIBLE HANDLING FOR ALL COLLAPSIBLE ELEMENTS ////////////////////////////////////////////////////////////////////////////

document.addEventListener("DOMContentLoaded", function () {
  const collapsibleHeaders = document.querySelectorAll(".collapsible-header");
  collapsibleHeaders.forEach(function (header) {
    header.addEventListener("click", function () {
      const content = this.nextElementSibling;
      content.classList.toggle("active");
    });
  });

  const sidebar = document.getElementById("sidebar");
  const sidebarToggle = document.getElementById("sidebar-toggle");

  sidebarToggle.addEventListener("click", function () {
    const currentLeft = parseFloat(window.getComputedStyle(sidebar).left);
    if (currentLeft < 0) {
      sidebar.style.left = "20px";
    } else {
      sidebar.style.left = "-250px"; // Adjust according to your sidebar width
    }
  });
});
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////// FETCHING STATIONS DATA FROM OUR FLASK ENDPOINT /////////////////////////////////////////////////////////////////////
const fetchDataFromDatabase = async () => {
  try {
    const response = await fetch("/stations");
    if (!response.ok) {
      throw new Error("Failed to fetch stationsData from the database");
    }
    const stationsData = await response.json();
    // Process the stationsData here
    // console.log(stationsData);
    return stationsData;
  } catch (error) {
    console.error("Error fetching stationsData:", error.message);
  }
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Call the async function to fetch stationsData when needed
fetchDataFromDatabase();
let weatherValue; //the reason I did it here is a global variable access issue, this is the fastest way to I came across
let map;
let userLatLng;
let markerForPrediction = {}; // feature added at the very last to point station locations intuitively.
/////////////////////////////////////////////////////////// START MAP FUNCTIONALITY AND SERVICES /////////////////////////////////////////////////////////////////////
const autocompleteOptions = {
    componentRestrictions: { country: "ie" },
  };
async function initMap() {
  const {
    Map,
    DirectionsService,
    DirectionsRenderer,
  } = // check why it is not being used ? CHECKED. NEEDED, BUT NOT INVOKED ACCORDING TO MAPS DOCS
    await google.maps.importLibrary("maps");

  // const customMapStyles = [
  //   {
  //     featureType: "water",
  //     elementType: "geometry",
  //     stylers: [{ color: "#49beb7" }],
  //   },
  //   {
  //     featureType: "landscape",
  //     elementType: "geometry",
  //     stylers: [{ color: "#24d4dd45" }],
  //   },
  // ];
  map = new Map(document.getElementById("map"), {
    zoom: 14,
    center: new google.maps.LatLng(53.34511048273914, -6.267027506499677),
    // styles: customMapStyles, // Apply custom map styles
  });

  // Add marker for user's current location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      userLatLng = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      new google.maps.Marker({
        position: userLatLng,
        map: map,
        title: "Your Location",
        icon: {
          url: "/images/ava_female.png",
          scaledSize: new google.maps.Size(50, 50), // Adjust size as needed
        },
      });
    });
  } else {
    console.error("Geolocation is not supported by this browser.");
  }

  // new google.maps.Marker({
  //   position: { lat: 53.351757, lng: -6.279787 },
  //   map: map,
  //   title: "Hello World!",
  // });

  const circleMap = (numberOfBikes) => {
    let fillColor = "#1E9600";
    if (numberOfBikes > 18) {
      fillColor = "#1E9600";
    } else if (numberOfBikes < 18 && numberOfBikes >= 15) {
      fillColor = "#FFF200";
    } else if (numberOfBikes < 15 && numberOfBikes >= 10) {
      fillColor = "#b4ab00";
    } else {
      fillColor = "#FF0000";
    }

    return {
      path: google.maps.SymbolPath.CIRCLE,
      fillColor: fillColor,
      fillOpacity: 0.5,
      strokeColor: "red",
      strokeWeight: 0,
      scale: 15, // Qingtian adjust the size of the circle if u want to
    };
  };

  const stationsData = await fetchDataFromDatabase();
  if (stationsData) {
    let infoWindowStatus = null;
    Object.values(stationsData).forEach((station) => {
      // remeber that JSON data in not an array. that's why I kept getting errors
      const marker_station = new google.maps.Marker({
        position: { lat: station.position_lat, lng: station.position_lng },
        map: map,
        title: station.name,
        clickable: true,
        icon: circleMap(station.available_bikes),
      });

      markerForPrediction[station.number] = marker_station;
      const infoWindow = new google.maps.InfoWindow({
        content: `<div>
        <h3>${station.name}</h3>
        <p>Station no.: ${station.number}</p>
        <p>Available Bikes/Total Stands: ${station.available_bikes}/${station.bike_stands}</p>
        <div id="graphContainer" class="graphContainer"></div>
        </div>`,
      });

      // Add event listener to marker to open info window when clicked
      marker_station.addListener("click", function () {
        if (infoWindowStatus) {
          infoWindowStatus.close();
        }

        infoWindowStatus = infoWindow;

        let stationInfo = document.getElementById("station_info");
        let availableInfo = document.getElementById("avail_info");

        stationInfo.innerHTML = `
          <p>Number : ${station.number}</p>
          <p>Address: ${station.address}, ${station.contract_name}</p>
          <p>Latitude : ${station.position_lat}</p>
          <p>Longitude : ${station.position_lng}</p>
          <p>Bike Stands : ${station.bike_stands}</p>
        `;

        availableInfo.innerHTML = `
          <p>Bike Stand no. : ${station.number} </p>
          <p>Last Updated : ${new Date(
            station.last_update * 1000
          ).toLocaleString()}</p>
          <p>Available Bikes : ${station.available_bikes}</p>
          <p>Available Bike Stands : ${station.available_bike_stands}</p>
          
        `;
        // Open the info window
        infoWindow.open(map, marker_station);
        // Fetch the graph HTML from the Flask route and display it
        fetch(`/available/${station.number}`)
          .then((response) => response.json())
          .then((data) => {
            const graphContainer = document.getElementById("graphContainer");
            // Ensure the container is empty before plotting
            while (graphContainer.firstChild) {
              graphContainer.removeChild(graphContainer.firstChild);
            }
            console.log(data.graph_json);
            Plotly.newPlot(
              "graphContainer",
              data.graph_json.data,
              data.graph_json.layout
            );
          })
          .catch((error) => console.error("Error fetching graph:", error));
      });
    });
  }

  const addressInputStart = document.getElementById("location0");
  const addressInputDestination = document.getElementById("location1");
  const autocompleteStart = new google.maps.places.Autocomplete(
    addressInputStart, autocompleteOptions
  );
  const autocompleteDestination = new google.maps.places.Autocomplete(
    addressInputDestination, autocompleteOptions
  );

  addressInputStart.addEventListener("change", function () {
    calculateAndDisplayRoute();
    // console.log(autocompleteStart);
  });

  addressInputDestination.addEventListener("change", function () {
    calculateAndDisplayRoute();
  });
  const directionsRenderer = new google.maps.DirectionsRenderer();

  async function calculateAndDisplayRoute() {
    const startLocation = addressInputStart.value;
    const destination = addressInputDestination.value;

    if (!startLocation || !destination) {
      return;
    }

    const directionsService = new google.maps.DirectionsService();
    directionsRenderer.setMap(null);
    directionsRenderer.setMap(map);
    directionsService.route(
      {
        origin: startLocation,
        destination: destination,
        travelMode: google.maps.TravelMode.DRIVING,
      },
      (response, status) => {
        if (status === "OK") {
          directionsRenderer.setDirections(response);
        } else {
          window.alert("Directions request failed due to " + status);
        }
      }
    );
  }
}

initMap();

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////// FETCHING WEATHER INFO ALONE FROM SAME STATION ENDPOINT ////////////////////////////////////
const getTheWeatherInformation = async () => {
  try {
    const response = await fetch("/stations");
    if (!response.ok) {
      throw new Error("Failed to fetch stationsData from the database");
    }
    const stationsData = await response.json();
    // Process the stationsData here
    // console.log(stationsData);
    return stationsData;
  } catch (error) {
    console.error("Error fetching stationsData:", error.message);
  }
};

document.addEventListener("DOMContentLoaded", function () {
  const weatherValue = document.getElementById("userDate");
  const weatherDiv = document.getElementById("weatherDiv");
  const currentTimeAndDate = new Date()
    .toISOString()
    .slice(0, 16)
    .replace("T", "_");
  const temperatureWidget = document.getElementById("temp_widget");
  weatherValue.value = currentTimeAndDate;

  const fetchWeatherInformation = async (date) => {
    try {
      // Fetch weather data for the provided date
      const response = await fetch(`/weather/${date}`);
      if (!response.ok) {
        throw new Error("Issues with weather Data");
      }
      const weatherData = await response.json();
      // console.log(weatherData);
      return weatherData;
    } catch (error) {
      console.error(error.message);
      throw error; // Rethrow the error to handle it later
    }
  };

  const showWeatherInfo = (weatherData) => {
    // console.log(weatherData);
    if (!weatherData || weatherData.length === 0) {
      console.error("No weather data available");
      return;
    }
    const weatherSpecific = weatherData[0];
    const timestamp = weatherSpecific.dt;
    const date = new Date(timestamp * 1000);
    const dt = date.toISOString().slice(0, 16);

    weatherDiv.innerHTML = ` <p id="date_date">Date : ${dt}</p>
  <p id="temperature">Temperature : ${Math.trunc(
    weatherSpecific.temp - 273.15
  )} Celisus</p>
  <p id="pressure">Pressure : ${weatherSpecific.pressure}</p>
  <p id="humidity">Humidity : ${weatherSpecific.humidity}</p>
  <p id="status">Status : ${weatherSpecific.weather_main}</p>
  <p id="description">Description : ${weatherSpecific.weather_description}</p>`;

    temperatureWidget.innerHTML = `${Math.trunc(
      weatherSpecific.temp - 273.15
    )}  &deg; C&nbsp;&nbsp; <i class="fa-solid fa-cloud"></i>`;

    let weatherDesc = weatherSpecific.weather_description;
    let backgroundVideo = document.getElementById("bkg-video");
    let sourceVideo = document.getElementById("src-video");

    if (weatherDesc.includes("rain")) {
      sourceVideo.src = "/videos/raining_v2.mp4";

      backgroundVideo.load();
      temperatureWidget.innerHTML = `${Math.trunc(
        weatherSpecific.temp - 273.15
      )}  &deg; C&nbsp;&nbsp; <i class="fa-solid fa-cloud-rain"></i>`;
    } else if (weatherDesc.includes("clouds")) {
      sourceVideo.src = "/videos/clouds.mp4";
      backgroundVideo.load();
    } else if (weatherDesc.includes("clear sky")) {
      console.log("clear sky");
      sourceVideo.src = "/videos/clear_sky.mp4";
      backgroundVideo.load();

      temperatureWidget.innerHTML = `${Math.trunc(
        weatherSpecific.temp - 273.15
      )}  &deg; C&nbsp;&nbsp; <i class="fa-solid fa-cloud-sun"></i>`;
    } else {
      console.log("Weather condition not handled.");
    }
  };
  (async () => {
    try {
      const weatherData = await fetchWeatherInformation(currentTimeAndDate);
      showWeatherInfo(weatherData);
    } catch (error) {
      console.error(error.message);
    }
  })();
  // Show weather information for the current date when page loads
  // showWeatherInfo(currentTimeAndDate);

  weatherValue.addEventListener("change", async function () {
    const userInputedDate = weatherValue.value;
    const final_date = userInputedDate.replace("T", "_");
    // console.log(userInputedDate);
    try {
      // Fetch weather data for the selected date
      const weatherData = await fetchWeatherInformation(final_date);
      // Display weather information for the selected date
      showWeatherInfo(weatherData);
    } catch (error) {
      console.error(error.message);
    }
  });

  //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  //////////////////////////////////////////  START PREDICTION FUNCTIONALITY //////////////////////////////////////////////////////////////
  let markers = {};
  const locationInput = document.getElementById("location2");
  const dateInput = document.getElementById("userDate1");
  const recommendedStations = document.querySelector(".recommended-stations");
  const isoDate = new Date(dateInput + ":00").toISOString(); // implemented elsewhere
  const autocomplete2 = new google.maps.places.Autocomplete(locationInput, autocompleteOptions);

  const addMarkersForPredictions = (stationIds) => {
    stationIds.forEach((stationId) => {
      const marker = markerForPrediction[stationId];
      if (marker) {
        // Set custom property isPrediction to true
        marker.isPrediction = true;
      }
    });
  };

  const changeColorsForPredictions = (stationIds) => {
    Object.values(markerForPrediction).forEach((marker) => {
      if (marker.isPrediction) {
        marker.setIcon({
          path: google.maps.SymbolPath.CIRCLE,
          fillColor: "blue",
          fillOpacity: 0.5,
          strokeColor: "red",
          strokeWeight: 6,
          scale: 15,
        });
      }
    });
  };

  const fetchRecommendedStations = async (location, datetime) => {
    try {
      const nearestStations = await findNearestStations(location);

      const predictions = await Promise.all(
        nearestStations.map(async (stationId) => {
          try {
            const prediction = await fetchPrediction(stationId, datetime);
            return { station: stationId, prediction: Math.floor(prediction) };
          } catch (error) {
            console.error("Error fetching prediction:", error.message);
            return { station: stationId, prediction: "N/A" };
          }
        })
      );

      addMarkersForPredictions(
        predictions.map((prediction) => prediction.station)
      );
      changeColorsForPredictions(
        predictions.map((prediction) => prediction.station)
      );

      recommendedStations.innerHTML = ""; // to cleamn the previous recommended stations

      predictions.forEach((prediction) => {
        const stationPredictionDiv = document.createElement("div");
        stationPredictionDiv.className = "station-prediction";

        const stationInfo = document.createElement("p");
        stationInfo.textContent = `Recommended Station: ${prediction.station}`;
        stationPredictionDiv.appendChild(stationInfo);

        const predictionInfo = document.createElement("p");
        predictionInfo.textContent = `Predicted no. of Bikes: ${prediction.prediction}`;
        stationPredictionDiv.appendChild(predictionInfo);

        recommendedStations.appendChild(stationPredictionDiv);
      });
    } catch (error) {
      console.error("Error fetching recommended stations:", error.message);
    }
  };

  const findNearestStations = async (location) => {
    try {
      const stationsData = await fetchDataFromDatabase();
      if (!stationsData) {
        throw new Error("Failed to fetch stations data from the database.");
      }

      // Convert stationsData object to an array of station objects
      const stationArray = Object.values(stationsData);
      const distances = [];
      console.log(stationArray); // remember, no issues with fetching data, logical error somewhere else.
      // Calculate distances from the provided location to each station
      stationArray.forEach((station) => {
        const stationLocation = new google.maps.LatLng(
          station.position_lat,
          station.position_lng
        );

        const distance = google.maps.geometry.spherical.computeDistanceBetween(
          location,
          stationLocation
        );
        distances.push({ stationId: station.number, distance }); // dont forget, when no key is specified distance : distance => same as distance
      });
      // console.log(distances);
      // Sort stations by distance in ascending order
      distances.sort((a, b) => a.distance - b.distance);

      // Extract the nearest station IDs
      const nearestStations = distances
        .slice(0, 3)
        .map((station) => station.stationId);
      return nearestStations;
    } catch (error) {
      console.error("Error finding nearest stations:", error.message);

      return [];
    }
  };

  const fetchPrediction = async (stationId, datetime) => {
    try {
      // Fetch prediction for the specified station and datetime
      const response = await fetch(`/inference/${stationId}/${datetime}`);
      if (!response.ok) {
        throw new Error("Failed to fetch prediction data.");
      }
      // console.log("The passed datetime for fetchPredictions is : " + datetime); // testing
      let fetchData = await response.json();
      console.log(`data from fetchPredictions : ${fetchData}`);

      return fetchData;
    } catch (error) {
      console.error(
        `Error fetching prediction for station ${stationId}:`,
        error.message
      );
      return { station: stationId, prediction: "N/A" };
    }
  };

  // START TEST FOR GEOCODE ADDRESS
  async function geocodeAddress(address) {
    try {
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${encodeURIComponent(
          address
        )}&key=AIzaSyB0I6hTtpc6uQPVy2wcdKz1ezH4b3QfHlI`
      );
      const data = await response.json();
      if (data.results && data.results.length > 0) {
        const location = data.results[0].geometry.location;
        return { lat: location.lat, lng: location.lng };
      } else {
        throw new Error("No results found for the address");
      }
    } catch (error) {
      throw new Error("Error geocoding address: " + error.message);
    }
  }

  // END CODE FOR GEOCODE ADDRESS
  // Inside the event listener for location input change
  locationInput.addEventListener("change", async function () {
    const location = this.value;
    // console.log(location);
    const datetime = userInputedDateNew.toISOString().split(".")[0] + "Z";
    // console.log(
    //   "The time from dateInput is from locationInput listener is : " + datetime
    // );
    if (location && datetime) {
      try {
        // Use the geocodeAddress function to obtain coordinates
        const coordinates = await geocodeAddress(location);
        if (coordinates) {
          fetchRecommendedStations(
            new google.maps.LatLng(coordinates.lat, coordinates.lng),
            datetime
          );
        } else {
          throw new Error("No results found for the address");
        }
      } catch (error) {
        console.error("Error geocoding address:", error.message);
      }
    }
  });

  dateInput.addEventListener("change", async function () {
    const location = locationInput.value;
    const userInputedDateNew = new Date(this.value);
    const datetime = userInputedDateNew.toISOString().split(".")[0] + "Z";

    const currentDate = new Date();

    const futureDate = new Date(currentDate.setDate(currentDate.getDate() + 5));

    // console.log(typeof datetime); // for testing purposes

    if (userInputedDateNew > futureDate) {
      alert("Please Select a Date Within The Next 5 days.");
      this.value = ""; // this caused me problems, alert box was working, yet wasn't resitting. had to do this.
      return;
    }
    if (location && datetime) {
      try {
        // Use the geocodeAddress function to obtain coordinates
        const coordinates = await geocodeAddress(location);
        if (coordinates) {
          fetchRecommendedStations(
            new google.maps.LatLng(coordinates.lat, coordinates.lng),
            datetime
          );
        } else {
          throw new Error("No results found for the address");
        }
      } catch (error) {
        console.error("Error geocoding address:", error.message);
      }
    }
  });
});
////////////////////////////////////////////////////////////// END PREDICTION ////////////////////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////// HANDLING FETCHED PREDICTIONS //////////////////////////////////////////////////////////////////////

//   const markersForPrediction = (stationIds) => {
//     stationIds.forEach((stationId) => {
//       const marker = markerForPrediction[stationId];
//       if (marker) {
//         marker.setIcon({
//           path: google.maps.SymbolPath.CIRCLE,
//           fillColor: "red",
//           fillOpacity: 0.5,
//           strokeColor: "blue",
//           strokeWeight: 3,
//           scale: 15,
//         });
//       }
//     });
//   };
// });
// Didn't work, try integrating markers inside the fetchPrediction function

///////////////////////////////////////////////////// T   H    E         E      N         D ///////////////////////////////////////////////////////////////////////
