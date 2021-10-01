from flask import Flask, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS 
from ApiHandler import ApiHandler

app = Flask(__name__, static_url_path='', static_folder='../src/build')
CORS(app)
api = Api(app)

@app.route("/", defaults={'path':''})
def serve(path): 
    return send_from_directory(app.static.folder, 'index.html')

api.add_resource(ApiHandler, '/flask/hello')