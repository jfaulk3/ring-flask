from flask import Flask
from flask_restful import Api, Resource, abort, request
from ring_doorbell import Ring, Auth
import json
from pathlib import Path
from oauthlib.oauth2 import MissingTokenError
from flask_cors import CORS

app = Flask (__name__)
api = Api(app)
CORS(app)

cache_file = Path("test_token.cache")

def token_updated(token):
    cache_file.write_text(json.dumps(token))

class Code(Resource):
  def post(self):
    username = request.forms.get('username')
    password = request.forms.get('password')

    auth = Auth("PorchPals/1.0", None, token_updated)
    try:
        auth.fetch_token(username, password)
    except MissingTokenError:
        return {"data": "Code has been sent"}, 201
    except:
        abort(401, message="Username or Password is not valid...")
    return {"data": "Code has been sent"}, 201

class Video(Resource):
  def post(self):
    username = request.forms.get('username')
    password = request.forms.get('password')
    code = request.forms.get('code') or None

    auth = Auth("PorchPals/1.0", None, token_updated)
    try:
        auth.fetch_token(username, password)
    except MissingTokenError:
        auth.fetch_token(username, password, code)
    except:
      abort(401, message="Invalid Credentials...")

    ring = Ring(auth)
    ring.update_data()
    devices = ring.devices()
    doorbell = devices['doorbots'][0]
    videoUrl = doorbell.recording_url(doorbell.last_recording_id)
    return {"data": videoUrl}, 200

class HelloWorld(Resource):
  def get(self):
    return {"data": "Hello World!"}, 200

api.add_resource(Code,"/code")
api.add_resource(Video,"/video")
api.add_resource(HelloWorld, "/")

if __name__ == "__main__":
  app.run(debug=True)