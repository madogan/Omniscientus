import pafy

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs


class YoutubeVideo:
    def __init__(self, videoID, channelID):
        self.base_url = "https://www.youtube.com/watch?v="
        self.videoID = videoID
        self.channelID = channelID
        self.data = pafy.new(self.base_url + self.videoID)
        self.title = self.data.title
        self.description = self.data.description
        self.publishedDate = self.data.published
        self.viewCount = self.data.viewcount
        self.commentCount = self.get_comment_count()
        self.duration = self.data.duration
        self.likes = self.data.likes
        self.dislikes = self.data.dislikes
        self.category = self.data.category
        self.majorSentimentClass = None

    def get_comment_count(self):
        response = urlopen(self.base_url + self.videoID)
        soup = bs(response, "lxml")
        return int(soup.select(".view-count")[0].text.split()[0])

    def get_json(self):
        return {
            "videoID": self.videoID,
            "channelID": self.channelID,
            "title": self.title,
            "description": self.description,
            "publishedAt": self.publishedDate,
            "viewCount": self.viewCount,
            "commentCount": self.commentCount,
            "duration": self.duration,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "category": self.category,
            "majorSentimentClass": None,
            "isPurchased": 0
        }
