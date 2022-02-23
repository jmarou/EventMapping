from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    DateTime,
    BIGINT,
    inspect,
)
from geoalchemy2 import Geometry, functions
import geoalchemy2
from sqlalchemy.orm import declarative_base, sessionmaker
from models import police_tweets, pyrosvestiki_tweets
import json
import requests
import os
import datetime
import decimal


class tweetEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)


engine = create_engine("postgresql://testuser:testpassword@localhost/eventmapping")
meta = MetaData()
DBSession = sessionmaker(bind=engine)
session = DBSession()

# a = session.query(pyrosvestiki_tweets).first()
tweets = session.query(functions.ST_AsGeoJSON(pyrosvestiki_tweets)).limit(5).all()
b = ""

# for tweet in tweets:
#     b += json.loads([r for r in tweet], default=alchemyencoder,ensure_ascii=False,separators=(',',':'))
# b = b[2:-2]
# print(b)
tweets = session.query(functions.ST_AsGeoJSON(pyrosvestiki_tweets)).all()
geojson = ""
for tweet in tweets:
    geojson += str(tweet)[2:-3]

print(geojson)


# tweetEncoder().encode(a)
# b = json.dumps(a, indent=4,sort_keys=True, default=str)

# print(a)
#%%
"""
This file exists only for testing 
It could be totally empty as well.
"""

# class BearerAuth(requests.auth.AuthBase):
#     def __init__(self, token):
#         self.token = token  # this is to get it from the Environment Variable called TOKEN
#     def __call__(self, r):
#         r.headers["authorization"] = "Bearer " + self.token
#         return r

# parameters = {"id": "fadf"}

# r = requests.get(
#     url = "https://api.twitter.com/2/tweets",
#     auth = BearerAuth(os.getenv('TOKEN')),
#     params = parameters
# )
# print(r.json())
# print(r.status_code)
