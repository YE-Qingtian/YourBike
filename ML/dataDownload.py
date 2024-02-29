import pandas as pd
import requests
from config import *
from sqlalchemy import create_engine

engine = create_engine(dblink)

availability_query = "SELECT * FROM availability"
station_query = "SELECT * FROM station"
weather_query = "SELECT * FROM weather"

availability_df = pd.read_sql(availability_query, engine)
station_df = pd.read_sql(station_query, engine)
weather_df = pd.read_sql(weather_query, engine)

# Convert timestamps to pandas datetime format
availability_df['last_update'] = pd.to_datetime(availability_df['last_update'], unit='ms')
weather_df['dt'] = pd.to_datetime(weather_df['dt'], unit='s')

# Round weather timestamps to match availability update frequency
weather_df['dt_rounded'] = weather_df['dt'].dt.round('5min')

# Merge availability and station data
station_df['number'] = pd.to_numeric(station_df['number'])
combined_df = pd.merge(availability_df, station_df, on='number')


# Function to find nearest weather record for each availability record
def find_nearest_weather(row):
    nearest_time = row['last_update'].round('5min')
    return weather_df.loc[(weather_df['dt_rounded'] - nearest_time).abs().idxmin()]


# Apply the function to find nearest weather for each row in combined_df
nearest_weather = combined_df.apply(find_nearest_weather, axis=1)

# Merge the nearest weather data with the combined_df
final_df = pd.concat([combined_df, nearest_weather], axis=1)
final_df.to_parquet('AvailabilityDataCombined.gzip', compression='gzip')
final_df.to_csv('AvailabilityDataCombined.csv')
