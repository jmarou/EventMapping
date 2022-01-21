import requests
import os 

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token  # this is to get it from the Environment Variable called TOKEN
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

parameters = {"id": "fadf"}

r = requests.get(
    url = "https://api.twitter.com/2/tweets",
    auth = BearerAuth(os.getenv('TOKEN')),
    params = parameters 
)
print(r.json())
print(r.status_code)
    