from typing import Any

import geoalchemy2.functions as geo_func

from db.database import db_session
from db.models import PyrosvestikiTweets, PoliceTweets
from operations.twitter import (DEFAULT_TWEET_PARAMETERS, ACCOUNT_IDS,
                                download_tweets)


def get_tweets_with_location(department: str) -> Any:
    """
    Gets the department name and returns a query result containing all the rows 
    with a valid location information.
    """
    departmentTable = \
        PoliceTweets if department == "Police" else PyrosvestikiTweets
    
    with db_session() as session:
        query = session.query(geo_func.ST_AsGeoJSON(departmentTable)).where(
            departmentTable.location != None
        )

    return query


def initialize_DB_tables(account: str) -> None:
    """
    Populates the database table that corresponds to the account by fetching the
    maximum number of tweets (according to the twitter API key).

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


def save_tweets(r_json: dict) -> None:
    """
    Gets the Python dictionary (json object) from the twitter API and inserts
    the data to the database.

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
        department_tweets = PoliceTweets
    else: 
        department_tweets = PyrosvestikiTweets

    for tweet in r_json["data"]:
        # the id of the tweet
        id = tweet["id"]
        # the datetime for the timestamp of the tweet creation (ISO with timezone)
        created_at = datetime.datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")       
        # the content of the tweet. The processing incorporates links for the HTML content
        text = format_text(tweet["text"])
        # get the location via geocoding analysis
        location = calc_location(tweet["text"])
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


def post_new_tweets_to_db(account: dict = ACCOUNT_IDS,
                          parameters: dict = DEFAULT_TWEET_PARAMETERS) -> None:
    try: 
        for account_id in account.values(): 
            save_tweets(download_tweets(account, parameters))
    except Exception as e: 
        print(e.message, e.args)
    
    return True


if __name__ == "__main__":
    # initialize_DB_tables("hellenic_police")
    # initialize_DB_tables("pyrosvestiki")
    post_new_tweets_to_db()
