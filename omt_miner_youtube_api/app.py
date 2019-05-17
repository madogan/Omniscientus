import falcon

from .resources.youtube_channel_resource import YoutubeChannelResource
from .resources.youtube_video_resource import YoutubeVideoResource
from .resources.youtube_comment_resource import YoutubeCommentResource


__version__ = '0.1'

# Falcon instance.
api = application = falcon.API()

api.add_route('api/v' + __version__ + '/miner/youtube/api/channel/{channel_id}', YoutubeChannelResource())
api.add_route('api/v' + __version__ + '/miner/youtube/api/video/{video_id}', YoutubeVideoResource())
api.add_route('api/v' + __version__ + '/miner/youtube/api/comment/{video_id}', YoutubeCommentResource())
