# CJSON --> Customized JSON Class

import json
import datetime

from bson.objectid import ObjectId


class CJSON(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)
