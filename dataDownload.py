import pandas as pd
import requests
from config import *
from sqlalchemy import create_engine
import json

engine = create_engine(dblink)
SQLQuery = """
SELECT * FROM availability;
"""

dfAvailability = pd.read_sql(SQLQuery, engine)
dfAvailability['last_update_ymd'] = pd.to_datetime(dfAvailability['last_update'],unit="ms")


weatherResponse = requests.get(f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={53}&lon={-6}&dt={1707942432000}&appid={OpenWeather_api_key}")

weather_json = json.loads(weatherResponse.text)
