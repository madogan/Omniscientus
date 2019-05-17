import json
import falcon
from schemas.channel import Channel


class YoutubeCommentResource(object):

    def on_get(self, req, resp, channel_id):
        if channel_id is not None:
            resp.media = Channel.objects.get(channel_id=channel_id)

    def on_post(self, req, resp):
        pass

    def on_put(self, req, resp):
        pass

    def on_delete(self, req, resp):
        pass
