from flask import Blueprint, jsonify, request, session, make_response

import omniscientus.api_methods as apmt

__version__ = "1.0"

bp = Blueprint('api', __name__, url_prefix='/api/v{}'.format(__version__))

STATUS_TRUE = {"status": True}
STATUS_FALSE = {"status": False}


@bp.route('/practice')
def practice():
    try:
        result = apmt.practice() or STATUS_FALSE
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_notifications_of_channel/channelId=<channelId>&offset=<int:offset>&number=<int:number>')
def get_notifications_of_channel(channelId, offset=None, number=None):
    try:
        result = apmt.get_notifications_of_channel(channelId, offset, number) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/add_notification/channelId=<channelId>&notification=<notification>')
def add_notification(channelId, notification):
    try:
        result = apmt.add_notification(channelId, notification) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


# it can be used for video or channel, date format: 0000-00-00
@bp.route('/get_change_rates_of_comments_sentiment_class/'
          'statisticId=<statisticId>&first_date=<first_date>&second_date=<second_date>')
def get_change_rates_of_comments_sentiment_class(statisticId, first_date=None, second_date=None):
    try:
        result = apmt.get_change_rates_of_comments_sentiment_class(statisticId, first_date, second_date) \
                 or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_change_rates_of_comments_sentiment_class_of_fans/channelId=<channelId>&first_date=<first_date>&'
          'second_date=<second_date>')
def get_change_rates_of_comments_sentiment_class_of_fans(channelId, first_date=None, second_date=None):
    try:
        result = apmt.get_change_rates_of_comments_sentiment_class_of_fans(channelId, first_date, second_date) or \
                 False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_change_rates_of_comments_sentiment_class_of_commentators/channelId=<channelId>&first_date=<first_date>&'
          'second_date=<second_date>')
def get_change_rates_of_comments_sentiment_class_of_commentators(channelId, first_date=None, second_date=None):
    try:
        result = apmt.get_change_rates_of_comments_sentiment_class_of_commentators(channelId, first_date, second_date) \
                 or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_change_rates_of_fans/channelId=<channelId>&first_date=<first_date>&'
          'second_date=<second_date>')
def get_change_rates_of_fans(channelId, first_date=None, second_date=None):
    try:
        result = apmt.get_change_rates_of_fans(channelId, first_date, second_date) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


# add change rates of sentiment class of commentators
@bp.route('/get_change_rates_of_commentators/channelId=<channelId>&first_date=<first_date>&'
          'second_date=<second_date>')
def get_change_rates_of_commentators(channelId, first_date=None, second_date=None):
    try:
        result = apmt.get_change_rates_of_commentators(channelId, first_date, second_date) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_comments_of_channel/channelId=<channelId>&offset=<offset>&number=<number>')
def get_comments_of_channel(channelId, offset=None, number=None):
    try:
        result = apmt.get_comments_of_channel(channelId, offset, number) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_comments_for_channel/channelId=<channelId>&offset=<offset>&number=<number>')
def get_comments_for_channel(channelId, offset=None, number=None):
    try:
        result = apmt.get_comments_for_channel(channelId, offset, number) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/update_fans/channelId=<channelId>')
def update_fans(channelId):
    try:
        result = apmt.update_fans(channelId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_fans/channelId=<channelId>')
def get_fans(channelId):
    try:
        result = apmt.get_fans(channelId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/add_fans/channelId=<channelId>')
def add_fans(channelId):
    try:
        result = apmt.add_fans(channelId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/update_commentators/channelId=<channelId>')
def update_commentators(channelId):
    try:
        result = apmt.update_commentators(channelId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_commentators/channelId=<channelId>')
def get_commentators(channelId):
    try:
        result = apmt.get_commentators(channelId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/add_commentators/channelId=<channelId>')
def add_commentators(channelId):
    try:
        result = apmt.add_commentators(channelId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/update_comments_of_video/videoId=<videoId>')
def update_comments_of_video(videoId):
    try:
        result = apmt.update_comments_of_video(videoId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/get_comments_of_video/videoId=<videoId>&offset=<int:offset>&number=<int:number>')
def get_comments_of_video(videoId, offset=None, number=None):
    try:
        result = apmt.get_comments_of_video(videoId, offset, number) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/add_comments_of_video/videoId=<videoId>')
def add_comments_of_video(videoId):
    try:
        result = apmt.add_comments_of_video(videoId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/update_videos_of_channel/channelId=<channelId>')
def update_videos_of_channel(channelId):
    try:
        result = apmt.update_videos_of_channel(channelId) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


# if offset and number is 0, it returns all videos
@bp.route('/get_videos_of_channel/channelId=<channel_id>&offset=<int:offset>&number=<int:number>')
def get_videos_of_channel(channel_id, offset=None, number=None):
    try:
        result = apmt.get_videos_of_channel(channel_id, offset, number) or False
    except Exception as e:
        result = {"error": str(e)}
    return jsonify(result)


@bp.route('/channel/videos/add', methods=["POST"])
def channel_videos_add():
    try:
        response_content, response_status = apmt.channel_videos_add(request.get_json())
    except Exception as e:
        response_content, response_status = {"error": str(e)}, 500
    return make_response((jsonify(response_content), response_status))


@bp.route('/video/update', methods=["PUT"])
def video_update():
    try:
        response_content, response_status = apmt.video_update(request.get_json())
    except Exception as e:
        response_content, response_status = {"error": str(e)}, 500
    return make_response((jsonify(response_content), response_status))


@bp.route('/video/get', methods=["GET"])
def video_get():
    try:
        response_content, response_status = apmt.video_get(request.args)
    except Exception as e:
        response_content, response_status = {"error": str(e)}, 500
    return make_response((jsonify(response_content), response_status))


@bp.route('/video/add', methods=["POST"])
def video_add():
    try:
        response_content, response_status = apmt.video_add(request.get_json())
    except Exception as e:
        response_content, response_status = {"error": str(e)}, 500
    return make_response((jsonify(response_content), response_status))


@bp.route('/channel/update', methods=["PUT"])
def channel_update():
    try:
        response_content, response_status = apmt.channel_update(request.get_json())
    except Exception as e:
        response_content, response_status = {"error": str(e)}, 500
    return make_response((jsonify(response_content), response_status))


@bp.route('/channel/get', methods=["GET"])
def channel_get():
    try:
        response_content, response_status = apmt.channel_get(request.args)
    except Exception as e:
        response_content, response_status = {"error": str(e)}, 500
    return make_response((jsonify(response_content), response_status))


@bp.route('/channel/add', methods=["POST"])
def channel_add():
    try:
        print(request.get_json())
        response_content, response_status = apmt.channel_add(request.get_json())
    except Exception as e:
        response_content, response_status = {"error": str(e)}, 500
    return make_response((jsonify(response_content), response_status))

"""
# [A] add here requests log
@bp.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    apmt.log_request(request)
    apmt.log_response(response)
    return response
"""

