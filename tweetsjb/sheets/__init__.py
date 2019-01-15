import argparse
import arrow
import json

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client.tools import argparser
from oauth2client import file, client, tools

from tweetsjb.settings import Settings

args = argparser.parse_args()
args.noauth_local_webserver = True  # avoid to open the browser

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1hyfoRoXWBQ1vJ2DKL8DTloxERio2zRobyqpwb4-zSdk'
RANGE_NAME = 'tweets!A1:F1'
VALUE_INPUT_OPTION = 'RAW'
INSERT_DATA_OPTION = 'INSERT_ROWS'


def get_sheets_service():
    store = file.Storage('secrets/token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('secrets/credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    return service


def _get_extended_status(tweet):
    status = tweet.get('text')

    if tweet.get('retweeted_status'):  # is retweet
        if tweet.get('retweeted_status', {}).get('extended_tweet'):
            return tweet.get('retweeted_status', {}).get('extended_tweet').get('full_text', status)

    if tweet.get('extended_tweet', {}).get('full_text'):
        return tweet.get('extended_tweet', {}).get('full_text', status)

    return status


def save_it_on_spreadsheet(created_at, screen_name, status, is_retweet, tweet_url, data):
    # service = get_sheets_service()
    date = arrow.get(created_at)

    value_range_body = {
        "values": [
            [
                date.format('DD/MM/YYYY HH:mm:ss'),
                screen_name,
                status,
                is_retweet,
                tweet_url,
                json.dumps(data),
            ]
        ],
        "range": RANGE_NAME,
        "majorDimension": "ROWS"
    }

    print(value_range_body)

    # request = service.spreadsheets().values().append(
    #     spreadsheetId=SPREADSHEET_ID,
    #     range=RANGE_NAME,
    #     valueInputOption=VALUE_INPUT_OPTION,
    #     insertDataOption=INSERT_DATA_OPTION,
    #     body=value_range_body)
    # response = request.execute()


def insert_delete_tweet_into_sheet(tweet):
    status = tweet.get('delete', {}).get('status')
    user_id = status.get('user_id_str')
    tweet_id = status.get('id_str')

    created_at = tweet.get('delete').get('timestamp_ms')
    screen_name = Settings.FOLLOW_IDS[user_id]
    status_text = 'Tweet {} deletado'.format(tweet_id)
    is_retweet = ''
    tweet_url = "https://twitter.com/{user}/status/{tweet_id}".format(
                    user=user_id,
                    tweet_id=tweet_id
                )

    save_it_on_spreadsheet(
        created_at[0:-3],  # remove ms
        screen_name,
        status_text,
        is_retweet,
        tweet_url,
        tweet
    )

def insert_tweet_into_sheet(tweet):
    is_retweet = 'N'
    if tweet._json.get('retweeted_status'):
        is_retweet = 'S'

    status_text = _get_extended_status(tweet._json)
    tweet_url = "https://twitter.com/{user}/status/{tweet_id}".format(
                    user=tweet.user.id_str,
                    tweet_id=tweet.id_str
                ),

    save_it_on_spreadsheet(
        tweet.created_at,
        tweet.user.name,
        status_text,
        is_retweet,
        tweet_url,
        tweet
    )