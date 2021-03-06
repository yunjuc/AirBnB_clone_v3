#!/usr/bin/python3
'''
    V1 of AirBnB API
'''
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def page_not_found(e):
    '''handle 404 page'''
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_app(error):
    '''
        close application
    '''
    storage.close()


if __name__ == "__main__":
    env_host = os.getenv('HBNB_API_HOST')
    env_port = os.getenv('HBNB_API_PORT')
    if env_host is None:
        env_host = '0.0.0.0'
    if env_port is None:
        env_port = 5000
    app.run(host=env_host, port=int(env_port))
