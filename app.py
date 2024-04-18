import pandas as pd
from flask import Flask, g, render_template, jsonify
from sqlalchemy import create_engine, text
import plotly.express as px
import datetime
from config import *
import json
import joblib
import requests

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
engine = create_engine(dblink)


@app.route('/')
def root():
    google_map_api_key = GoogleMap_api_key
    return render_template('index.html', google_map_api_key = google_map_api_key)


@app.route('/weather/<string:datetime_str>')
def get_weather(datetime_str):
    """
    The function should lookup for the closest dt (Primary key) and return the record in json.

    :param datetime_str: format %Y-%m-%d_%H:%M, example 2024-02-25_10:38
    :return: example, [{"dt":1708804200,
    "sunrise":1708759439,"sunset":1708797059,"temp":278.55,"feels_like":276.7,"pressure":997,"humidity":93,"uvi":0.0,
    "clouds":100,"visibility":10000,"wind_speed":2.3,"wind_deg":120,"wind_gust":2.2,"weather_main":"Clouds",
    "weather_description":"overcast clouds","rain":null,"snow":null}]
    """
    try:
        input_datetime = datetime.datetime.strptime(datetime_str, "%Y-%m-%d_%H:%M")

        # SQL to find the closest dt
        query = text("""
            SELECT * FROM weather
            ORDER BY ABS(TIMESTAMPDIFF(SECOND, dt, :dt))
            LIMIT 1
        """)

        df = pd.read_sql_query(query, engine, params={'dt': input_datetime})

        if not df.empty:
            # Convert DataFrame to JSON
            # orient='records' makes the JSON output as an array of records
            return df.to_json(orient='records', date_format='iso')
        else:
            return jsonify({"error": "No weather data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/stations')
def get_stations():
    query = """
    SELECT s.*, last_update, a.available_bike_stands, a.available_bikes
    FROM station s
    JOIN (
        SELECT number, last_update, available_bike_stands, available_bikes
        FROM availability
        WHERE (number, last_update) IN (
            SELECT number, MAX(last_update)
            FROM availability
            GROUP BY number
        )
    ) a ON s.number = a.number
    """
    stations = pd.read_sql_query(query, engine)
    return stations.to_json(orient='index')


@app.route("/available/<int:station_id>")
def get_station(station_id):
    """
    param: station_id
    return: The returned snippet should be embedded inside your main page, change index.html and
    css, so it fits in your index.html. Modify the return of this function if necessary.
    """

    # Data Query
    current_datetime = datetime.datetime.utcnow()
    current_day = current_datetime.strftime('%a')
    # Adjust to the start of the day
    seven_days_ago_start = (current_datetime - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0)
    same_day_last_week = seven_days_ago_start.strftime('%a')
    query = f"SELECT * FROM availability WHERE number = {station_id} AND last_update >= {int(1000 * (seven_days_ago_start.timestamp()-3600))}"
    data = pd.read_sql_query(query, engine)

    # Data preparation
    df = pd.DataFrame(data, columns=['number', 'last_update', 'available_bike_stands', 'available_bikes'])
    df['last_update_datetime'] = pd.to_datetime(df['last_update'], unit='ms')
    df['day_of_week'] = df['last_update_datetime'].dt.day_name()
    df['time_of_day'] = df['last_update_datetime'].dt.time
    df.set_index('last_update_datetime', inplace=True)
    df_resampled = df.resample('15min')['available_bikes'].mean()
    df_resampled = df_resampled.to_frame().reset_index()
    df_resampled['day_of_week'] = df_resampled['last_update_datetime'].dt.day_name()
    df_resampled['time_of_day'] = df_resampled['last_update_datetime'].dt.time
    df_resampled['time_of_day'] = df_resampled['last_update_datetime'].dt.strftime('%H:%M')
    df_resampled.sort_values(by='last_update_datetime', inplace=True)
    df_resampled['day_identifier'] = df_resampled['last_update_datetime'].apply(
        lambda x: f"{x.strftime('%a')}(Now)" if x.strftime(
            '%a') == current_day and x.date() == current_datetime.date()
        else (f"{x.strftime('%a')}(Last)" if x.strftime(
            '%a') == same_day_last_week and x.date() == seven_days_ago_start.date()
              else x.strftime('%a'))
    )

    df_resampled = df_resampled[df_resampled['last_update_datetime']>=seven_days_ago_start]
    # Create a Plotly graph using 'day_identifier' for color distinction
    fig = px.line(df_resampled, x='time_of_day', y='available_bikes', color='day_identifier',
                  template='plotly_white',
                  labels={'time_of_day': 'Time', 'available_bikes': 'Available Bikes', 'day_identifier': 'Day'})
    for trace in fig.data:
        if "Now" in trace.name:
            trace.line.width = 5  # Thicker line for the current day
            trace.line.dash = 'dash'  # Dotted style for the current day
        elif "Last" in trace.name:
            trace.line.width = 3  # Slightly thicker line for the same day last week
            # trace.line.dash = 'dash'  # Dashed style for the same day last week
        else:
            trace.line.width = 0.5  # Default line width for other days

    # Render the template with the graph
    graph_json = fig.to_json(pretty=True)
    # Output for debug
    # graph_html = fig.to_html()
    # return render_template("station.html", graph_html=graph_html, tables = [df_resampled.to_html(header="true", table_id="table")])
    return jsonify(graph_json=json.loads(graph_json))


@app.route('/inference/<int:station_id>/<string:datetime_str>')
def inference(station_id, datetime_str):
    """
    :param station_id:
    :param datetime_str: Using ISO 8601 format. example. inference/84/2024-04-05T10:30:30Z
    :return:
    """

    def addHourDayMonth(dfX):
        # Convert 'last_update' to datetime and extract useful features
        dfX['last_update'] = pd.to_datetime(dfX['last_update'])
        dfX['hour'] = dfX['last_update'].dt.hour
        dfX['day'] = dfX['last_update'].dt.day
        dfX['day_of_week'] = dfX['last_update'].dt.dayofweek
        dfX['month'] = dfX['last_update'].dt.month
        dfX = dfX.drop(['last_update'], axis=1, inplace=True)

    def get_infer_weather(station_id, datetime_str):
        def parse_item(item):
            rain = item.get('rain', {'1h': None}).get('1h')
            snow = item.get('snow', {'1h': None}).get('1h')
            weather_main = item['weather'][0]['main'] if 'weather' in item and item['weather'] else None
            weather_description = item['weather'][0]['description'] if 'weather' in item and item['weather'] else None
            return {
                'dt': item.get('dt'),
                'sunrise': item.get('sunrise'),
                'sunset': item.get('sunset'),
                'temp': item.get('temp'),
                'feels_like': item.get('feels_like'),
                'pressure': item.get('pressure'),
                'humidity': item.get('humidity'),
                'uvi': item.get('uvi'),
                'clouds': item.get('clouds'),
                'visibility': item.get('visibility'),
                'wind_speed': item.get('wind_speed'),
                'wind_deg': item.get('wind_deg'),
                'wind_gust': item.get('wind_gust'),
                'weather_main': weather_main,
                'weather_description': weather_description,
                'rain': rain,
                'snow': snow
            }

        dtForecast = int(datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").timestamp())
        weatherResponse = requests.get(
            f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={53}&lon={-6}&dt={dtForecast}&appid={OpenWeather_api_key}")
        weatherJson = json.loads(weatherResponse.text)
        weather = parse_item(weatherJson['data'][0])
        return weather

    model = joblib.load(f"ML/models/{station_id}.joblib")
    X_infer = pd.DataFrame.from_dict(
        [{"number": station_id, "banking": 0, "last_update": datetime_str} | get_infer_weather(station_id, datetime_str)])
    featuresList = ["number","last_update","banking","temp","feels_like","pressure","humidity","uvi","clouds","visibility","wind_speed","wind_gust","weather_main","rain","weather_description"]
    X_infer = X_infer[featuresList]
    addHourDayMonth(X_infer)
    print(f"model: ML/models/{station_id}.joblib \ndatetime_str: {datetime_str}")
    prediction = model.predict(X_infer)
    return str(prediction[0])


if __name__ == "__main__":
    app.run(debug=True)
