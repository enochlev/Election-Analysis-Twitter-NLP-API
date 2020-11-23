import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, CategoriesOptions, EmotionOptions
#TUTUORIAL
#https://cloud.ibm.com/apidocs/natural-language-understanding?code=python#versioning



class NLP_API:
    def __init__(self):
        authenticator = IAMAuthenticator('<IBM API KEY>')
        self.natural_language_understanding = NaturalLanguageUnderstandingV1(version='2020-08-01',authenticator=authenticator)



    def processString(self, string_tweet = ""):
        string_tweet = string_tweet.replace("\\u", " ")
        self.natural_language_understanding.set_service_url('<service URL>')
        response = self.natural_language_understanding.analyze(html=string_tweet,features=Features(emotion=EmotionOptions(targets=['biden','trump']))).get_result()

        
        return response

