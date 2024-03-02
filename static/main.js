document.addEventListener("DOMContentLoaded", function () {
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

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    zoom: 14,
    center: new google.maps.LatLng(53.34511048273914, -6.267027506499677),
  });

  // Add marker for user's current location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const userLatLng = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      new google.maps.Marker({
        position: userLatLng,
        map: map,
        title: "Your Location",
        icon: {
          url: "https://png.pngtree.com/png-clipart/20190924/original/pngtree-human-avatar-free-vector-png-image_4825373.jpg",
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

  const circleMap = {
    path: google.maps.SymbolPath.CIRCLE,
    fillColor: "blue",
    fillOpacity: 0.5,
    strokeColor: "red",
    strokeWeight: 2,
    scale: 15, // Adjust the size of the circle
  };

  const stationsData = await fetchDataFromDatabase();
  if (stationsData) {
    Object.values(stationsData).forEach((station) => {
      // remeber that JSON data in not an array. that's why I kept getting errors
      new google.maps.Marker({
        position: { lat: station.position_lat, lng: station.position_lng },
        map: map,
        title: station.name,
        clickable: true,
        icon: circleMap,
      });
    });
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
