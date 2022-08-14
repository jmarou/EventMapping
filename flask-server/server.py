from flask import Flask, send_from_directory, request

# from operations.core import get_layer_as_geojson, get_layer_as_table

app = Flask(__name__, static_url_path="/", static_folder="../client/build")


@app.route("/")
def homepage():
    return send_from_directory("../client/build", "index.html")


@app.route("/getLayer", methods=["GET"])
def getLayer():
    
    return get_layer_as_geojson(request.args.get("department"))

if __name__ == "__main__":
    # app.run(host="localhost", debug=True)
    query2 = get_layer_as_table(department='Police')
    print("as")
