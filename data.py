import sqlalchemy as sqla
from sqlalchemy import create_engine
from sqlalchemy.dialects.mysql import insert
import traceback
import glob
import os
import json
from pprint import pprint
import requests
from datetime import datetime
import pandas as pd
from config import *
import logging


def insert_on_conflict_nothing(table, conn, keys, data_iter):
    data = [dict(zip(keys, row)) for row in data_iter]
    stmt = insert(table.table).prefix_with('IGNORE').values(data)
    result = conn.execute(stmt)
    return result.rowcount


def round_to_nearest_10min(timestamp):
    dt = datetime.utcfromtimestamp(timestamp // 1000)  # Convert ms to seconds
    rounded_minute = int(10 * round(float(dt.minute) / 10))
    return int(datetime(dt.year, dt.month, dt.day, dt.hour, rounded_minute).timestamp())


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


logging.basicConfig(filename='data.log', encoding='utf-8', level=logging.DEBUG)
engine = create_engine(dblink)
metadata = sqla.MetaData()
station = sqla.Table(
    "station", metadata,
    sqla.Column("number", sqla.String(256), nullable=False, primary_key=True),
    sqla.Column("contract_name", sqla.String(256), nullable=False),
    sqla.Column("name", sqla.String(256), nullable=False),
    sqla.Column("address", sqla.String(256), nullable=False),
    sqla.Column("position_lat", sqla.REAL),
    sqla.Column("position_lng", sqla.REAL),
    sqla.Column("banking", sqla.Integer),
    sqla.Column("bonus", sqla.Integer),
    sqla.Column("bike_stands", sqla.Integer),
    sqla.Column("status", sqla.String(256)),
)

availability = sqla.Table(
    "availability", metadata,
    sqla.Column("number", sqla.Integer, primary_key=True, nullable=False),
    sqla.Column("last_update", sqla.BigInteger, primary_key=True, nullable=False),
    sqla.Column("available_bike_stands", sqla.Integer),
    sqla.Column("available_bikes", sqla.Integer),
)

metadata.create_all(engine)

urlStations = f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}&apiKey={JDC_api_key}"
response = requests.get(urlStations)
json_struct = json.loads(response.text)
df = pd.json_normalize(json_struct, sep='_')

dfStations = df[
    ['number', 'contract_name', 'name', "address", "position_lat", "position_lng", "banking", "bonus", "bike_stands",
     "status"]]
dfAvailability = df[['number', "last_update", 'available_bike_stands', 'available_bikes']]
try:
    dfStations.to_sql("station", engine, index=False, if_exists='append')
except:
    logging.debug("Stations Table Already Exist.")

dfAvailability.to_sql("availability", engine, index=False, if_exists='append', method=insert_on_conflict_nothing)
logging.info(f"{datetime.now():%Y-%m-%d %H:%M:%S} Update Success. Total records:{dfAvailability.shape[0]}")

dfAvailability['rounded_timestamp'] = dfAvailability['last_update'].apply(round_to_nearest_10min)
unique_timestamps = dfAvailability['rounded_timestamp'].unique()
parsed_data = []
for i in unique_timestamps:
    weatherResponse = requests.get(
        f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={53}&lon={-6}&dt={i}&appid={OpenWeather_api_key}")
    weatherJson = json.loads(weatherResponse.text)
    parsed_data.append(*[parse_item(item) for item in weatherJson['data']])
dfWeather = pd.DataFrame.from_dict(parsed_data)
dfWeather.to_sql("weather", engine, index=False, if_exists='append', method=insert_on_conflict_nothing)
