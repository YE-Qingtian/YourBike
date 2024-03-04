document.addEventListener("DOMContentLoaded", function () {
  // Add event listeners for collapsible headers
  const collapsibleHeaders = document.querySelectorAll(".collapsible-header");
  collapsibleHeaders.forEach(function (header) {
    header.addEventListener("click", function () {
      const content = this.nextElementSibling;
      content.classList.toggle("active");
    });
  });
});
const fetchDataFromDatabase = async () => {
  try {
    const response = await fetch("/stations");
    if (!response.ok) {
      throw new Error("Failed to fetch stationsData from the database");
    }
    const stationsData = await response.json();
    // Process the stationsData here
    console.log(stationsData);
    return stationsData;
  } catch (error) {
    console.error("Error fetching stationsData:", error.message);
  }
};

// Call the async function to fetch stationsData when needed
fetchDataFromDatabase();

let map;
let userLatLng;
async function initMap() {
  const { Map, DirectionsService, DirectionsRenderer } =
    await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    zoom: 14,
    center: new google.maps.LatLng(53.34511048273914, -6.267027506499677),
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
          url: "https://toppng.com/uploads/preview/reen-person-icon-transparent-png-green-person-icon-green-person-ico-11563325236gfijwfavym.png",
          scaledSize: new google.maps.Size(50, 50), // Adjust size as needed
        },
      });
    });
  } else {
    console.error("Geolocation is not supported by this browser.");
  }

  new google.maps.Marker({
    position: { lat: 53.351757, lng: -6.279787 },
    map: map,
    title: "Hello World!",
  });

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
      scale: 15, // Adjust the size of the circle
    };
  };

  const stationsData = await fetchDataFromDatabase();
  if (stationsData) {
    Object.values(stationsData).forEach((station) => {
      // remeber that JSON data in not an array. that's why I kept getting errors
      const marker_station = new google.maps.Marker({
        position: { lat: station.position_lat, lng: station.position_lng },
        map: map,
        title: station.name,
        clickable: true,
        icon: circleMap(station.available_bikes),
      });
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
  const addressInput = document.getElementById("location");
  addressInput.addEventListener("change", function () {
    calculateAndDisplayRoute(addressInput.value);
  });

  // Function to calculate and display route
  function calculateAndDisplayRoute(destination) {
    // const directionsService = new DirectionsService();
    const directionsService = new google.maps.DirectionsService(); // mistake I was making is init in different ways.

    // const directionsRenderer = new DirectionsRenderer();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setDirections({ routes: [] }); // CLEARING PREV ROUTES .. NOT WORKING YET
    directionsRenderer.setMap(map);

    directionsService.route(
      {
        origin: userLatLng,
        destination: destination,
        travelMode: google.maps.TravelMode.BICYCLING,
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

const getTheWeatherInformation = async () => {
  try {
    const response = await fetch("/stations");
    if (!response.ok) {
      throw new Error("Failed to fetch stationsData from the database");
    }
    const stationsData = await response.json();
    // Process the stationsData here
    console.log(stationsData);
    return stationsData;
  } catch (error) {
    console.error("Error fetching stationsData:", error.message);
  }
};

document.addEventListener("DOMContentLoaded", function () {
  const weatherValue = document.getElementById("userDate");
  const weatherDiv = document.getElementById("weatherDiv");

  weatherValue.addEventListener("change", async function () {
    const userInputedDate = weatherValue.value;
    // Qingtian, why is your weather foramt with _ and not ISO T ??
    const final_date = userInputedDate.replace("T", "_");
    try {
      const response = await fetch(`/weather/${final_date}`);
      if (!response.ok) {
        throw new Error("Issues with weather Data");
      }
      let weatherData = await response.json();
      console.log(weatherData);
      showWeatherInfo(weatherData);
    } catch (error) {
      console.log(error.message);
    }
  });
  let showWeatherInfo = (weatherData) => {
    const weatherSpecific = weatherData[0];
    const timestamp = weatherSpecific.dt;
    const date = new Date(timestamp * 1000);
    const dt = date.toUTCString();

    weatherDiv.innerHTML = ` <p id="date_date">Date : ${dt}</p>
    <p id="temperature">Temperature : ${weatherSpecific.temp}</p>
    <p id="pressure">Pressure : ${weatherSpecific.pressure}</p>
    <p id=" humidity">Humidity : ${weatherSpecific.humidity}</p>
    <p id="status">Status : ${weatherSpecific.weather_main}</p>
    <p id="description">Description : ${weatherSpecific.weather_description}</p>`;
  };
});

// THE CODE BELOW WILL BE USED TO FETCH THE DATA  FROM THE DATABASE.
