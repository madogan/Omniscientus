import os
import json
import datetime
from time import sleep
from flask import session
import omniscientus.database as dbm  # dbm: database methods
import omniscientus.utils.youtube_api.methods as ytm  # youtube api helper methods
from omniscientus.utils.youtube_api.YoutubeConnection import YoutubeConnection

# Youtube API V3 Client
yt = YoutubeConnection()

STATUS_TRUE = {"status": True}
STATUS_FALSE = {"status": False}

# [A] write check conditions for youtube api responses ([A]: add)


def deploy_model_comments():
    files = [os.path.join("omniscientus/utils/youtube_api/yt_mdl_comments", x) for x in
             os.listdir("omniscientus/utils/youtube_api/yt_mdl_comments")]
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                try:
                    text = json.loads(line)["text"].replace("\ufeff", "").replace("\n", "").lower()
                except:
                    print(file, line)
                dbm.db.yt_model_comments.insert({"text": text, "category": []})


def practice():
    dbm.db.request_log.remove()
    dbm.db.response_log.remove()
    return 2


def get_notifications_of_channel(channelId, offset=None, number=None):
    if (offset and number) and (offset == 0 and number == 0):
        return list(dbm.db.notification.find({"channelId": channelId}))
    else:
        return list(dbm.db.notification.find({"channelId": channelId}).skip(offset).limit(number))


def add_notification(channelId, notification):
    dbm.db.notification.insert_one({'channelId': channelId,
                                    'notification': notification,
                                    'date': datetime.datetime.now() - datetime.timedelta(days=15)})
    return True


# follower: commentator or fan
def get_follower_comments_stat(channelId, first_date, second_date):
    fyear, fmonth, fday = date_split(first_date)
    syear, smonth, sday = date_split(second_date)
    
    result = {
        'opinion': 0, 'feedback': 0, 'abusive': 0, 'request': 0, 'supportive': 0, 'didactic': 0, 'question': 0,
        'criticism': 0, 'admiration': 0,  'advice': 0, 'trash': 0
    }
    
    before_comments = dbm.db.channel_commentator.find(
        {
            "commentatorId": {"$eq": channelId},
            "date": {"$lt": datetime.datetime(fyear, fmonth, fday)}
        },
        {'_id': 0, 'channelId': 0, 'commentatorId': 0, 'videoId': 0, 'date': 0}
    )

    after_comments = dbm.db.channel_commentator.find(
        {
            "commentatorId": {"$eq": channelId},
            "date": {"$lt": datetime.datetime(syear, smonth, sday)}
        },
        {'_id': 0, 'channelId': 0, 'commentatorId': 0, 'videoId': 0, 'date': 0}
    )

    for comment in after_comments:
        commentSentimentClass = dbm.db.comment.find_one(
            {'commentId': {'$eq': comment['commentId'][:26]}},
            {'sentimentClass': 1}
        )
        if not commentSentimentClass: continue
        result[commentSentimentClass['sentimentClass']] += 1

    for comment in before_comments:
        commentSentimentClass = dbm.db.comment.find_one({'commentId': {'$eq': comment['commentId']}},
                                                        {'sentimentClass': 1})
        if not commentSentimentClass: continue
        result[commentSentimentClass['sentimentClass']] -= 1
    return result


def get_change_rates_of_comments_sentiment_class_of_fans(channelId, first_date, second_date):
    result = {
        'opinion': 0, 'feedback': 0, 'abusive': 0, 'request': 0, 'supportive': 0, 'didactic': 0, 'question': 0,
        'criticism': 0, 'admiration': 0, 'advice': 0, 'trash': 0
    }

    fans = dbm.db.channel_fan.find({'channelId': {'$eq': channelId}}, {'_id': 0, 'channelId': 0, 'date': 0})

    for fan in fans:
        item = get_follower_comments_stat(fan['fanId'], first_date, second_date)
        for key, value in item.items():
            result[key] += value

    return result


def get_change_rates_of_comments_sentiment_class_of_commentators(channelId, first_date, second_date):
    result = {
        'opinion': 0, 'feedback': 0, 'abusive': 0, 'request': 0, 'supportive': 0, 'didactic': 0, 'question': 0,
        'criticism': 0, 'admiration': 0, 'advice': 0, 'trash': 0
    }

    commentators = dbm.db.channel_commentator.find({'channelId': channelId}).distinct('commentatorId')

    for commentator in commentators:
        item = get_follower_comments_stat(commentator, first_date, second_date)
        for key, value in item.items():
            result[key] += value

    return result


def get_change_rates_of_comments_sentiment_class(statisticId, first_date, second_date):
    fyear, fmonth, fday = date_split(first_date)
    syear, smonth, sday = date_split(second_date)
    before_stat = dbm.db.statistic.find({
        "statisticId": {"$eq": statisticId},
        "recordDate": {"$lt": datetime.datetime(fyear, fmonth, fday)}
    })
    before_result = {'opinion': 0, 'feedback': 0, 'abusive': 0, 'request': 0, 'supportive': 0, 'didactic': 0,
                    'question': 0, 'criticism': 0, 'admiration': 0, 'advice': 0, 'trash': 0}

    for stat in before_stat:
        before_result['opinion'] += stat['opinion']
        before_result['feedback'] += stat['feedback']
        before_result['abusive'] += stat['abusive']
        before_result['request'] += stat['request']
        before_result['supportive'] += stat['supportive']
        before_result['didactic'] += stat['didactic']
        before_result['question'] += stat['question']
        before_result['criticism'] += stat['criticism']
        before_result['admiration'] += stat['admiration']
        before_result['advice'] += stat['advice']
        before_result['trash'] += stat['trash']

    after_stat = dbm.db.statistic.find({
        "statisticId": {"$eq": statisticId},
        "recordDate": {"$lt": datetime.datetime(syear, smonth, sday)}
    })
    after_result = {'opinion': 3123, 'feedback': 412, 'abusive': 15123, 'request': 1321, 'supportive': 5343, 'didactic': 523,
                     'question': 131, 'criticism': 434, 'admiration': 321, 'advice': 2523, 'trash': 213}

    for stat in after_stat:
        after_result['opinion'] += stat['opinion']
        after_result['feedback'] += stat['feedback']
        after_result['abusive'] += stat['abusive']
        after_result['request'] += stat['request']
        after_result['supportive'] += stat['supportive']
        after_result['didactic'] += stat['didactic']
        after_result['question'] += stat['question']
        after_result['criticism'] += stat['criticism']
        after_result['admiration'] += stat['admiration']
        after_result['advice'] += stat['advice']
        after_result['trash'] += stat['trash']

    result = {
        'opinion': after_result['opinion'] - before_result['opinion'],
        'feedback': after_result['feedback'] - before_result['feedback'],
        'abusive': after_result['abusive'] - before_result['abusive'],
        'request': after_result['request'] - before_result['request'],
        'supportive': after_result['supportive'] - before_result['supportive'],
        'didactic': after_result['didactic'] - before_result['didactic'],
        'question': after_result['question'] - before_result['question'],
        'criticism': after_result['criticism'] - before_result['criticism'],
        'admiration': after_result['admiration'] - before_result['admiration'],
        'advice': after_result['advice'] - before_result['advice'],
        'trash': after_result['trash'] - before_result['trash']
    }
    return result


def get_change_rates_of_fans(channelId, first_time, second_time):
    fyear, fmonth, fday = date_split(first_time)
    syear, smonth, sday = date_split(second_time)
    before_count = dbm.db.channel_fan.find({
        'channelId': {"$eq": channelId},
        "date": {"$lt": datetime.datetime(fyear, fmonth, fday)}
    }).distinct('fanId').count()
    after_count = dbm.db.channel_fan.find({
        'channelId': {"$eq": channelId},
        "date": {"$lt": datetime.datetime(syear, smonth, sday)}
    }).distinct('fanId').count()
    return after_count - before_count


def get_change_rates_of_commentators(channelId, first_date, second_date):
    fyear, fmonth, fday = date_split(first_date)
    syear, smonth, sday = date_split(second_date)
    before_count = dbm.db.channel_commentator.find({
        'channelId': {"$eq": channelId},
        "date": {"$lt": datetime.datetime(fyear, fmonth, fday)}
    }).distinct('commentatorId').count()
    after_count = dbm.db.channel_commentator.find({
        'channelId': {"$eq": channelId},
        "date": {"$lt": datetime.datetime(syear, smonth, sday)}
    }).distinct('commentatorId').count()
    return after_count-before_count


def get_comments_of_channel(channelId, offset, number):
    if (offset and number) and (offset == 0 and number == 0):
        return list(dbm.db.comment.find({"authorChannelId": channelId}))
    else:
        return list(dbm.db.comment.find({"authorChannelId": channelId}).skip(offset).limit(number))


def get_comments_for_channel(channelId, offset, number):
    if (offset and number) and (offset == 0 and number == 0):
        return list(dbm.db.comment.find({"channelId": channelId}))
    else:
        return list(dbm.db.comment.find({"channelId": channelId}).skip(offset).limit(number))


def update_fans(channelId):
    commentators = dbm.db.channel_commentator.find({'channelId': channelId}).sort([('date', -1)])\
        .distinct('commentatorId')
    items = dict()
    for commentator in commentators:
        num_comments = dbm.db.comment.find({'authorChannelId': commentator}).count()
        items[commentator] = num_comments

    avg_num_comments = sum(items.values()) / len(items.items())

    for commentator in commentators:
        num_comments = dbm.db.comment.find({'authorChannelId': commentator}).count()
        if num_comments > avg_num_comments:
            if not dbm.db.channel_fan.find_one({
                'channelId': channelId,
                'fanId': commentator,
            }):
                dbm.db.channel_fan.insert_one({
                    'channelId': channelId,
                    'fanId': commentator,
                    'date': datetime.datetime.now()
                })
            else:
                break
    return True


def get_fans(channelId):
    result = dbm.db.channel_fan.find({'channelId': channelId})
    return list(result)


# do this with aggregations
def add_fans(channelId):
    commentators = dbm.db.channel_commentator.find({'channelId': channelId}).distinct('commentatorId')
    items = dict()
    for commentator in commentators:
        num_comments = dbm.db.comment.find({'authorChannelId': commentator}).count()
        items[commentator] = num_comments

    avg_num_comments = sum(items.values()) / len(items.items())

    for commentator in commentators:
        num_comments = dbm.db.comment.find({'authorChannelId': commentator}).count()
        if num_comments > avg_num_comments:
            item = {
                'channelId': channelId,
                'fanId': commentator,
                'date': datetime.datetime.now()
            }
            dbm.db.channel_fan.insert_one(item)
    return True


def update_commentators(channelId):
    comments = dbm.db.comment.find({'channelId': channelId}, {'channelId': 1, 'authorChannelId': 1, 'videoId': 1,
                                                              'commentId': 1}).sort([("updatedAt", -1)])
    for comment in comments:
        if not dbm.db.channel_commentator.find_one({
            'channelId': comment['channelId'],
            'commentatorId': comment['authorChannelId'],
            'videoId': comment['videoId'],
            'commentId': comment['commentId']
        }):
            dbm.db.channel_commentator.insert_one({
                'channelId': comment['channelId'],
                'commentatorId': comment['authorChannelId'],
                'videoId': comment['videoId'],
                'commentId': comment['commentId'],
                'date': datetime.datetime.now()
            })
        else:
            break
    return True


def get_commentators(channelId):
    result = dbm.db.channel_commentator.find({'channelId': channelId})
    return list(result)


def add_commentators(channelId):
    comments = dbm.db.comment.find({'channelId': channelId}, {'channelId': 1, 'authorChannelId': 1, 'videoId': 1,
                                                              'commentId': 1})
    for comment in comments:
        item = {
            'channelId': comment['channelId'],
            'commentatorId': comment['authorChannelId'],
            'videoId': comment['videoId'],
            'commentId': comment['commentId'],
            'date': datetime.datetime.now()
        }
        dbm.db.channel_commentator.insert_one(item)
    return True


def update_comments_of_video(videoId):
    return True


def get_comments_of_video(videoId, offset=None, number=None):
    if (offset and number) and (offset == 0 and number == 0):
        return list(dbm.db.comment.find({"videoId": videoId}))
    else:
        return list(dbm.db.comment.find({"videoId": videoId}).skip(offset).limit(number))


def add_comments_of_video(videoId):
    next_page_token, number_of_comments = None, 0
    # add if the video of comments is not exist
    yt_video_response = ytm.check_video_and_add_if_not_exist(videoId)
    # comment count from youtube api actually from database
    number_of_remaining_comments = int(yt_video_response['statistics'].get('commentCount', None))
    # if no comments exists
    if not number_of_remaining_comments: return False
    # loop for comments every loop request 100 comments in a page
    while True:
        # youtube api comments request
        comments = ytm.yt_comment_request(yt.client, videoId, nextPageToken=next_page_token)
        # add comments to database
        dbm.add_one_document('comment', comments)
        # calculate number of added comments
        number_of_comments += len(comments)
        # print remaining number of comments
        print("{}/{} comment is left.".format(number_of_comments, number_of_remaining_comments))
        # there is no next page token in last page
        if comments[-1]["pageInfo"]["nextPageToken"] is None:
            print("0 comment is left.".format(number_of_remaining_comments))
            break
        else:
            next_page_token = comments[-1]["pageInfo"]["nextPageToken"]
        # if comments in page under 100 it means last page
        if int(comments[-1]["pageInfo"]["totalResults"]) < 100:
            print("0 comment is left.".format(number_of_remaining_comments))
            break
    return True


def update_videos_of_channel(channelId):
    # next_page_token = None
    # # add if the channel of videos is not exist
    # yt_channel_response = ytm.check_channel_and_add_if_not_exist(channelId)
    # # video count of channel
    # video_count_of_channel = int(yt_channel_response['statistics']["videoCount"])
    # # number of added videos
    # count = 0
    # keep = True
    # while True:
    #     time.sleep(random.uniform(0.1, 0.3))
    #
    #     yt_search_response = ytm.yt_videos_of_channel_request(yt.client, channelId, pageToken=next_page_token)
    #
    #     for item in yt_search_response["items"]:
    #         if dbm.db.video.find_one({"videoId": {"$exists": True}}):
    #             keep = False
    #             break
    #         time.sleep(random.uniform(0.1, 0.3))
    #         yt_video_response = ytm.yt_video_request(yt.client, item['id']['videoId'])
    #         dbm.add_document('video', yt_video_response)
    #         count += 1
    #
    #     next_page_token = yt_search_response.get("nextPageToken", None)
    #
    #     print("{}/{} video is added.".format(count, video_count_of_channel))
    #
    #     if next_page_token is None or keep is False: break
    return True, 200


def get_videos_of_channel(channelId, offset=None, number=None):
    if (offset and number) and (offset == 0 and number == 0):
        return list(dbm.db.video.find({"channelId": channelId}))
    else:
        return list(dbm.db.video.find({"channelId": channelId}).skip(offset).limit(number))


def add_videos_of_channel(channelId):
    next_page_token = None
    # add if the channel of videos is not exist
    yt_channel_response = ytm.check_channel_and_add_if_not_exist(channelId)
    # video count of channel
    video_count_of_channel = int(yt_channel_response['statistics']["videoCount"])
    # number of added videos
    count = 0
    while True:
        yt_search_response = ytm.yt_videos_of_channel_request(yt.client, channelId, pageToken=next_page_token)
        for item in yt_search_response["items"]:
            yt_video_response = ytm.yt_video_request(yt.client, item['id']['videoId'])
            dbm.add_one_document('video', yt_video_response)
            count += 1
        print("{}/{} video is added.".format(count, video_count_of_channel))
        next_page_token = yt_search_response.get("nextPageToken", None)
        if next_page_token is None: break
    return True


def video_update(params):
    video_id = params.get("videoId", None)
    many = params.get("many", None)
    if many is not None and video_id is None:
        for video_id in many:
            yt_video_response = ytm.yt_video_request(yt.client, video_id, sleep_amount=1)
            if not dbm.replace_one_document("video", {"videoId": video_id}, yt_video_response):
                return {"error": "Problem with this {}".format(video_id)}, 404
        return STATUS_TRUE, 200
    elif video_id is not None and many is None:
        yt_video_response = ytm.yt_video_request(yt.client, video_id)
        if dbm.replace_one_document("channel", {"channelId": video_id}, yt_video_response):
            return STATUS_TRUE, 200
        else:
            return STATUS_FALSE, 404


def video_get(params):
    many = params.get("many", None)
    video_id = params.get("videoId", None)
    if many is not None and many == "1":
        result, status = \
            dbm.get_many_document("video", offset=params.get("offset", None), number=params.get("number", None)), 200
    elif video_id is not None and many is None:
        result, status = dbm.get_one_document("video", {"videoId": video_id}), 200
    else:
        result, status = STATUS_FALSE, 404
    return result, status


def video_add(params):
    video_id = params.get("videoId", None)
    many = params.get("many", None)
    if video_id is not None and many is None:
        if dbm.get_one_document("video", {"videoId": video_id}):
            return STATUS_TRUE, 200

        yt_video_response = ytm.yt_video_request(yt.client, video_id)

        result = dbm.add_one_document('video', yt_video_response)

        if result: ytm.check_channel_and_add_if_not_exist(result["channelId"])

        return STATUS_TRUE, 200
    elif many is not None and video_id is None:
        for video_id in many:
            if dbm.get_one_document("video", {"videoId": video_id}):
                continue

            yt_video_response = ytm.yt_video_request(yt.client, video_id, sleep_amount=1)

            result = dbm.add_one_document('video', yt_video_response)

            if result: ytm.check_channel_and_add_if_not_exist(result["channelId"])

        return STATUS_TRUE, 200
    else:
        return {"error": "You can give many for multiple channel addition or single channel id"}, 404


def channel_update(params):
    channel_id = params.get("channelId", None)
    many = params.get("many", None)
    if many is not None and channel_id is None:
        for channel_id in many:
            yt_channel_response = ytm.yt_channel_request_by_id(yt.client, channel_id, sleep_amount=1)
            if not dbm.replace_one_document("channel", {"channelId": channel_id}, yt_channel_response):
                return {"error": "Problem with this {}".format(channel_id)}, 404
        return STATUS_TRUE, 200
    elif channel_id is not None and many is None:
        yt_channel_response = ytm.yt_channel_request_by_id(yt.client, channel_id)
        if dbm.replace_one_document("channel", {"channelId": channel_id}, yt_channel_response):
            return STATUS_TRUE, 200
        else:
            return STATUS_FALSE, 404


def channel_get(params):
    many = params.get("many", None)
    channel_id = params.get("channelId", None)
    if many is not None and many == "1":
        result, status = \
            dbm.get_many_document("channel", offset=params.get("offset", None), number=params.get("number", None)), 200
    elif channel_id is not None and many is None:
        result, status = dbm.get_one_document("channel", {"channelId": channel_id}), 200
    else:
        result, status = STATUS_FALSE, 404
    return result, status


def channel_add(params):
    # check params consists of "channelId"
    channel_id = params.get("channelId", None)
    many = params.get("many", None)
    if channel_id is not None and many is None:  # if params has channelId
        # if channel already exists
        if dbm.get_one_document("channel", {"channelId": channel_id}):
            return STATUS_TRUE, 200
        else:
            # make youtube api request
            yt_channel_response = ytm.yt_channel_request_by_id(yt.client, channel_id)
            # add youtube api response to database
            response = dbm.add_one_document('channel', yt_channel_response)
            if response:  # if response is not None or False
                return STATUS_TRUE, 200
            else:  # if there is any problem while adding channel to database
                return STATUS_FALSE, 404
    elif many is not None and channel_id is None:
        for channel_id in many:
            # if channel already exists, continue for others
            if dbm.get_one_document("channel", {"channelId": channel_id}): continue
            # make youtube api request
            yt_channel_response = ytm.yt_channel_request_by_id(yt.client, channel_id, sleep_amount=1)
            # add youtube api response to database
            response = dbm.add_one_document('channel', yt_channel_response)
            if not response:  # if response is not None or False
                return {"error": "Problem with this {}".format(channel_id)}, 404
        return STATUS_TRUE, 200
    else:
        return {"error": "You can give many for multiple channel addition or single channel id"}, 404


def log_request(req):
    if dbm.add_one_document("request_log", parse_request(req)): return STATUS_TRUE
    else: return {"error": "Logging request error"}


def log_response(resp):
    if dbm.add_one_document("response_log", parse_response(resp)): return STATUS_TRUE
    else: return {"error": "Logging response error"}


def date_split(date):
    return int(date.split("-")[0]), int(date.split("-")[1]), int(date.split("-")[2])


def parse_response(resp):
    return {
        "headers": str(resp.headers),
        "status": resp.status,
        "status_code": resp.status_code,
        "data": resp.data,
        "json": resp.get_json(silent=True),
        "is_json": resp.is_json,
        "max_cookie_size": resp.max_cookie_size,
        "mimetype": resp.mimetype,
    }


def parse_request(req):
    return {
        "path": req.path,
        "full_path": req.full_path,
        "script_root": req.script_root,
        "base_url": req.base_url,
        "url": req.url,
        "url_root": req.url_root,
        "accept_charsets": req.accept_charsets.__str__,
        "accept_encodings": req.accept_encodings.__str__,
        "accept_languages": req.accept_languages.__str__,
        "accept_mimetypes": req.accept_mimetypes.__str__,
        "access_route": list(req.access_route),
        "args": req.args.to_dict(),  # The parsed URL parameters (the part in the URL after the question mark)
        "authorization": req.authorization,
        "blueprint": req.blueprint,
        "cache_control": req.cache_control.__str__,
        "content_encoding": req.content_encoding,
        "content_length": req.content_length,
        "content_md5": req.content_md5,
        "content_type": req.content_type,
        "cookies": req.cookies,
        "data": req.data,
        "date": req.date,
        "endpoint": req.endpoint,
        "files": list(req.files),
        "form": list(req.form),
        "headers": req.headers.__str__,
        "host": req.host,
        "host_url": req.host_url,
        "if_match": req.if_match.__str__,
        "if_modified_since": req.if_modified_since,
        "if_none_match": req.if_none_match.__str__,
        "if_range": req.if_range.__str__,
        "if_unmodified_since": req.if_unmodified_since,
        "is_json": req.is_json,
        "is_multiprocess": req.is_multiprocess,
        "is_multithread": req.is_multithread,
        "is_run_once": req.is_run_once,
        "is_secure": req.is_secure,
        "is_xhr": req.is_xhr,
        "max_content_length": req.max_content_length,
        "max_forwards": req.max_forwards,
        "method": req.method,
        "mimetype": req.mimetype,
        "mimetype_params": req.mimetype_params,
        "pragma": req.pragma.__str__,
        "query_string": req.query_string,
        "range": req.range,
        "referrer": req.referrer,
        "remote_user": req.remote_user,
        "routing_exception": req.routing_exception,
        "scheme": req.scheme.__str__,
        "stream": req.stream.read(),
        "url_rule": req.url_rule,
        "charset_of_url": req.url_charset
    }
