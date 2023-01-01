import os
import json
from datetime import datetime

import pandas as pd
from sqlalchemy.sql import func

from db.database import db_session
from db.crud import str2department
from operations.core import (find_woi_in_text, calc_location, 
    remove_links_emojis, get_capital_words, translate_text,
    geograpy_woi, categorize_tweet)


def db_to_excel(department: str, file: str, sheet_name: str = None,
                original: bool = False) -> None:
    """
    Reads rows from a database table and writes the result to a new sheet
    in an xlsx file. If the specified output already exists it appends the
    new sheet.

    Parameters
    ----------
    department: str
        The name of the department.
    file: str
        The absolute or relative path of the output xlsx file.
    sheet_name: str
        The name of the sheet to write to.
    original: bool
        True if we want the original tweet text or False for text without
        emojis and/or links.

    Returns
    ----------
    None
    """
    departmentTable = str2department(department)

    if sheet_name is None:
        sheet_name = 'Sheet1'

    tweet_df = pd.DataFrame()
    
    with db_session() as session:
        # rows = session.query(departmentTable).limit(100)
        rows = session.query(departmentTable).order_by(
            func.random()).limit(100)

    # tweet_df['id'] = [str(row.id) for row in rows]
    tweet_df['original_text'] = [row.text for row in rows]

    if original:
        tweet_df['text'] = [row.text for row in rows]
    else:
        tweet_df['text'] = [remove_links_emojis(row.text) for row in rows]
    
    # tweet_df['created_at'] = [row.created_at for row in rows]

    ##### Add processing values from the methods
    # Capital words column
    tweet_df['capital_words'] = tweet_df['text'].apply(
        lambda text: get_capital_words(text)) 

    # Regex WOI
    tweet_df['regex_woi'] = tweet_df['text'].apply(
        lambda text: find_woi_in_text(text))

    # Translated text using deepL
    tweet_df['translated'] = tweet_df['text'].apply(
        lambda text: translate_text(text))

    # Geograpy WOI
    tweet_df['geograpy_woi'] = tweet_df['translated'].apply(
        lambda translated_text: geograpy_woi(translated_text))

    mode = 'a' if os.path.exists(file+'.xlsx') else 'w'

    writer = pd.ExcelWriter(file+'.xlsx', mode=mode)
    tweet_df.to_excel(writer, sheet_name)
    writer.save()
    
    return None
    
    
def json_to_database(departmentTable, file: str):
    f = open('../pyrosvestiki2.json')
    data = json.load(f)

    for tweet in data["features"]:
        id = tweet["id"]
        text = tweet["properties"]["text"]
        created_at = datetime.strptime(tweet["properties"]["created_at"], 
                                       "%Y/%m/%d %H:%M:%S")
        if tweet["geometry"] == None:
            latitude, longitude = None, None
        else:
            latitude = tweet["geometry"]["coordinates"][0]
            longitude = tweet["geometry"]["coordinates"][1]
        
        new_tweet = departmentTable(
                    id=id,
                    text=text,
                    created_at=created_at,
                    latitude=latitude,
                    longitude=longitude)
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


def update_tweets_category(department: str) -> None:
    """
    Update/calculate the category for all the saved tweets.
    """
    departmentTable = str2department(department=department)

    with db_session() as session:
        all_tweets = session.query(departmentTable).all()

        count = 0
        all_count = len(all_tweets)
        for tweet in all_tweets:
            count+= 1
            print(f'{count/all_count * 100}%')
            tweet.category = categorize_tweet(tweet.plain_text, department)

        session.commit()


def update_tweets_plain_text(department: str) -> None:
    """
    Update/calculate the plain text for all the saved tweets.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        all_tweets = session.query(departmentTable).all()

        count = 0
        all_count = len(all_tweets)
        for tweet in all_tweets:
                count+= 1
                print(f'{count/all_count * 100}%')
                tweet.plain_text = remove_links_emojis(tweet.text)
        
        session.commit()


def update_tweets_regex_woi(department: str) -> None:
    """
    Update/calculate the regex_woi for all the tweets with eligible 
    category representing an event, based on categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        all_tweets = session.query(departmentTable).where(
            departmentTable.category>=0)

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
                count += 1
                print(f'{count/all_count * 100}%')
                tweet.regex_woi = find_woi_in_text(tweet.plain_text)
        
        session.commit()


def update_tweets_capital_words(department: str) -> None:
    """
    Update/calculate the capital_words for all the tweets with eligible
    category representing an event, based on the categorize_tweet function.
    """
    departmentTable = str2department(department)
    
    with db_session() as session:
        all_tweets = session.query(departmentTable).where(
            departmentTable.category>=0)

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
            count += 1
            print(f'{count} / {all_count}')
            tweet.capital_words = get_capital_words(tweet.plain_text)
        
        session.commit()


def update_tweets_translated_text(department: str) -> None:
    """
    Update/calculate the translated_text for all the tweets with eligible 
    category representing an event, based on categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        all_tweets = session.query(departmentTable).where(
            departmentTable.category>=0)

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
                count += 1
                print(f'{count} / {all_count}')
                tweet.translated_text = translate_text(tweet.plain_text)
        
        session.commit()


def update_tweets_location(department: str) -> None:
    """
    Update/calculate the regex_woi for all the tweets with eligible 
    category representing an event, based on categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        all_tweets = session.query(departmentTable).where(
            departmentTable.regex_woi!=None)

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
                count += 1
                print(f'{count} / {all_count}')
                tweet.longitude, tweet.latitude = calc_location(tweet.regex_woi)
                session.commit()
        
        # session.commit()
