from flask import Flask
from flask_restful import Api, Resource, abort, request
from ring_doorbell import Ring, Auth
"""Python Ring Doorbell wrapper."""
import json
from pathlib import Path
from oauthlib.oauth2 import MissingTokenError

app = Flask (__name__)
api = Api(app)

class getCode(Resource):
  def post(self):
    username = request.forms.get('username')
    password = request.forms.get('password')

    auth = Auth("PorchPals/1.0", None, token_updated)
    try:
        auth.fetch_token(username, password)
    except MissingTokenError:
        return {"data": ""}, 201
    except:
        abort(401, message="Username or Password is not valid...")
    return {"data": ""}, 201

class HelloWorld(Resource):
  def get(self):
    return {"data": "Hello World!"}

api.add_resource(getCode,"/getcode")
api.add_resource(HelloWorld, "/helloworld")
if __name__ == "__main__":
  app.run(debug=True)