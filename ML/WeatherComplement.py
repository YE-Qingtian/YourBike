"""
Unfinished
"""
import pandas as pd
import requests
from config import *
from sqlalchemy import create_engine

engine = create_engine(dblink)

weatherStart = pd.to_datetime('1707990000000',unit='ms')
availabilityStart = pd.to_datetime('1707933824000',unit='ms')
availability_query = "SELECT * FROM availability"
availability_df = pd.read_sql(availability_query, engine)
