import json
import falcon
import random


CLASSES = [
    'opinion',
    'feedback',
    'abusive',
    'request',
    'supportive',
    'didactic',
    'question',
    'criticism',
    'admiration',
    'advice',
    'trash'
]


def classify(text):
	return CLASSES[random.randint(0, 10)]


class Resource:
    def on_get(req, resp):
        result_class = classify(req.get_param("t"))
        resp.body = json.dumps({"class": result_class})
        resp.status = falcon.HTTP_200
