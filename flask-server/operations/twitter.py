import datetime
import os
import requests

from db.database import db_session
from db.models import police_tweets, pyrosvestiki_tweets, USER_IDS
from operations.core import calculate_location, format_text
   
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


def download_tweets(account: int, parameters: dict) -> dict:
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
        auth = BearerAuth(TWITTER_TOKEN),
        url = "https://api.twitter.com/2/users/{}/tweets".format(user_id),
        params = parameters,
    )
    print(f"Last twitter: {r.json()['data'][0]['created_at']}")
    print(f"Fetched {len(r.json()['data'])} new tweets")
    return r.json()


def save_tweets(r_json: dict) -> None:
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
        department_tweets = police_tweets
    else: 
        department_tweets = pyrosvestiki_tweets

    for tweet in r_json["data"]:
        # the id of the tweet
        id = tweet["id"]
        # the datetime for the timestamp of the tweet creation (ISO with timezone)
        created_at = datetime.datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")       
        # the content of the tweet. The processing incorporates links for the HTML content
        text = format_text(tweet["text"])
        # get the location via geocoding analysis
        location = calculate_location(tweet["text"])
        new_tweet = department_tweets(
                id=id,
                text=text,
                created_at=created_at,
                location=location
        )
        try:
            with db_session() as session:
                session.add(new_tweet)
                session.commit()
        except:
            print(
                f"The {new_tweet.__tablename__} tweet with id {new_tweet.id} already exists in DB!"
            )
    return None


def initialize_DB_tables(account: str) -> None:
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

    r_json = download_tweets(account, parameters)

    while "next_token" in r_json["meta"]:
        save_tweets(r_json)
        parameters["pagination_token"] = r_json["meta"]["next_token"]
        r_json = download_tweets(account, parameters)
    return None


if __name__ == "__main__":
    initialize_DB_tables("hellenic_police")
    initialize_DB_tables("pyrosvestiki")
