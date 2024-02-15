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
