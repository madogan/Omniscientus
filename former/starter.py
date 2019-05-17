import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--app", help="flask app name, default omniscientus")
parser.add_argument("--env", help="development or product environment, default development")
parser.add_argument("--mongo_uri", help="uri for mongodb, default mongodb://localhost:27017/omniscientus")
parser.add_argument("--host", help="host")

args = parser.parse_args()

FLASK_APP = "omniscientus/__init__.py"
FLASK_ENV = "development"
MONGO_URI = "mongodb://localhost:27017/omniscientus"
HOST = "0.0.0.0"

if args.app: FLASK_APP = args.app
if args.env: FLASK_ENV = args.env
if args.mongo_uri: MONGO_URI = args.mongo_uri
if args.host: HOST = args.host

os.system("export FLASK_APP={} && export FLASK_ENV={} && export MONGO_URI={} && "
          "python -m flask run --host {}".format(FLASK_APP, FLASK_ENV, MONGO_URI, HOST))
