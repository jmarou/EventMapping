from flask import Flask, send_from_directory
from geoalchemy2 import functions

from db.models import pyrosvestiki_tweets, police_tweets
from db.database import db_session

app = Flask(__name__, static_url_path="/", static_folder="../client/build")


@app.route("/")
def homepage():
    return send_from_directory("../client/build", "index.html")


@app.route("/getLayer/<department>", methods=["GET"])
def getLayer(department):
    departmentTable = (
        police_tweets if department == "police_tweets" else pyrosvestiki_tweets
    )

    with db_session() as session:
        query = session.query(functions.ST_AsGeoJSON(departmentTable)).where(
            departmentTable.location != None
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
