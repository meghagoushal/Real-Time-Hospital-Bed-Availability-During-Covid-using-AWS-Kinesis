import tweepy
import os
import pandas as pd
import csv
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import re
import string
from bs4 import BeautifulSoup

# authorization tokens
consumer_key= 'ZT'
consumer_secret= 'rW'
access_key= '9S'
access_secret= 'PrPp'

def cleaner(tweet):
        tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
        tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
        tweet = " ".join(tweet.split())
        tweet = tweet.replace("#", "").replace("_", " ").replace(",", "") #Remove hashtag sign but keep the text
        return tweet

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.
class StreamListener(tweepy.StreamListener):


    def on_status(self, status):
        print(status.id_str)
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")

        # check if text has been truncated
        if hasattr(status,"extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status,"extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        quoted_text = quoted_text.encode("ascii", "ignore")
        quoted_text = quoted_text.decode()
        text = text.encode("ascii", "ignore")
        text = text.decode()
        example1 = BeautifulSoup(quoted_text, 'lxml')
        quoted_text = example1.get_text()
        example2 = BeautifulSoup(text, 'lxml')
        text = example2.get_text()
        quoted_text = cleaner(quoted_text)
        text = cleaner(text)
        # remove characters that might cause problems with csv encoding
        remove_characters = [",","\n"]
        for c in remove_characters:
            text.replace(c," ")
            quoted_text.replace(c, " ")


        final_str = str(status.created_at) + str(status.user.screen_name) + str(is_retweet) + str(is_quote) + str(text) + str(quoted_text)
        if quoted_text.strip() and not is_retweet:
            print(final_str)
            with open("out_final_new_test_1.csv", "a", encoding='utf-8') as f:
                f.write("%s,%s,%s,%s,%s,%s\n" % (status.created_at,status.user.screen_name,is_retweet,is_quote,text,quoted_text))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()



if __name__ == "__main__":
    # complete authorization and initialize API endpoint
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    with open("out_final_new_test_1.csv", "w", encoding='utf-8') as f:
        f.write("date,user,is_retweet,is_quote,text,quoted_text\n")
    #new_search = "available+beds+delhi -filter:retweets"
    tags = ["available beds", "delhi"]
    stream.filter(track=tags) 
