import falcon
from omt_ml_youtube.ml import Resource as ml_model


__version__ = '0.1'

api = application = falcon.API()

api.add_route(f'/api/v{__version__}/ml/youtube/classify', ml_model)
