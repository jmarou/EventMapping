import os
import requests


# token for twitter API
TWITTER_TOKEN = os.getenv("TOKEN")

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


def download_tweets(account_id: int, parameters: dict) -> dict:
    """
    Gets the account name of the twitter user and a set of parameters and 
    returns the last tweets from their timeline.

    Parameters
    ----------
    account_id : int
        The account id given by twitter API.

    Returns
    ----------
    r.json : dict
        A python dictionary with the response from twitter API v2.
    """
    r = requests.get(
        auth = BearerAuth(TWITTER_TOKEN),
        url = "https://api.twitter.com/2/users/{}/tweets".format(account_id),
        params = parameters,
    )
    
    print(f"Last twitter: {r.json()['data'][0]['created_at']}")
    print(f"Fetched {len(r.json()['data'])} new tweets")
    
    return r.json()
