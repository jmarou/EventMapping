from flask import Flask, render_template, send_from_directory, jsonify
from models import pyrosvestiki_tweets, police_tweets
from sqlalchemy import create_engine, MetaData
from geoalchemy2 import functions
from sqlalchemy.orm import sessionmaker
import json

app = Flask(__name__, static_url_path="/", static_folder="../client/build")

engine = create_engine("postgresql://testuser:testpassword@localhost/eventmapping")
meta = MetaData()
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/")
def homepage():
    return send_from_directory("../client/build", "index.html")


@app.route("/GetLayer_Pyrosvestiki")
def GetLayer_Pyrosvestiki():
    '''
    Loads the table "pyrosvestiki_tweets" from DB as geoJSON to display @leaflet.js
    '''
    query = session.query(functions.ST_AsGeoJSON(pyrosvestiki_tweets)).where(
        pyrosvestiki_tweets.location != None
    )
    geojson = ""
    for tweet in query:
        geojson += tweet[0] + ","
    geojson = (
        '{"type": "FeatureCollection","features": ['
        + geojson[:-1]
        + '], "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::4326"}}}'
    )
    return geojson


@app.route("/GetLayer_Police")
def GetLayer_Police():
    '''
    Loads the table "police_tweets" from DB as geoJSON to display @leaflet.js
    '''
    query = session.query(functions.ST_AsGeoJSON(police_tweets)).where(
        police_tweets.location != None
    )
    geojson = ""
    for tweet in query:
        geojson += tweet[0] + ","
    geojson = (
        '{"type": "FeatureCollection","features": ['
        + geojson[:-1]
        + '], "crs":{"type":"name","properties":{"name":"urn:ogc:def:crs:EPSG::4326"}}}'
    )
    return geojson


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
