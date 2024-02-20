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

// const fetchDataFromDatabase = async () => {
//   try {
//     const response = await fetch("/stations"); // '/stations' in not yet ready for implementation.
//     if (!response.ok) {
//       throw new Error("Failed to fetch data from the database");
//     }
//     const data = await response.json();
//     // Process the data here
//     console.log(data);
//   } catch (error) {
//     console.error("Error fetching data:", error.message);
//   }
// };

// // Call the async function to fetch data when needed
// fetchDataFromDatabase();
