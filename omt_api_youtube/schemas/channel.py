# -*- coding: utf-8 -*-

import mongoengine as me  # ORM of MongoDB


class Channel(me.Document):
	"""
		Schema for Channel created using 'mongoengine'

		Fields:
			channel_id (str): Youtube defined unique id for channel.
			channel_title (str): Actually Youtube channel name.
			thumbnails (dict): Profile image urls in three different sizes.
			topic_details (dict): Topic information provided by Youtube.
			yt_statistics (dict): Basic statistics provided by Youtube.
			score (float): Value of comments according to analysis of old comments of the channel.
			commentators (list of Channel): Channels who have sent comment ot the channel.
			num_commentators (int): Number of commentators.
			fans (list of Channel): Channels which are also commentator but more valuable for the channel.
			num_fans (int): Number of channels.

		TODO:
			* It is needed to add sentiment class distributions of the channel according to comments sentiment analysis
			* Class sentiment distrubitons must be updated peridoically.

	"""

	channel_id = me.StringField(primary_key=True, min_length=24, max_length=24)
	channel_title = me.StringField(required=True)
	thumbnails = me.DictField(required=True)
	topic_details = me.DictField(required=True)
	yt_statistics = me.DictField(required=True)
	score = me.DecimalField(min_value=-1, max_value=1, precision=4)
	commentators = me.ListField(me.ReferenceField('self'), default=list)
	num_commentators = me.LongField(min_value=0, default=0)
	fans = me.ListField(me.ReferenceField('self'), default=list)
	num_fans = me.LongField(min_value=0, default=0)
