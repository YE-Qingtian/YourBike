"""
This is the main app.
"""
from flask import Flask, g, render_template, jsonify
from sqlalchemy import create_engine
import json
from config import *

app = Flask(__name__, static_url_path='')
app.config.from_object('config')


def connect_to_database():
    engine = create_engine(dblink)
    return engine


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db


# @app.route("/available/<int:station_id>")
# def get_stations():
#     engine = get_db()
#     data = []
#     rows = engine.execute(f"SELECT available_bikes from stations where number = {station_id};")
#     for row in rows:
#         data.append(dict(row))
#     return jsonify(available=data)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/stations')
def get_stations():
    conn = get_db()


if __name__ == "__main__":
    app.run(debug=True)
