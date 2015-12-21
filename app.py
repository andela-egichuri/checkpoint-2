#!flask/bin/python
import os
import base64
from flask import Flask, request, Response, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask.ext.login import LoginManager, logout_user, login_required, \
    current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    BadSignature, SignatureExpired
import config
app = Flask(__name__)

# app.config.from_object(os.environ.get('APP_SETTINGS'))
app.config.from_object(config.DevelopmentConfig)
# app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_serializer = Serializer(app.config['SECRET_KEY'])


from models import *
from resources import *


@app.route('/')
def index():
    return "API Root"


@app.route('/auth/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return jsonify({'message': 'Login Failed'})
    token = user.generate_auth_token()
    user = db.session.query(User).filter_by(username=username).one()
    user.online = '1'
    try:
        db.session.commit()
    except:
        db.session.rollback()
    return jsonify({'token': token})


@login_manager.request_loader
def load_user(request):
    auth_key = request.headers.get('Authorization')
    if auth_key:
        auth_key = auth_key.replace('Basic ', '', 1)
        try:
            auth_key = base64.b64decode(auth_key)
            username, password = auth_key.split(":")
            user = User.query.filter_by(username=username).first()
            if not user or not user.verify_password(password):
                return False
        except TypeError:
            return False
        return user
    token = request.headers.get('token')
    if token:
        try:
            data = login_serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data[0])
        if user.password == data[1] and user.online:
            return user
    return None


@app.route('/auth/logout', methods=['GET', 'POST'])
@login_required
def logout():
    current_user.online = '0'
    try:
        db.session.commit()
        return jsonify({'message': 'logged out'})
    except:
        db.session.rollback()
    return jsonify({'message': 'error'})


api.add_resource(Bucketlists, '/bucketlists/')
api.add_resource(BucketlistResource, '/bucketlists/<id>')
api.add_resource(BucketlistItems, '/bucketlists/<id>/items/')
api.add_resource(BucketlistItem, '/bucketlists/<id>/items/<item_id>')
api.add_resource(UserResource, '/auth/register')


if __name__ == '__main__':
    app.run()
