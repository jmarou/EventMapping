import requests
import os 
import sqlite3


# @hellenicpolice -> 119014566
# @pyrosvestiki -> 158003436
user_ids = {"hellenic_police":119014566, "pyrosvestiki": 158003436}
token = os.getenv('TOKEN')

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token  # this is to get it from the Environment Variable called TOKEN
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def get_tweets(user_id):
    r = \
        requests.get(
            auth = BearerAuth(token),
            url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
            )
    return r

def save_tweets(r):
    con = sqlite3.connect('tweets.db')

if __name__ == '__main__':
    r = get_tweets(user_ids["hellenic_police"])
    print(r.json())