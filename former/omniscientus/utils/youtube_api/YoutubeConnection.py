import os
import pafy
import random

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = os.path.join("omniscientus", "utils", "youtube_api", "data", "client_secret.json")
DEVELOPER_KEYS = [
    "AIzaSyCeOMzhR2oVWpA5wNbh1a3i3AsEyYhp3lw",
    "AIzaSyDx5JP_9w-YAwzjZF0KgSziZGnjldwp8zE",
    "AIzaSyAiNXPfK5bfYzeemlyZZfpyelZN91AM6CY",
    "AIzaSyBmerRtYoSwqoONdQN-0EQvcrLrK4cHpvE",
    "AIzaSyDmjjRI9YZ9kQPHT_sOE6vj7zKLJN-Kqaw"
]
SERVICE_NAME = "youtube"
VERSION = "v3"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


class YoutubeConnection:
    def __init__(self):
        # self.flow = flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        # self.credentials = flow.run_console()
        # self.client = None
        self.key = DEVELOPER_KEYS[0]
        self.client = build(SERVICE_NAME, VERSION, developerKey=self.key, cache_discovery=False)
        pafy.set_api_key(self.key)

    # def get(self):
    #     return build(API_SERVICE_NAME, API_VERSION, credentials=self.credentials)

    # def update_connection(self):
    #     new_key = DEVELOPER_KEYS[random.randint(0, len(DEVELOPER_KEYS)-1)]
    #     while new_key == self.key:
    #         new_key = DEVELOPER_KEYS[random.randint(0, len(DEVELOPER_KEYS)-1)]
    #         self.key = new_key
    #     self.client = build(SERVICE_NAME, VERSION, developerKey=self.key, cache_discovery=False)
    #     pafy.set_api_key(self.key)
