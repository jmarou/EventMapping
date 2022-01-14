# EventMapping
The goal of this project is to map the events uploaded in the twitter accounts of @hellenicpolice and @pyrosvestiki in an online WFS layer.

The front end is developed using ReactJS and LeafletJS.
The backend is developed using Python and flask.

In order to run the application:
First build the front end:
Inside the client folder run the following commands:
- npm install
- npm run build 

In order to be able to make API calls to the twitter API you must have a bearer token saved in the environment with name 'TOKEN'.

Inside the flask-server folder run the following commands:
- pip install -r requirements.txt
- python3 server.py


Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.