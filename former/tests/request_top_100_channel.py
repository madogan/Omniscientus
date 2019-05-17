import os
import requests

#
# with open("../channels.txt", "rt", encoding="utf-8") as f:
#     channels = [line.split("\t")[1] for line in f.readlines()]
#
# for channel in channels[1:]:
#     requests.post("http://127.0.0.1:5000/api/v1.0/channel/add", json={"videoId": channel})


# requests.post("http://127.0.0.1:5000/api/v1.0/video/add", json={"videoId": "C6Ptu2qrWMw"})


requests.get("http://127.0.0.1:5000/api/v1.0/add_comments_of_video/videoId=C6Ptu2qrWMw")