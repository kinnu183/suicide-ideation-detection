# fetch tweets from twitter
import re
import pandas as pd
import json
import tweepy
from tweepy import MyStreamListener, Stream, Cursor
import config

class MyStreamListener(Stream):
    def on_status(self, status):
        with open('tweets.json', 'a') as db:
            db = {'tweet': status.text, 'user': status.user.name}
            json.dumps(db, ensure_ascii=False, indent=2)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            return False # disconnect the stream

def stream_data():
    """Stream tweets from twitter."""
    
    consumerKey = config.CONSUMER_KEY
    consumerSecret = config.CONSUMER_SECRET
    accessToken = config.ACCESS_TOKEN
    accessTokenSecret = config.ACCESS_TOKEN_SECRET

    # authentication
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    # set access token
    auth.set_access_token(accessToken, accessTokenSecret)
    # create the api object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    _listener = MyStreamListener()
    my_stream = Stream(auth=api.auth, listener=_listener)
    rules = ['suicide', 'commit suicide', 'suicidal']
    my_stream.filter(track=rules)

def get_twitter_data():
    """Fetch tweets from twitter."""
    # get the data
    consumerKey = config.CONSUMER_KEY
    consumerSecret = config.CONSUMER_SECRET
    accessToken = config.ACCESS_TOKEN
    accessTokenSecret = config.ACCESS_TOKEN_SECRET

    # authentication
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    # set access token
    auth.set_access_token(accessToken, accessTokenSecret)
    # create the api object
    api = tweepy.API(auth, wait_on_rate_limit=True)

    _listener = MyStreamListener()
    my_stream = Stream(auth=api.auth, listener=_listener)
    rules = ['suicide', 'commit suicide', 'suicidal']

    Count = 10
    public_tweets = Cursor(api.search, rules, lang="en").items(Count)
    unwanted_words = ['@', 'RT', ':', 'https', 'http']
    symbols = ['@', '#']
    single_chars = re.compile(r'\s+[a-zA-Z]\s+')
    data = []
    for tweet in public_tweets:
        text = tweet.text
        textWords = text.split()
        cleaning_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(RT)", " ", text).split())
        cleaning_tweet = single_chars.sub('', cleaning_tweet)
        data.append(cleaning_tweet)
    data = pd.DataFrame(data)
    return data
    
df = get_twitter_data()
print(f"Len data: {len(df)} \n {df.head()}")
