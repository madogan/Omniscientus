# -*- coding: utf-8 -*-

import mongoengine as me  # ORM of MongoDB


class Video(me.Document):
	"""
		Schema for Video created using 'mongoengine'

		Fields:
			video_id (str): Youtube defined unique id for video.
			title (str): Actually Youtube video name.
			description (dict): Description of the video.
			thumbnails (dict): Video image urls in three different sizes.
			category_id (dict): Video category id provided by Youtube.
			tags (str): Video tags provided by user.
			channel_id (float): Owner of the video.
			yt_statistics (int): Basic statistics provided by Youtube.
			comments (list of Comment): Comments have sent by Youtube users to the video.

		TODO:
			* It is needed to add sentiment class distributions of the video according to comments sentiment analysis
			* Class sentiment distrubitons must be updated peridoically.

	"""

	video_id = me.StringField(primary_key=True, min_length=11, max_length=11)
	title = me.StringField(required=True)
	description = me.MultiLineStringField(required=True, default="")
	thumbnails = me.DictField(required=True)
	category_id = me.IntField(required=True)
	tags = me.ListField(me.StringField(), required=True)
	channel_id = me.ReferenceField('Channel', required=True)
	yt_statistics = me.DictField(required=True)
	comments = me.ListField(me.ReferenceField('Comment'), default=list)
