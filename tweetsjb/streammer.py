import tweepy
import json
import codecs
import os

from pathlib import Path

from tweetsjb.settings import Settings
from tweetsjb.sheets import insert_tweet_into_sheet

def saveToFile(tweet):
    filename = '{}.json'.format(tweet.id_str)
    path =  Path('./data/{}'.format(filename))

    status_json = json.dumps(tweet._json)
    path.touch(exist_ok=True)
    with open(path, 'w+') as file:
        file.write(status_json)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.user.id_str in Settings.FOLLOW_IDS:
            saveToFile(status)
            insert_tweet_into_sheet(status)

        username = status.user.screen_name.ljust(15)
        print('@{} - {}'.format(username, status.text))

    def on_error(self, err):
        print(err)
