import falcon

from mongoengine import connect
from resources.channel_resource import ChannelResource
from resources.video_resource import VideoResource
from resources.comment_resource import CommentResource
from resources.user_resource import UserResource


__version__ = '0.1'

ROUTE_PREFIX = f'/api/v{__version__}/youtube'

app = application = falcon.API()
app.add_route(ROUTE_PREFIX + '/channels/{channel_id}', ChannelResource())
app.add_route(ROUTE_PREFIX + '/videos/{video_id}', VideoResource())
app.add_route(ROUTE_PREFIX + '/comments/{comment_id}', CommentResource())
app.add_route(ROUTE_PREFIX + '/users/{user_id}', UserResource())

database = connect(db='Omniscientus', host='localhost', port=27017)
