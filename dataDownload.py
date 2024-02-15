import pandas as pd
from config import *
from sqlalchemy import create_engine


engine = create_engine(dblink)
SQLQuery = """
SELECT * FROM availability;
"""

dfAvailability = pd.read_sql(SQLQuery, engine)
dfAvailability['last_update'] = pd.to_datetime(dfAvailability['last_update'],unit="ms")