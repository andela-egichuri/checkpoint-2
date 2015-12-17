#!flask/bin/python
import os
from flask import Flask, flash, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_restful.reqparse import RequestParser
from flask_security import auth_token_required
from flask.ext.login import LoginManager, login_required, logout_user, login_user


app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)

import models
from resources import *


@app.route('/')
def index():
    return "API Root"


@app.route('/auth/login', methods=['POST'])
def login():
    # parser = RequestParser()
    # parser.add_argument('username', required=True)
    # parser.add_argument('password', required=True)
    # args = parser.parse_args()
    # username = args.username
    # password = args.password
    import ipdb
    # ipdb.set_trace()
    username = request.form['username']
    password = request.form['password']
    user = models.User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return jsonify({'message': 'Error: Username or Password is invalid'})
    login_user(user)
    return jsonify({'message': 'Logged in successfully'})


# @login_manager.request_loader
# def load_user(request):
#     token = request.headers.get('Authorization')
#     if token is None:
#         token = request.args.get('token')

#     if token is not None:
#         username,password = token.split(":") # naive token
#         user_entry = User.get(username)
#         if (user_entry is not None):
#             user = User(user_entry[0],user_entry[1])
#             if (user.password == password):
#                 return user
#     return None


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/auth/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return jsonify({'message' : 'logged out'})

api.add_resource(Bucketlists, '/bucketlists/')

api.add_resource(Bucketlist, '/bucketlists/<id>')
api.add_resource(BucketlistItems, '/bucketlists/<id>/items/')
api.add_resource(BucketlistItem, '/bucketlists/<id>/items/<item_id>')
api.add_resource(User, '/auth/register')


if __name__ == '__main__':
    app.run()