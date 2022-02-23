from flask import Flask
from random import random
from models import police_tweets, pyrosvestiki_tweets
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import geocoder
import requests
import datetime
import os

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

def format_text(text):
    '''
    format_text(text)
    Parameters: 
    text (String): Plain text
    Return:
    formatted_text (String): HTML text (including hashtags and links)
    '''
    text_list = text.split(' ')

    for idx, word in enumerate(text_list):
        if word.startswith("http"):
            text_list[idx] = '<a href="{}">{}</a>'.format(word,word) 
        elif word.startswith("#"):
            text_list[idx] = '<a href="https://twitter.com/hashtag/{}">{}</a>'.format(word[1:], word)
        else:
            pass
    formatted_text =  " ".join(text_list)

    return formatted_text

def get_location(text):
    capital_words = ''
    for word in text.split()[1:]:           
        unicode = ord(word[0])
        if unicode >= 913 and unicode <= 937:
            capital_words = word + ','

    geo = geocoder.osm(capital_words)
    # Suppose all tweets concern places in Greece!
    if geo.country_code == 'gr':
        # add a slight randomness to the location to avoid two markers on leaflet to overlap 100%
        location = f"SRID=4326;POINT({geo.lng} {geo.lat+random()/1000})"
    else: 
        location = None

    return location

def get_all_tweets(account):
    '''
    get_all_tweets(user_id)
    Parameters:
    user_id (String) : 

    '''
    parameters = {
        "max_results": "100",
        "expansions": ["author_id"],
        "tweet.fields": "created_at",
    }

    r_json = get_tweets(account, parameters)

    while "next_token" in r_json["meta"]:
        save_tweets(r_json)
        parameters["pagination_token"] = r_json["meta"]["next_token"]
        r_json = get_tweets(account, parameters)

    return 0

def get_tweets(account, parameters):
    user_id = USER_IDS[account]
    r = requests.get(
        auth=BearerAuth(TWITTER_TOKEN),
        url="https://api.twitter.com/2/users/{}/tweets".format(user_id),
        params=parameters,
    )
    print(f"Last twitter: {r.json()['data'][0]['created_at']}")
    print(f"Fetched {len(r.json()['data'])} new tweets")
    return r.json()

def save_tweets(r_json):
    author_id = r_json["data"][0]['author_id']
    if author_id == USER_IDS["hellenic_police"]:
        flag = 1 
    else: 
        flag = 0

    for tweet in r_json["data"]:
        # the id of the tweet 
        id = tweet["id"]

        # the datetime for the timestamp of the tweet creation (ISO with timezone)
        created_at = datetime.datetime.strptime(
            tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
        )
        # the content of the tweet. The processing incorporates links for the HTML content 
        text = format_text(tweet["text"])

        # get the location via geocoding analysis
        location = get_location(tweet["text"])

        if flag:
            new_tweet = police_tweets(
                id=id,
                text=text,
                created_at=created_at,
                location=location
            )
        else:
            new_tweet = pyrosvestiki_tweets(
                id=id,
                text=text,
                created_at=created_at,
                location=location
                # location=f"SRID=4326;POINT({random()*4+23} {random()*4+37})"
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
        row.location = f"SRID=4326;POINT({random()*7+21} {random()*7+39})"
    session.commit()
    return None

if __name__ == "__main__":
    # make get request to get the tweets from twitter API
    # newest_id = session.query(pyrosvestiki_tweets.id).order_by(pyrosvestiki_tweets.id.desc()).first()
    # parameters = {"max_results":"10","since_id": newest_id, "expansions":["geo.place_id,author_id"], "tweet.fields":"created_at"}

    # parameters = {
    #     "max_results": "100",
    #     "expansions": ["geo.place_id,author_id"],
    #     "tweet.fields": "created_at",
    # }

    # r_json = get_tweets("pyrosvestiki", parameters)
    # save_tweets(r_json)

    get_all_tweets("pyrosvestiki")
