from sqlalchemy import create_engine, MetaData, insert
from sqlalchemy.orm import sessionmaker
from flask import Flask
from models import police_tweets, pyrosvestiki_tweets
import requests
import datetime
import os
from random import random

# connection to Postgresql + PostGIS Database
engine = create_engine("postgresql://testuser:testpassword@localhost/eventmapping")
meta = MetaData()

# create session for interaction with DB
DBSession = sessionmaker(bind=engine)
session = DBSession()

# @hellenicpolice -> 119014566 ||  @pyrosvestiki -> 158003436
USER_IDS = {"hellenic_police": 119014566, "pyrosvestiki": 158003436}

# token for twitter API
TWITTER_TOKEN = os.getenv("TOKEN")

class BearerAuth(requests.auth.AuthBase):
    """
    Authentication for the twitter API with Bearer Token
    """

    def __init__(self, token):
        self.token = TWITTER_TOKEN  # my TWITTER API TOKEN IS SAVED IN OS ENVIRONMENT

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def get_all_tweets(user_id, parameters):

    r = get_tweets(USER_IDS[user_id], parameters)

    if int(r["data"][0]["author_id"]) == USER_IDS["hellenic_police"]:
        flag = 1
    else:
        flag = 0

    while r["meta"]["next_token"]:
        for idx, tweet in enumerate(r["data"]):
            # author_id = tweet['author_id']
            id = tweet["id"]
            text = tweet["text"]
            created_at = datetime.datetime.strptime(
                tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
            )

            if flag:
                new_tweet = police_tweets(
                    id=id,
                    text=text,
                    created_at=created_at,
                    location=f"SRID=4326;POINT({random()*4+23} {random()*4+37})",
                )
            else:
                new_tweet = pyrosvestiki_tweets(
                    id=id,
                    text=text,
                    created_at=created_at,
                    location=f"SRID=4326;POINT({random()*4+23} {random()*4+37})",
                )

            session.add(new_tweet)
            session.commit()

            parameters["pagination_token"] = r["meta"]["next_token"]
            r = get_tweets(USER_IDS[user_id], parameters)
    return 0

def get_tweets(user_id, parameters):
    r = requests.get(
        auth=BearerAuth(TWITTER_TOKEN),
        url="https://api.twitter.com/2/users/{}/tweets".format(user_id),
        params=parameters,
    )
    print(f"Last twitter: {r.json()['data'][0]['created_at']}")
    print(f"Fetched {len(r.json()['data'])} new tweets")
    return r.json()

def save_tweets(r):
    """
    Function to save the tweets in the Database.
    r: response type
    """
    for idx, tweet in enumerate(r["data"]):
        # author_id = tweet['author_id']
        id = tweet["id"]
        text = tweet["text"]
        created_at = datetime.datetime.strptime(
            tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        if new_tweet.__tablename__ == "hellenic_police":
            # new_tweet = police_tweets(id=id, text=text, created_at=created_at)
            new_tweet = police_tweets(
                id=id,
                text=text,
                created_at=created_at,
                location=f"SRID=4326;POINT({random()*4+23} {random()*4+37})",
            )
        else:
            # new_tweet = pyrosvestiki_tweets(id=id, text=text, created_at=created_at)
            new_tweet = pyrosvestiki_tweets(
                id=id,
                text=text,
                created_at=created_at,
                location=f"SRID=4326;POINT({random()*4+23} {random()*4+37})",
            )
        try:
            session.add(new_tweet)
            session.commit()
        except:
            print(
                f"The {new_tweet.__tablename__} tweet with id {new_tweet.id} already exists in DB!"
            )

def update_location(tweets):
    for row in session.query(tweets):
        # put random locations
        row.location = f"SRID=4326;POINT({random()*4+23} {random()*4+37})"
    session.commit()
    return None

if __name__ == "__main__":
    # make get request to get the tweets from twitter API
    # newest_id = session.query(pyrosvestiki_tweets.id).order_by(pyrosvestiki_tweets.id.desc()).first()
    # print(newest_id)
    # parameters = {"max_results":"100","since_id": newest_id, "expansions":["geo.place_id,author_id"], "tweet.fields":"created_at"}
    # r = get_tweets(USER_IDS["pyrosvestiki"], parameters)

    # parameters = {
    #     "max_results": "100",
    #     "expansions": ["geo.place_id,author_id"],
    #     "tweet.fields": "created_at",
    # }
    # get_all_tweets("hellenic_police", parameters)
    update_location(police_tweets)
    