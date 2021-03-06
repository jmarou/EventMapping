import datetime
import os
import random
import requests

import geocoder

from db.models import police_tweets, pyrosvestiki_tweets
from db.database import db_session


# @hellenicpolice -> 119014566 ||  @pyrosvestiki -> 158003436
USER_IDS = {
    "hellenic_police": 119014566, 
    "pyrosvestiki": 158003436
}
    
# token for twitter API
TWITTER_TOKEN = os.getenv("TOKEN")


class BearerAuth(requests.auth.AuthBase):
    """Authentication for the twitter API with Bearer Token."""

    def __init__(self, token):
        # my TWITTER API TOKEN IS SAVED IN OS ENVIRONMENT
        self.token = TWITTER_TOKEN

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def format_text(text):
    """Gets the tweet's plain text and returns a rich text, including http links and twitter hashtags.

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    formatted_text : str
        The rich text.
    """

    text_list = text.split(" ")

    for idx, word in enumerate(text_list):
        if word.startswith("http"):
            text_list[idx] = '<a href="{}">{}</a>'.format(word, word)
        elif word.startswith("#"):
            text_list[idx] = '<a href="https://twitter.com/hashtag/{}">{}</a>'.format(
                word[1:], word
            )
        else:
            pass
    formatted_text = " ".join(text_list)

    return formatted_text


def get_location(text):
    """Gets the tweet's plain text and returns the location as WKT (POINT(lng lat)).

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    location : str
        The geolocation as WKT (Well known text).
    """

    capital_words = ""
    for word in text.split()[1:]:
        unicode = ord(word[0])
        if unicode >= 913 and unicode <= 937:
            capital_words = word + ","

    geo = geocoder.osm(capital_words)
    # Suppose all tweets concern places in Greece!
    if geo.country_code == "gr":
        # add a slight randomness to the location to avoid two markers on leaflet to overlap 100%
        location = f"SRID=4326;POINT({geo.lng} {geo.lat + random.random()/1000})"
    else:
        location = None

    return location


def get_tweets(account, parameters):
    """
    Gets the account name of the twitter user and a set of parameters and returns the last tweets
    from their timeline.

    Parameters
    ----------
    account : str
        The account name.

    Returns
    ----------
    r.json : dict
        A python dictionary with the response from twitter API v2.
    """

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
    """Gets the Python dictionary (json object) from the twitter API and inserts the data to the database.

    Parameters
    ----------
    text : str
        The input text.

    Returns
    ----------
    formatted_text : str
        The rich text.
    """

    author_id = r_json["data"][0]["author_id"]

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
                id=id, text=text, created_at=created_at, location=location
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
            with db_session() as session:
                session.add(new_tweet)
                session.commit()
        except:
            print(
                f"The {new_tweet.__tablename__} tweet with id {new_tweet.id} already exists in DB!"
            )


def initialize_DB_tables(account):
    """
    Populates the database table that corresponds to the account by fetching the maximum number
    of tweets (according to the twitter API key).

    Parameters
    ----------
    account : str
        The account name.

    Returns
    ----------
    None
    """

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
    return None


if __name__ == "__main__":
    initialize_DB_tables("hellenic_police")
    initialize_DB_tables("pyrosvestiki")
