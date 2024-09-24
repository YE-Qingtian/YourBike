# Overview

The application represents a variety of integrated technologies that enables it to give real-time and future predictions of available bikes in different stations depending on your trip and future plans. The project consisted of various tasks including frontend development including building the main structure, styling it, handling interactiveness to communicating with the backend server through a flask application. The main source API used was JCdecaux from DublinBikes official website.  Moreover, backend development consists of creating various routes for our endpoints which will be considered as a new API for us to use in the frontend. Finally, a ML model was trained for each station and day of the week separately and then integrated with our application to give future predictions.
The application will:
- Retrieve bike station data from the Dublin Bike API.
- Fetch weather data from the Open Weather API.
- Convert original APIs in our flask app and create a new endpoint for those APIs
- Use Google Maps for displaying bike stations.
- Accept user input for bike-renting location and date/time.
- Basic error handling for user inputs (Human error) + Advanced error handling for internal developer issues.
- Display real-time bike and stand availability and weather information.
- Predict future bike and stand availability using a machine learning model.

# Architecture
This application can be divided into front and back end. Front end handles user inputs and passes instructions to backend, and backend retrieves data from API or Database and passes it to the user after processing.
The backend is running on an EC2 instance, and a separate MySQL database running on Amazon RDS service was used to store all collected data.
Flask was used as the main backend framework, it provides several endpoints for the front end, see table below. It used Sqlalchemy for connection with the database, Pandas and Sci-kit Learn for data processing and machine learning model inference, and Plotly for making the graph of availability across the previous week.

Function Name
Route
Return Value
root()
/
template of index.html
 get_weather()
/weather/<string:datetime_str>
json object of weather from database
get_stations()
/stations
json string of stations metadata from database
get_station(station_id)
/available/<int:station_id>
json object of Plotly graph, to be reconstructed by Plotly.js on the front end
inference(station_id, datetime_str)
/inference/<int:station_id>/<string:datetime_str>
json object of a float value. The predicted available bikes at station_id at datetime_str


Data scraper runs independently from the application, it was set to execute every 5 minutes by Cron on the EC2 machine and retrieve data from JCdecaux and OpenweatherAPI. The script processes the data and stores it into the database.
A script of dataDownload.py was written to retrieve and process data from the Database, the bike availability records were combined with corresponding weather data in Pandas. It will download and save all data into AvailabilityDataCombined.csv and AvailabilityDataCombined.gzip for later use in machine learning.
ML.ipynb was the testground for machine learning models. It needs to be run manually. It takes bike availability data and weather data from previous downloaded files. It trains several potential models and selects the best model for each station. The model is saved to a .joblib file with the number of the station as its file name inside models folder. Flask app will load the corresponding model and make inference. The model evaluation plots were saved to /plots with station number + model name as file name. 

(image source: tezeract.ai[7])
This web application is deployed on Amazon's Elastic Compute Cloud (EC2) using Ubuntu 22.04 as the operating system. Gunicorn acts as the WSGI server, while Nginx functions as both a web server and a reverse proxy. The domain (yourbike.v6.rocks) was a domain  provided by dynv6.com. SSL certificate provided by Let’s Encrypt. All http traffic will be diverted to https.
Unit test script was written under the test folder, Qingtian wrote unit tests as a proof of concept. Only basic functions inside the Flask application were tested with limited test cases. It was not rigorous and exhaustive, but we have demonstrated that it was in mind. Unfortunately not well-designed due to time constraints and short of staff.
As to the code structure and most important functions in the frontend, you can view the table below for more insights.


Function Name
Description 
Return Value
initMap()
Handles everything that has to do with the map, initializes the map, markers, routes …etc.
Doesn’t really return anything, from google maps docs 
fetchDataFromDatabase()
Fetches data about stations from the Flask endpoint "/stations".
Returns a promise that resolves to the JSON data of stations fetched from the database.
getTheWeatherInformation()
Fetches weather information from the Flask endpoint "/stations".
Returns a promise for weather data
fetchWeatherInformation(date)
Fetches weather data for the provided date from the Flask endpoint "/weather/{date}".
Return a promise for weather data, but only for a specified date
calculateAndDisplayRoute()
calculates the distance and displays the best route between start location and destination when the user provides addresses.
Google docs code, no return value.
findNearestStations(location)
finds the nearest stations provided by the user provided location and looks at stations that are near the user.
Returns a Promise that resolves to an array of IDs of the nearest stations.
fetchPrediction(stationId, datetime)
Fetches predictions for the specified station and datetime from the Flask endpoint "/inference/{stationId}/{datetime}".
Return a promise for a specific station number and date.
geocodeAddress(address)
Converts the provided address into geographical coordinates (latitude and longitude) using the Google Maps Geocoding API.
Returns a Promise that resolves to an object containing the latitude and longitude coordinates of the provided address.
fetchRecommendedStations(location, datetime)
fetches nearest stations based on the users inputted location and the datetime 
No specific return value, used as a main function with nested funcs inside of it.
showWeatherInfo(weatherData)
Displays weather information fetched from the database on the webpage, including temperature, pressure, humidity, and weather status.
No Return value

