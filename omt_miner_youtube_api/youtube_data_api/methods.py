import datetime
from time import sleep


def parse_channel_response(yt_channel_response):
    result = {
        "responseEtag": yt_channel_response.get("etag", None),
        "itemEtag": yt_channel_response["items"][0].get("etag", None),
        "channelId": yt_channel_response["items"][0]["id"],
        "channelTitle": yt_channel_response["items"][0]["snippet"]["title"],
        "nameAbbr": "".join([part[0] for part in yt_channel_response["items"][0]["snippet"]["title"].split()]),
        "publishedAt": yt_channel_response["items"][0]["snippet"]["publishedAt"],
        "thumbnails": yt_channel_response["items"][0]["snippet"].get("thumbnails", None),
        "topicDetails": yt_channel_response["items"][0].get("topicDetails", None),
        "statistics": yt_channel_response["items"][0]["statistics"],
        "email": None,
        "phone": None,
        "activation": None,
        "activationDate": None,
        "videoPriceFactor": 1,
        "majorSentimentClass": None,
        "score": None,
        "commentators": [],
        "numCommentators": 0,
        "fans": [],
        "numFans": 0,
        "commentsOther": [],
        "numCommentsOther": 0,
        "commentsSelf": [],
        "numCommentsSelf": 0
    }
    return result


def parse_video_response(yt_video_response):
    result = {
        "responseEtag": yt_video_response.get("etag", None),
        "itemEtag": yt_video_response["items"][0].get("etag", None),
        "videoId": yt_video_response["items"][0]["id"],
        "categoryId": yt_video_response["items"][0]["snippet"].get("categoryId", None),
        "channelId": yt_video_response["items"][0]["snippet"]["channelId"],
        "description": yt_video_response["items"][0]["snippet"].get("description", None),
        "tags": yt_video_response["items"][0]["snippet"].get("tags", None),
        "thumbnails": yt_video_response["items"][0]["snippet"].get("thumbnails", None),
        "title": yt_video_response["items"][0]["snippet"]["title"],
        "statistics": yt_video_response["items"][0]["statistics"]
    }
    return result


# # search for aggregations to calculate number of comments for channel
# 1: add channel of commentator and push list of commentators in the owner of channel and update  number of it
# 2: add comments into in the owner of the channel and update number of it
# 3: calculate fans. Fans: commentators which comments more then main number of comments of all commentators and add it
# fans list in the owner of the channel and update number of it
def parse_comments_response(yt_comments_response):
    comments = list()
    # get requested video id
    videoId = yt_comments_response['items'][0]['snippet']['videoId']
    # check the video is exist otherwise insert
    check_video_and_add_if_not_exist(videoId)
    # get channel id from video id
    channelId = dbm.get_one_document('video', {'videoId': videoId})['channelId']
    # this dictionary is common for all comments in one response
    pageInfo = {
        "etag": yt_comments_response['etag'],
        "nextPageToken": yt_comments_response.get("nextPageToken", None)
    }

    for key, value in yt_comments_response['pageInfo'].items():
        pageInfo[key] = value

    # iterate for all comments in response
    for item in yt_comments_response['items']:
        # create a variable to add to db
        comment = {
            "commentId": item['id'],
            **item['snippet']['topLevelComment']['snippet'],
            "channelId": channelId,
            "totalReplyCount": item['snippet']['totalReplyCount'],
            "commentEtag": item['snippet']['topLevelComment']['etag'],
            "itemEtag": item['etag'],
            "pageInfo": pageInfo,
            "replied": False
        }
        # fix a youtube convention
        comment["authorChannelId"] = comment["authorChannelId"]["value"]
        # check channel of commentator is exist otherwise insert
        check_channel_and_add_if_not_exist(comment["authorChannelId"])
        # append parsed comment to result list
        comments.append(comment)
        # if comment is replied
        if item.get('replies', None):
            # get replied comments in one variable
            replies = item['replies']['comments']
            # iterate for all replied comments
            for reply in replies:
                # create a variable to add to db
                comment = {
                    "commentId": reply['id'],
                    **reply['snippet'],
                    "channelId": channelId,
                    "commentEtag": reply['etag'],
                    "itemEtag": item['etag'],
                    "pageInfo": pageInfo,
                    "replied": True
                }
                # fix a youtube convention
                comment["authorChannelId"] = comment["authorChannelId"]["value"]
                # check channel of commentator is exist otherwise insert
                check_channel_and_add_if_not_exist(comment["authorChannelId"])
                # append parsed comment to result list
                comments.append(comment)
    # return list of parsed comments
    return comments


def yt_channel_request_by_id(client, channel_id, sleep_amount=None):
    if sleep_amount: sleep(sleep_amount)
    yt_channel_response = client.channels().list(
        part='snippet,statistics,topicDetails',
        fields='etag,items/etag,items/id,items/snippet/customUrl,items/snippet/title,items/snippet/publishedAt,'
               'items/snippet/thumbnails,items/statistics,items/topicDetails',
        id=channel_id
    ).execute()
    return parse_channel_response(yt_channel_response)


def yt_channel_request_by_username(client, channel_name):
    yt_channel_response = client.channels().list(
        part="snippet,statistics,topicDetails",
        forUsername=channel_name
    ).execute()
    return yt_channel_response


def yt_video_request(client, video_id, sleep_amount=None):
    if sleep_amount: sleep(sleep_amount)

    video_info = client.videos().list(
        part='snippet,statistics',
        fields='etag,items/etag,items/statistics,items/id,items/snippet/categoryId,items/snippet/channelId,'
               'items/snippet/channelTitle,items/snippet/description,items/snippet/tags,items/snippet/thumbnails,'
               'items/snippet/title',
        id=video_id
    ).execute()
    return parse_video_response(video_info)


def yt_videos_of_channel_request(client, channelId, pageToken=None):
    response = client.search().list(
        part="id",
        channelId=channelId,
        fields="nextPageToken,items/id/videoId",
        maxResults=25,
        order="date",
        type="video",
        pageToken=pageToken
    ).execute()
    return response


# page by page write to mongodb
def yt_comment_request(client, videoId, nextPageToken=None):
    response = client.commentThreads().list(
        part="snippet,replies",
        fields="etag,nextPageToken,pageInfo,items(etag,id,replies(comments(etag,id,snippet(authorChannelId," \
               "authorProfileImageUrl,likeCount,publishedAt,textDisplay,textOriginal,updatedAt,videoId)))," \
               "snippet(isPublic,videoId,totalReplyCount,topLevelComment(etag,id,snippet(authorChannelId," \
               "authorProfileImageUrl,likeCount,publishedAt,textDisplay,textOriginal,updatedAt,videoId))))",
        maxResults=100,
        videoId=videoId,
        textFormat="plainText",
        pageToken=nextPageToken,
        order="time"
    ).execute()
    return parse_comments_response(response)


def yt_duration_to_mysql_duration(duration):
    return str(datetime.timedelta(seconds=isodate.parse_duration(duration).total_seconds()))


def yt_datetime_to_mysql_datetime(dt):
    return dt.split("T")[0] + " " + dt.split("T")[1].split(".")[0]


def clean_text(text):
    text = text.replace("'", " ").replace("\n", " ").strip()
    return ' '.join(text.split())


def channel_name_to_channel_id(client, channelName):
    channel_info = yt_channel_request_by_username(client, channelName)
    channelId = channel_info["items"][0]["id"]
    return channelId


def check_video_and_add_if_not_exist(videoId):
    yt_video_response = dbm.get_one_document('video', _filter={'videoId': videoId})
    if yt_video_response is None:
        yt_video_response = apmt.add_video(videoId)
        if not yt_video_response:
            raise "ERROR: " + "addition video."
    check_channel_and_add_if_not_exist(yt_video_response["channelId"])
    return yt_video_response


def check_channel_and_add_if_not_exist(channel_id):
    # get channel from db if exist
    yt_channel_response = dbm.get_one_document("channel", {"channelId": {"$eq": channel_id}})
    # otherwise add to db
    if yt_channel_response is None: yt_channel_response = apmt.channel_add({"channelId": channel_id})
    # return channel info
    return yt_channel_response


def yt_channels(client, **kwargs):
    response = client.channels().list(**kwargs).execute()
    return response
