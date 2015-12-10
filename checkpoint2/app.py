#!flask/bin/python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api


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


# # POST: Create a new bucket list
# # GET: List all the created bucket lists
# @app.route('/bucketlists/', methods=['POST', 'GET'])
# def bucketlist_actions():
# 	return 'bucketlists'


# # GET: Get single bucket list
# # PUT: Update this bucket list
# # DELETE: Delete this single bucket list
# @app.route('/bucketlists/<id>', methods=['DELETE', 'GET', 'PUT'])
# def item(id):
# 	return id

# #Create a new item in bucket list
# @app.route('/bucketlists/<id>/items/', methods=['POST'])
# def bucketlist_item(id):
#     return id


# # PUT: Update a bucket list item
# # DELETE: Delete an item in a bucket list
# @app.route('/bucketlists/<id>/items/<item_id>', methods=['PUT', 'DELETE'])
# def get_bucketlists(id, item_id):
#     return id + " " + item_id


api.add_resource(Bucketlists, '/bucketlists/')
api.add_resource(Bucketlist, '/bucketlists/<id>')
api.add_resource(BucketlistItems, '/bucketlists/<id>/items/')
api.add_resource(BucketlistItem, '/bucketlists/<id>/items/<item_id>')

if __name__ == '__main__':
    app.run(debug=True)