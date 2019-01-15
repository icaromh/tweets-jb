import tweepy
import json
import codecs
import os

from pathlib import Path

from tweetsjb.settings import Settings
from tweetsjb.sheets import insert_tweet_into_sheet, \
                            insert_delete_tweet_into_sheet


def save_to_file(tweet_id, tweet):
    filename = '{}.json'.format(tweet_id)
    path =  Path('./data/{}'.format(filename))

    status_json = json.dumps(tweet)
    path.touch(exist_ok=True)
    with open(path, 'w+') as file:
        file.write(status_json)


def get_user_id(tweet):
    if tweet.get('delete', {}):
        return tweet.get('delete', {}).get('status', {}).get('user_id_str')
    elif tweet.user and tweet.user.id_str:
        return tweet.user.id_str

    return False


def should_save(tweet):
    import ipdb; ipdb.set_trace()
    user_id = get_user_id(tweet)
    follow_ids = list(Settings.FOLLOW_IDS.keys())
    if user_id in follow_ids:
        return True

    return False


class StreamListener(tweepy.StreamListener):

    def on_data(self, raw):
        print(raw)
        data = json.loads(raw)

        if 'delete' in data.keys() and should_save(data):
            tweet_id = data.get('delete', {}).get('status').get('id_str')

            save_to_file(tweet_id, data)
            insert_delete_tweet_into_sheet(data)

    def on_status(self, status):
        if should_save(status):
            save_to_file(status.id_str, status._json)
            insert_tweet_into_sheet(status)

        username = status.user.screen_name.ljust(15)
        print('@{} - {}'.format(username, status.text))

    def on_error(self, err):

        print(err)
