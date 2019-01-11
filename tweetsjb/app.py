import tweepy
import json

from urllib3.exceptions import ProtocolError

from tweetsjb.settings import Settings
from tweetsjb.streammer import StreamListener

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

    try:
        myStream = tweepy.Stream(auth = api.auth, listener=listener)
        myStream.filter(follow=Settings.follow_ids)
    except (ConnectionResetError, ProtocolError) as e:
        print(e)
        run()  # reset the streamming


if __name__ == "__main__":
    run()