import tweepy
import json
import codecs
import os
from pathlib import Path

def saveToFile(status):
    filename = '{}.json'.format(status.id_str)
    path =  Path('./data/{}'.format(filename))

    status_json = json.dumps(status._json)

    path.touch(exist_ok=True)
    with open(path, 'w+') as file:
        file.write(status_json)


class StreamListener(tweepy.StreamListener):

    def on_status(self, status):
        saveToFile(status)
        print(status.text)

    def on_error(self, err):
        print(err)
