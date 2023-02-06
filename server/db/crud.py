from datetime import datetime
from typing import Any, List, Union

from db.database import db_session
from db.models import PyrosvestikiTweets, PoliceTweets
from operations.core import format_text, geocoding_osm
from operations.twitter import ACCOUNT_IDS


def str2department(department: str):
    """Given the name of the department returns its database class
    """
    if department.lower() == "police":
        return PoliceTweets
    elif department.lower() == "pyrosvestiki":
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
        query = session.query(departmentTable).where(
            departmentTable.latitude!=None
        ).where(departmentTable.category>-1)

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
    # with db_session() as session:
    #     query = session.query(departmentTable).filter(text(where_clause))
    
    return None
    # return query


def save_tweets(tweet: Union[dict, List]) -> None:
    """
    Gets a tweet or a list of tweets and writes them to the database   

    Parameters
    ----------
    text : Union[dict, List[dict]]
        The tweets.

    Returns
    ----------
    None
    """
    # if only one tweet, create a list with 1 tweet in it
    if isinstance(tweet, dict):
        tweets = [tweet]

    # TODO: First check if tweet exists in database
    for tweet in tweets:
        new_tweet = create_new_tweet(tweet)
        try:
            with db_session() as session:
                session.add(new_tweet)
                session.commit()
                print(f"The {new_tweet.__tablename__} tweet with id "\
                    f"[{new_tweet.id}] is saved in the database!"
                )
        except:
            print(f"The {new_tweet.__tablename__} tweet with id {new_tweet.id} \
                  already exists in DB!")
    return None


def create_new_tweet(tweet: dict) -> Union[PoliceTweets,
                                           PyrosvestikiTweets]:
    """
    Converts a tweet from a dictionary object to database model object class

    Parameters
    ----------
    tweet : dict
        The tweet as python dictionary (json format)

    Returns
    ----------
    _ : db.models 
        The tweet as db.model (PoliceTweets or PyrosvestikiTweets)
    """
    author_id = tweet["author_id"]

    if author_id == ACCOUNT_IDS["hellenic_police"]:
        departmentTable = PoliceTweets
    elif author_id == ACCOUNT_IDS["pyrosvestiki"]:
        departmentTable = PyrosvestikiTweets
    else: 
        raise ValueError

    # the id of the tweet
    id = tweet["id"]

    # the datetime for the timestamp of the tweet creation (ISO with timezone)
    created_at = datetime.strptime(tweet["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z")       
    
    # the content of the tweet. 
    # The processing incorporates links for the HTML content
    text = format_text(tweet["text"])
    
    # get the location via geocoding analysis
    longitude, latitude = geocoding_osm(tweet["text"])
    return departmentTable(
                id=id,
                text=text,
                created_at=created_at,
                longitude=longitude,
                latitude=latitude
           )

