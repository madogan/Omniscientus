# -*- coding: utf-8 -*-

import mongoengine as me  # ORM of MongoDB


class User(me.Document):
	"""
		Schema for User created using 'mongoengine'

		Fields:
			name (str): User permanent name.
			password (str): User password.
			email (EmailField): user email address.
			phone (str): User phone number.
			youtube_channel_id (Channel): Youtube channel of the user referenced to Channel.

	"""

	name = me.StringField(required=True)
	password = me.StringField(required=True)
	email = me.EmailField(required=True)
	phone = me.StringField(default=None)
	youtube_channel_id = me.ReferenceField('Channel', required=True)
