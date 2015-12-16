#!flask/bin/python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_restful.reqparse import RequestParser

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
api = Api(app)

from models import *
from resources import *


@app.route('/')
def index():
    return "API Root"

#Register a user
@app.route('/auth/register')
def create_user():
    return "Create User"

#Log a user in
@app.route('/auth/login', methods=['POST'])
def login():
    return "Login"

#Log a user out
@app.route('/auth/logout', methods=['GET'])
def logout():
    return "Logout"


api.add_resource(Bucketlists, '/bucketlists/')
api.add_resource(Bucketlist, '/bucketlists/<id>')
api.add_resource(BucketlistItems, '/bucketlists/<id>/items/')
api.add_resource(BucketlistItem, '/bucketlists/<id>/items/<item_id>')
api.add_resource(User, '/auth/register')
if __name__ == '__main__':
    app.run()