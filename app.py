import tweepy
import json

from settings import Settings
from streammer import StreamListener

def authenticateTwitter():
    auth = tweepy.OAuthHandler(
        Settings.twitter_consumer_token,
        Settings.twitter_consumer_secret
    )

    auth.set_access_token(
        Settings.twitter_access_token,
        Settings.twitter_secret_token
    )

    return auth


def run():
    auth = authenticateTwitter()
    api = tweepy.API(auth)
    listener = StreamListener()

    myStream = tweepy.Stream(auth = api.auth, listener=listener)
    myStream.filter(follow=Settings.follow_ids)

run()