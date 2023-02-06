import json
import random
from datetime import datetime
from typing import List

import pandas as pd
from sqlalchemy.sql import func
from db.database import db_session
from db.crud import str2department
from db.models import EVENTS_DICT
from operations.core import (
    regex_woi,
    geocoding_osm,
    remove_links_emojis,
    get_capital_words,
    translate_text,
    geograpy_woi,
    categorize_tweet,
    spacy_woi,
)


def db_to_excel(
    file: str, departments: List[str] = ["police", "pyrosvestiki"], n: int = 100
) -> None:
    """
    Reads rows from a database table and writes the result to a new sheet
    in an xlsx file. If the specified output already exists it appends the
    new sheet.

    Parameters
    ----------
    file: str
        The absolute or relative path of the output xlsx file.
    departments: List[str]
        A list containing the name of the departments
        Default: police, pyrosvestiki.
    n: int
        The number of columns for the test dataset.

    Returns
    ----------
    None
    """
    writer = pd.ExcelWriter(file + ".xlsx", engine="xlsxwriter")

    for department in departments:
        departmentTable = str2department(department)

        tweet_df_category = pd.DataFrame()
        tweet_df = pd.DataFrame()

        with db_session() as session:
            # get all tweets to test the category (and plain_text)
            all_tweets = session.query(departmentTable).all()
            # get all tweets with category >0 to test woi extraction
            all_tweets_pos = (
                session.query(departmentTable)
                .where(departmentTable.category > 0)
                .all()
            )

            # doesn't guarantee unique values!
            ids = random.sample([row.id for row in all_tweets], k=n)
            ids_pos = random.sample([row.id for row in all_tweets_pos], k=n)

            # filter tweets using the random ids
            rows = session.query(departmentTable).filter(
                departmentTable.id.in_(ids)
            )
            rows_pos = session.query(departmentTable).filter(
                departmentTable.id.in_(ids_pos)
            )

        tweet_df_category["text"] = [row.plain_text for row in rows]
        tweet_df_category["category"] = [
            EVENTS_DICT[department][row.category] for row in rows
        ]
        tweet_df_category["ground_truth"] = [
            None for row in rows
        ]  # fill up manually

        tweet_df["text"] = [row.plain_text for row in rows_pos]
        tweet_df["category"] = [
            EVENTS_DICT[department][row.category] for row in rows_pos
        ]
        tweet_df["regex_woi"] = [row.regex_woi for row in rows_pos]
        tweet_df["spacy_woi"] = [row.spacy_woi for row in rows_pos]
        tweet_df["geograpy_woi"] = [row.geograpy_woi for row in rows_pos]
        tweet_df["capital_words"] = [row.capital_words for row in rows_pos]
        tweet_df["ground_truth"] = [None] * n
        tweet_df["regex_woi_precision"] = [None] * n
        tweet_df["regex_woi_recall"] = [None] * n
        tweet_df["regex_woi_f1"] = [None] * n
        tweet_df["spacy_woi_precision"] = [None] * n
        tweet_df["spacy_woi_recall"] = [None] * n
        tweet_df["spacy_woi_f1"] = [None] * n
        tweet_df["geograpy_woi_precision"] = [None] * n
        tweet_df["geograpy_woi_recall"] = [None] * n
        tweet_df["geograpy_woi_f1"] = [None] * n
        tweet_df["capital_words_precision"] = [None] * n
        tweet_df["capital_words_recall"] = [None] * n
        tweet_df["capital_words_f1"] = [None] * n

        tweet_df_category.to_excel(
            writer,
            sheet_name=f"{department}_cat",
            startrow=1,
            header=False,
            index=False,
        )
        tweet_df.to_excel(
            writer,
            sheet_name=department,
            startrow=1, 
            header=False,
            index=False
        )

        # get the worksheet
        worksheet = writer.sheets[department]
        worksheet_cat = writer.sheets[f'{department}_cat']

        # dimensions of the dataframe
        (max_row, max_col) = tweet_df.shape
        # dimensions of the dataframe
        (max_row_cat, max_col_cat) = tweet_df_category.shape

        # create a list of column headers
        column_settings = []
        for header in tweet_df.columns:
            column_settings.append({"header": header})

        column_settings_cat = []
        for header in tweet_df_category.columns:
            column_settings_cat.append({"header": header})

        # add the table with the headers
        worksheet.add_table(
            0, 0, max_row, max_col - 1, {"columns": column_settings}
        )
        worksheet_cat.add_table(
            0, 0, max_row_cat, max_col_cat - 1, {"columns": column_settings_cat}
        )

        # make the columns wider for clarity
        worksheet.set_column(0, max_col - 1, 12)
        worksheet_cat.set_column(0, max_col - 1, 12)

    writer.save()
    return None


def json_to_database(departmentTable, file: str):
    f = open("../pyrosvestiki2.json")
    data = json.load(f)

    for tweet in data["features"]:
        id = tweet["id"]
        text = tweet["properties"]["text"]
        created_at = datetime.strptime(
            tweet["properties"]["created_at"], "%Y/%m/%d %H:%M:%S"
        )
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
            longitude=longitude,
        )
        try:
            with db_session() as session:
                session.add(new_tweet)
                session.commit()
                print(
                    f"The {new_tweet.__tablename__} tweet with id "
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
            count += 1
            print(f"{count/all_count * 100}%")
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
            count += 1
            print(f"{count/all_count * 100}%")
            tweet.plain_text = remove_links_emojis(tweet.text)

        session.commit()


def update_tweets_regex_woi(department: str) -> None:
    """
    Update/calculate the regex_woi for all the tweets with eligible
    category representing an event, based on categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        # all_tweets = session.query(departmentTable).where(
        #     departmentTable.category>0)
        all_tweets = session.query(departmentTable)

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
            count += 1
            print(f"{count/all_count * 100}%")

            if tweet.category < 1:
                tweet.regex_woi = None
            else:
                tweet.regex_woi = regex_woi(tweet.plain_text)

        session.commit()


def update_tweets_capital_words(department: str) -> None:
    """
    Update/calculate the capital_words for all the tweets with eligible
    category representing an event, based on the categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        # all_tweets = session.query(departmentTable).where(
        #     departmentTable.category>=0)
        all_tweets = session.query(departmentTable)

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
            count += 1
            print(f"{count} / {all_count}")
            if tweet.category > 0:
                tweet.capital_words = get_capital_words(tweet.plain_text)
            else:
                tweet.capital_words = None

        session.commit()


def update_tweets_translated_text(department: str) -> None:
    """
    Update/calculate the translated_text for all the tweets with eligible
    category representing an event, based on categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        all_tweets = (
            session.query(departmentTable)
            .where(departmentTable.category > 0)
            .where(departmentTable.translated_text.is_(None))
        )

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
            count += 1
            print(f"{count} / {all_count}")
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
            departmentTable.regex_woi != None
        )

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
            count += 1
            print(f"{count} / {all_count}")
            tweet.longitude, tweet.latitude = geocoding_osm(tweet.regex_woi)
            session.commit()

        # session.commit()


def update_tweets_geograpy_woi(department: str) -> None:
    """
    Update/calcualte the regex_woi for all the tweets with eligible
    category representing an event, based on categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        all_tweets = session.query(departmentTable)

    count = 0
    all_count = all_tweets.count()
    for tweet in all_tweets:
        count += 1
        print(f"{count} / {all_count}")
        if tweet.category < 1:
            tweet.geograpy_woi = None
        else:
            tweet.geograpy_woi = geograpy_woi(tweet.translated_text)

    session.commit()


def update_tweets_spacy_woi(department: str) -> None:
    """
    Update/calculate the spacy_woi for all the tweets with eligible
    category representing an event, based on categorize_tweet function.
    """
    departmentTable = str2department(department)

    with db_session() as session:
        all_tweets = session.query(departmentTable)

        count = 0
        all_count = all_tweets.count()
        for tweet in all_tweets:
            count += 1
            print(f"{count/all_count * 100}%")
            if tweet.category < 1:
                tweet.spacy_woi = None
            else:
                tweet.spacy_woi = spacy_woi(tweet.plain_text)

        session.commit()
