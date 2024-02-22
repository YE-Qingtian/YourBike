import pandas as pd
from flask import Flask, g, render_template, jsonify
from sqlalchemy import create_engine
import plotly.express as px
import datetime
from config import *

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
engine = create_engine(dblink)


@app.route('/')
def root():
    return render_template('index.html')


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
    current_datetime = datetime.datetime.now()
    current_day = current_datetime.strftime('%A')
    # Adjust to the start of the day, 7 days ago
    seven_days_ago_start = (current_datetime - datetime.timedelta(days=7)).replace(hour=0, minute=0, second=0,
                                                                                   microsecond=0)
    same_day_last_week = seven_days_ago_start.strftime('%A')

    query = f"SELECT * FROM availability WHERE number = {station_id} AND last_update >= {int(seven_days_ago_start.timestamp())}"
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
    df_resampled.sort_values(by='time_of_day', inplace=True)
    df_resampled['day_identifier'] = df_resampled['last_update_datetime'].apply(
        lambda x: f"{x.strftime('%A')}(Current)" if x.strftime('%A') == current_day and x.date() == current_datetime.date()
        else (f"{x.strftime('%A')}(Last Week)" if x.strftime('%A') == same_day_last_week and x.date() == seven_days_ago_start.date()
              else x.strftime('%A'))
    )

    # Create a Plotly graph using 'day_identifier' for color distinction
    fig = px.line(df_resampled, x='time_of_day', y='available_bikes', color='day_identifier',
                  template='plotly_white',
                  labels={'time_of_day': 'Time', 'available_bikes': 'Available Bikes', 'day_identifier': 'Day'})
    for trace in fig.data:
        if "Current" in trace.name:
            trace.line.width = 5  # Thicker line for the current day
            trace.line.dash = 'dot'  # Dotted style for the current day
        elif "Last Week" in trace.name:
            trace.line.width = 3  # Slightly thicker line for the same day last week
            trace.line.dash = 'longdash'  # Dashed style for the same day last week
        else:
            trace.line.width = 1  # Default line width for other days

    # Render the template with the graph
    graph_html = fig.to_html(full_html=False)
    return render_template("station.html", graph_html=graph_html)


if __name__ == "__main__":
    app.run(debug=True)
