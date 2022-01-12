from flask import Flask, render_template, send_from_directory

# app = Flask(__name__, static_url_path='/', static_folder='../client/build')
app = Flask(__name__, static_url_path='/', static_folder='../client/build')

# Routes 

@app.route('/')
def homepage():
    return send_from_directory("../client/build", "index.html")
    # return send_from_directory("../client/public", "index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)