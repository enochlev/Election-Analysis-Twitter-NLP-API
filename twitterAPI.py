import requests
import traceback
import os
import json
from NLP import NLP_API
os.environ['BEARER_TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAFbDJAEAAAAAj4g5RXy70g0r9JuXBEzUrz2keV0%3DWwj2JizcBUVFZ2hmYR8ixEWPnqhsyyckTUcEI2uC70MjTUZBX5'
import datetime


#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#::::                       TUTORIAL                    ::::#
#https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#versioning
#:::::                                                 :::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#
#:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::#

class Twitter_API:


    
    def __init__(self):
        __bearer_token = os.environ.get("BEARER_TOKEN")
        self.__headers = self.__create_headers(__bearer_token)
        __rules = self.__get_rules(self.__headers, __bearer_token)
        __delete = self.__delete_all_rules(self.__headers, __bearer_token, __rules)
        __set = self.__set_rules(self.__headers, __delete, __bearer_token)

    def __create_headers(self, bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers

    def __get_rules(self, headers, bearer_token):
        response = requests.get(
            "https://api.twitter.com/2/tweets/search/stream/rules", headers=headers
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        print(json.dumps(response.json()))
        return response.json()

    def __delete_all_rules(self, headers, bearer_token, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=headers,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))

    def __set_rules(self, headers, delete, bearer_token):
        # You can adjust the rules if needed
        Elect_Rules = [

            {"value": "trump -biden -has:links -has:images -has:media -has:videos -is:quote lang:en sample:1", "tag": "Trump"}          ,#sample:1 => take 1% of the tweets randomly 
            {"value": "biden -trump -has:links -has:images -has:media -has:videos -is:quote lang:en sample:1", "tag": "Biden"}
        
        ]
        payload = {"add": Elect_Rules}
        response = requests.post(
            "https://api.twitter.com/2/tweets/search/stream/rules",
            headers=headers,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )

    def get_stream(self):

        

        response = requests.get("https://api.twitter.com/2/tweets/search/stream", headers=self.__headers, stream=True,)
        print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        return response

           

def startup():


    bearer_token = os.environ.get("BEARER_TOKEN")
    headers = create_headers(bearer_token)
    rules = get_rules(headers, bearer_token)
    delete = delete_all_rules(headers, bearer_token, rules)
    set = set_rules(headers, delete, bearer_token)
    get_stream(headers, set, bearer_token)




