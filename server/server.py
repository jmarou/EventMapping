from flask import Flask, send_from_directory, request


from db.crud import get_tweets_with_location
from operations.core import format_geojson
# from operations.twitter import post_new_tweets_to_db


app = Flask(__name__, static_url_path="/", static_folder="../client/build")


def get_layer_as_geojson(department: str = None):
    return format_geojson(get_tweets_with_location(department))


@app.route("/")
def homepage():
    return send_from_directory("../client/build", "index.html")


@app.route("/getLayer", methods=["GET"])
def getLayer():
    return get_layer_as_geojson(request.args.get("department"))


@app.route("/downloadTweets", methods=["POST"])
def downloadNewTweets():
    pass 


if __name__ == "__main__":
    app.run(host="localhost", debug=True)
    # query2 = get_layer_as_table(department='Police')
    # query2 = get_layer_as_geojson(department='Police')
