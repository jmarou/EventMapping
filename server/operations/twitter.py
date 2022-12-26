import os
import requests
from datetime import datetime
from typing import List

from tokens import TWITTER_TOKEN

# account ids given by twitter to user accounts
ACCOUNT_IDS = {
    "hellenic_police": 119014566,
    "pyrosvestiki": 158003436
}

# default parameters for fetching new tweets from twitter API
DEFAULT_TWEET_PARAMETERS =  {
        "max_results": "100",
        "expansions": ["author_id"],
        "tweet.fields": "created_at"
}


class BearerAuth(requests.auth.AuthBase):
    """Authentication for the twitter API with Bearer Token."""

    def __init__(self, token):
        # my TWITTER API TOKEN IS SAVED IN OS ENVIRONMENT
        self.token = TWITTER_TOKEN

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def download_tweets(account_id: int, max_results: int=100) -> List:
    """
    Gets the account name of the twitter user and a set of parameters and 
    returns the last tweets from their timeline.

    Parameters
    ----------
    account_id : int
        The account id given by twitter API.

    Returns
    ----------
    r_data : List[dict]
        A list containing python dictionaries with the response from twitter
        API v2.
    """
    parameters = DEFAULT_TWEET_PARAMETERS
    r_data = []
    while True:
        r_json_next = requests.get(
            auth = BearerAuth(TWITTER_TOKEN),
            url = "https://api.twitter.com/2/users/{}/tweets".format(account_id),
            params = parameters
        ).json()
        r_data_next = r_json_next['data']
        print_message(
            len=len(r_data_next),
            first_date=r_data_next[0]['created_at'],
            last_date=r_data_next[-1]['created_at']
        )
        # r_json = {**r_json, **r_json_next}
        r_data += r_data_next
        max_results -= 100
        if max_results <= 0 or "next_token" not in r_json_next["meta"]:
            break
        else:
            # continue with the next patch of tweets
            parameters["pagination_token"] = r_json_next["meta"]["next_token"]
            parameters['max_results'] = min(100, max_results)
    
    return r_data        


def print_message(len: str, first_date: str, last_date: str) -> str:
    print(f"Fetched {len} new tweets from "\
        f"{datetime.strptime(first_date, '%Y-%m-%dT%H:%M:%S.%f%z').date()}"\
        " until "\
        f"{datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S.%f%z').date()}")
