import pandas as pd
from flask import Flask, g, render_template, jsonify
from sqlalchemy import create_engine
import json
from config import *

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
engine = create_engine(dblink)


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/stations')
def get_stations():
    stations = pd.read_sql_table('station', engine)
    return stations.to_json(orient='index')


# Still working on this, not functioning yet.
# @app.route("/available/<int:station_id>")
# def get_station():
#     data = []
#     rows = engine.execute(f"SELECT available_bikes from stations where number = {station_id};")
#     for row in rows:
#         data.append(dict(row))
#     return jsonify(available=data)


if __name__ == "__main__":
    app.run(debug=True)
