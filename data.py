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
