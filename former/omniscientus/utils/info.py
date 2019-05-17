import json

from os.path import join

CATEGORIES = [
    'opinion',
    'feedback',
    'abusive',
    'request',
    'supportive',
    'didactic',
    'question',
    'criticism',
    'admiration',
    'advice',
    'trash'
]


def get_google_credentials():
    with open(join("omniscientus", "utils", "youtube_api", "data", "client_secret.json")) as f:
        return json.load(f)
