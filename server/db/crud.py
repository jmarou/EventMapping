from datetime import datetime
from typing import Any, List

import geoalchemy2.functions as geo_func
from sqlalchemy.sql import text

from db.database import db_session
from db.models import PyrosvestikiTweets, PoliceTweets
from operations.core import format_text, calc_location
from operations.twitter import (ACCOUNT_IDS, download_tweets)


def str2department(department: str):
    """Given the name of the department returns its database class
    """
    if department == "Police":
        return PoliceTweets
    elif department == "Pyrosvestiki":
        return PyrosvestikiTweets
    else:
        raise ValueError


def get_tweets_with_location(department: str) -> Any:
    """
    Gets the department name and returns a query result containing all the rows 
    with a valid location information.
    """
    departmentTable = str2department(department=department)
    
    with db_session() as session:
        query = session.query(geo_func.ST_AsGeoJSON(departmentTable)).where(
            departmentTable.location != None
        )

    return query


def get_tweets_with_filter(department: str, order_by: str = None, 
                           order: str = 'ASC', limit: int = None,
                           location_only: bool = True) -> Any:
    departmentTable = str2department(department=department)

    # where_clause = ''
    # if limit is not None:
    #     where_clause += f' LIMIT({limit})'
    # if order_by in departmentTable.__table__.columns.keys():
    #     where_clause += f' ORDER BY {order_by}'
    #     if order == 'DESC' or order == 'desc':
    #         where_clause += ' DESC'
    #     else: 
    #         where_clause += ' ASC'
    # if location_only:
    #     where_clause += f' WHERE {departmentTable.__tablename__}'

    # print(where_clause)

    

    with db_session() as session:
        query = session.query(departmentTable).filter(text(where_clause))
    
    return query


def save_tweets(r_data: List) -> None:
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
    author_id = r_data[0]["author_id"]

    if author_id == ACCOUNT_IDS["hellenic_police"]:
        department_tweets = PoliceTweets
    elif author_id == ACCOUNT_IDS["pyrosvestiki"]:
        department_tweets = PyrosvestikiTweets
    else: 
        raise ValueError

    # TODO: First check if tweet exists in database
    for tweet in r_data:
        # the id of the tweet
        id = tweet["id"]
        # the datetime for the timestamp of the tweet creation (ISO with timezone)
        created_at = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")       
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
                print(f"The {new_tweet.__tablename__} tweet with id "\
                    f"[{new_tweet.id}] is saved in the database!"
                )
        except:
            print(
                f"The {new_tweet.__tablename__} tweet with id {new_tweet.id} already exists in DB!"
            )
    return None
