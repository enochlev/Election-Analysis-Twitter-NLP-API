from NLP import NLP_API
from twitterAPI import Twitter_API
import datetime
import time
import traceback
import json




def createEmotionsCSVLine(response, name = "", id = ""):
    returnString = ""
    #name = response['emotion']['targets']['text']
    #print(json.dumps(response, indent=2))
    sadness = response['emotion']['document']['emotion']['sadness']
    joy     = response['emotion']['document']['emotion']['joy']
    fear    = response['emotion']['document']['emotion']['fear']
    disgust = response['emotion']['document']['emotion']['disgust']
    anger   = response['emotion']['document']['emotion']['anger']

    returnString = id + ',' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ',' + name + ',' + str(sadness) + ',' + str(joy) + ',' +  str(fear) + ',' +  str(disgust) + ',' +  str(anger)


    return (returnString)

def createTwiiterTextCSVLine(json_tweet_response,twitterText):
    return str(json_tweet_response["data"]['id']) + ',' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ',' + twitterText.replace(',','","')



def main():
    NLPWorker = NLP_API()

    fEmotions = open("emotionsFile.txt", "a")  # append mode 
    fText = open("textFile.txt", "a")  # append mode 
    i = 0

    twitterAPI = Twitter_API()


    stream = twitterAPI.get_stream()

    for response_line in stream.iter_lines():
        if response_line:            

            #twitter tweet into a json
            json_tweet_response = json.loads(response_line)
            twitterText = (str(json_tweet_response["data"]['text']).encode('ascii', 'ignore')).decode("utf-8")
           
           
            try:
                jsonNLPEmotions = NLPWorker.processString(twitterText)
            except Exception as e:
                print("\n\n>>>>>>>>>>"+ str(e) + "\n\n")
                continue#ignore any errors from NLP, and go on to next response

            twitterText = twitterText.replace('\n',' ')

            emotionsCSVLine = createEmotionsCSVLine(jsonNLPEmotions,str(json_tweet_response["matching_rules"][0]['tag']) , str(json_tweet_response["data"]['id']))
            textCSVline = createTwiiterTextCSVLine(json_tweet_response,twitterText)


            print(emotionsCSVLine)
            print(textCSVline)
            print("\n\n")
            i+=1


            fEmotions.write('\n' + emotionsCSVLine) 
            fText.write('\n' + textCSVline) 

            #every 100 entries, clear up ram
            if (i%100 == 0):
                fEmotions.close()
                fText.close()
                fEmotions = open("emotionsFile.txt", "a")  # append mode 
                fText = open("textFile.txt", "a")   # append mode 
                
            

while True:
    try:
        main()
    except KeyboardInterrupt:
        break
    except Exception as e:#else
        time.sleep(1)#wait 1 second before reconnection
        traceback.print_exc()
        continue#we want to always be streaming in new data, and retry if failed
