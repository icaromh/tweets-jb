import tweepy
import json
import codecs
import os

from pathlib import Path

from tweetsjb.settings import Settings


def saveToFile(status):
    filename = '{}.json'.format(status.id_str)
    path =  Path('./data/{}'.format(filename))

    status_json = json.dumps(status._json)

    path.touch(exist_ok=True)
    with open(path, 'w+') as file:
        file.write(status_json)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        if status.user.id_str in Settings.follow_ids:
            saveToFile(status)

        username = status.user.screen_name.ljust(15)
        print('@{} - {}'.format(username, status.text))

    def on_error(self, err):
        print(err)
