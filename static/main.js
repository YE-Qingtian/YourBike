document.addEventListener("DOMContentLoaded", function () {
  const collapsibleHeaders = document.querySelectorAll(".collapsible-header");

  collapsibleHeaders.forEach(function (header) {
    header.addEventListener("click", function () {
      const content = this.nextElementSibling;
      content.classList.toggle("active");
    });
  });
});

let map;

async function initMap() {
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    zoom: 14,
    center: new google.maps.LatLng(53.34511048273914, -6.267027506499677),
  });

  new google.maps.Marker({
    position: { lat: 53.351757, lng: -6.279787 },
    map,
    title: "Hello World!",
  });
}

initMap();

// THE CODE BELOW WILL BE USED TO FETCH THE DATA  FROM THE DATABASE.

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
