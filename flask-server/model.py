import sqlite3 
import sqlalchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tweets.sqlite"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:123@localhost/eventmapping"
db = SQLAlchemy(app)


class pyrosvestiki_tweets(db.Model):
    __tablename__ = 'pyrosvestiki_tweets'

    def __init__ (self, id, text, lon=0, lat=0):
        self.id = id
        self.text = text 
        self.lon = lon 
        self.lat = lat
  
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280)) # limit of characters for a single tweet
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    def __repr__(self):
        return '<pyrosvestiki_tweets %s>' % (self.text)

class police_tweets(db.Model):
    __tablename__ = 'police_tweets'

    def __init__ (self, id, text, lon=0, lat=0):
        self.id = id
        self.text = text 
        self.lon = lon 
        self.lat = lat
  
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(280)) # limit of characters for a single tweet
    lon = db.Column(db.Float)
    lat = db.Column(db.Float)

    def __repr__(self):
        return '<police_tweets %s>' % (self.text)

def initDb():
    db.create_all()