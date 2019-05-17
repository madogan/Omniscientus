# -*- coding: utf-8 -*-

import mongoengine as me  # ORM of MongoDB
from .sentiment_categories import SENTIMENT_CATEGORIES  # Predetermined comment sentiment classes


class Comment(me.Document):
	"""
		Schema for Comment created using 'mongoengine'

		Fields:
			time_index (long): This is an integer which determines time sorted index.
			comment_id (str): ID of the comment provided by Youtube.
			channel_id (str): Author ID of the comment referenced to Channel.
			channel_title (str): Author name of the comment referenced to Channel.
			channel_thumbnail (url): Url for pic of channel.
			video_id (str): Video of the comment.
			text (str): Content of the comment.
			likes (long): Number of likes for the comment.
			time (str): Passed time after commented as string representation.
			edited (bool): If comment is edited, value is True.
			timestamp (long): Timestamp of comment.
			has_replies (bool): If the comment is replied its value is True.

	"""

	time_index = me.LongField(required=True, default=0)
	comment_id = me.StringField(primary_key=True)
	channel_id = me.ReferenceField('Channel', required=True)
	channel_title = me.StringField(required=True)
	channel_thumbnail = me.URLField(required=True)
	video_id = me.ReferenceField('Video', required=True)
	text = me.MultiLineStringField(required=True)
	likes = me.LongField(required=True, default=0)
	time = me.StringField(required=True)
	edited = me.BooleanField(required=True, default=False)
	timestamp = me.LongField(required=True)
	has_replies = me.BooleanField(required=True, default=False)
	sentiment_category = me.StringField(choices=SENTIMENT_CATEGORIES)
