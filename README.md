![Eventmapping-github](https://user-images.githubusercontent.com/26281506/155498608-8f71868e-bbfb-4759-afc5-c3353a1ac249.png)

EventMapping is an open-source project developed in the context of the course _Modern Web Applications_ of <a href="https://www.ece.ntua.gr/en/postgraduate/2">MBA: Engineering - Economics Systems</a> hosted by <a href="https://www.ntua.gr/en/">NTUA</a> & <a href="https://www.unipi.gr/unipi/en/">UNIPI</a>.

The project focuses on parsing tweets from the twitter accounts of <a href="https://twitter.com/hellenicpolice">👮🏽‍♀️ #Hellenic_police</a> and <a href="https://twitter.com/pyrosvestiki">👩🏼‍🚒  #Pyrosvestiki</a> and display them on a WebGIS map.

## Documentation
Please see the <a href="https://github.com/jmarou/EventMapping/wiki">🕮 wiki</a>. For further information and demonstration contact 📨  johnmaroufidis@gmail.com 

## Languages & Libraries
![Python](https://img.shields.io/badge/Python-%23323330?style=flat&logo=python&logoColor=%155509708) ![Flask](https://img.shields.io/badge/flask-%23323330.svg?style=flat&logo=Flask&logoColor=white) ![Postgres](https://img.shields.io/badge/PostgreSQL-%23323330.svg?style=flat&logo=postgresql&logoColor=%23316192) 

![HTML5](https://img.shields.io/badge/html5-%23323330.svg?style=flat&logo=HTML5&logoColor=23E34F26) ![CSS3](https://img.shields.io/badge/CSS3-%23323330.svg?style=flat&logo=css3&logoColor=%231572B6) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=flat&logo=Javascript&logoColor=%23F7DF1E) ![Leaflet](https://img.shields.io/badge/Leaflet.js-%23323330.svg?style=flat&logo=leaflet&logoColor=199900) ![React](https://img.shields.io/badge/React.js-%23323330.svg?style=flat&logo=react&logoColor=23E34F26) 

## 🌟 Preview 
<img width="1790" alt="image" src="https://user-images.githubusercontent.com/26281506/222982233-06a2c8f6-2adb-4f33-963d-2ca5963134f0.png">

## Get Started


## 1. Twitter API
In order to be able to make API calls to the twitter API you must have a bearer token. 

See how to inquire twitter API token: [Twitter API v2](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api)

The end point used for fetching and pulling the tweets is: [Timelines ](https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/quick-start). With free account, this endpoint fetches the last 3200 tweets.

1. Save the Token saved as environment variable 'TOKEN'. Using python venv go to {env_name}/bin/activate and paste export TOKEN=xxxxxxxxxxxxxx


## 2. How to install backend
Backend: [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/en/2.0.x/).
To install go to server folder and run (with [pip](https://pip.pypa.io/en/stable/)): 

* `pip install -r requirements.txt`

We recommend using a virtual python environment such as [venv](https://docs.python.org/3/library/venv.html)

## 3. Install the front end 
Front end: [React.js](https://reactjs.org/), [Leaflet.js](https://leafletjs.com/).
To install cd to client and run (with [npm](https://www.npmjs.com/)):

1. Download and install [node.js](https://nodejs.org/en/download/)
2. `npm install`
3. `npm run build`

## 4. Run the application
To run the application (in localhost), from the server folder run the following command:

* `python3 server.py`

Open [http://localhost:5000](http://localhost:5000) to view it in your browser.
