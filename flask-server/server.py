from flask import Flask, render_template, send_from_directory, jsonify
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import functions
from models import pyrosvestiki_tweets, police_tweets
import json

engine = create_engine("postgresql://testuser:testpassword@localhost/eventmapping")
meta = MetaData()
DBSession = sessionmaker(bind=engine)
session = DBSession()

# app = Flask(__name__, static_url_path='/', static_folder='../client/')
app = Flask(__name__, static_url_path="/", static_folder="../client/build")

@app.route("/")
def homepage():
    return send_from_directory("../client/build", "index.html")
    # return send_from_directory("../client/public", "index.html")

@app.route("/GetLayer_Pyrosvestiki")
def GetLayer_Pyrosvestiki():
    query = session.query(functions.ST_AsGeoJSON(pyrosvestiki_tweets)).all()
    geojson = ""
    for tweet in query:
        geojson += str(tweet)[2:-3] + ","
    geojson = (
        '{"type": "FeatureCollection","features": ['
        + geojson[:-1]
        + '], "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::4326"}}}'
    )
    return geojson

@app.route("/GetLayer_Police")
def GetLayer_Police():
    query = session.query(functions.ST_AsGeoJSON(police_tweets)).limit(1)
    geojson = ""
    for tweet in query:
        geojson += str(tweet)[2:-3] + ","

    geojson = (
        '{"type": "FeatureCollection","features": ['
        + geojson[:-1]
        + '], "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::4326"}}}'
    )
    return geojson


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)