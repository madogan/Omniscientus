import os

import pymongo
from flask import Flask

from omniscientus.utils.CJSON import CJSON
from omniscientus.utils.youtube_api.YoutubeConnection import YoutubeConnection
from .config import app_config

# mongodb client
mongo_client = pymongo.MongoClient(os.environ.get('MONGO_URI'))
db = mongo_client["omniscientus"]


def create_app():
    app = Flask(__name__)

    app.config.from_object(app_config[os.environ.get("FLASK_ENV")])
    app.config.from_pyfile('config.py')

    app.json_encoder = CJSON

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    from . import home
    app.register_blueprint(home.bp)

    from . import api
    app.register_blueprint(api.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    # from . import user
    # app.register_blueprint(user.bp)
    
    return app
