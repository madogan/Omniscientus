from urllib.error import HTTPError


class YoutubeChannel:
    def __init__(self, client=None, channel_id=None, username=None):
        self.client = client
        self.channel_id = channel_id
        self.username = username
        self.video_links = list()
        self.num_videos = 0
        self.videos = list()
        self.comments = list()
        if channel_id is None and username is not None:
            self.channel_id = self.get_channel_id_from_username(client, username)
        elif channel_id is None and username is None:
            raise "ERROR: " + "You can not empty username and channelID"

    @staticmethod
    def get_channel_id_from_username(client, username):
        channel_id = None
        try:
            channel_id = client.channels().list(
                part="snippet,contentDetails,statistics",
                forUsername=username
            ).execute()['items'][0]['id']
        except (HTTPError, IndexError):
            print("Channel has not found, check username.")
    
        return channel_id

