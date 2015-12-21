import time
from flask import jsonify, abort, request
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequestKeyError
from passlib.apps import custom_app_context as pwd_context
from flask.ext.login import login_required, current_user
from flask_restful import Resource, fields, marshal
import models
from app import db


bli_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'done': fields.Boolean,
}

bl_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.String,
    'date_modified': fields.String,
    'bl_items': fields.Nested(bli_fields),
    'created_by': fields.String
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'online': fields.Boolean,
    'bucketlists': fields.Nested(bl_fields)
}


class Bucketlists(Resource):
    """Resource for showing all and adding bucketlists."""

    decorators = [login_required]

    def get(self):
        """List bucketlists from authenticated user.

        `limit` specifies the number of results
        `q` specifies the search term
        """
        try:
            limit = int(request.args['limit'])
        except BadRequestKeyError:
            limit = 20

        if limit > 100:
            limit = 20

        try:
            q = request.args['q']
        except BadRequestKeyError:
            q = ''

        try:
            bl = (models.Bucketlist).query.filter(
                models.Bucketlist.created_by == current_user.id,
                models.Bucketlist.name.like('%' + q + '%')).paginate(1, limit)
            return marshal(bl.items, bl_fields)
        except:
            return {'message': 'No Result'}, 400

    def post(self):
        """Create a bucketlist"""
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('date_created')
        parser.add_argument('date_modified')
        args = parser.parse_args()
        current_date = time.strftime('%Y/%m/%d %H:%M:%S')
        bl = models.Bucketlist(name=args.name, date_created=current_date,
            date_modified=current_date, created_by=int(current_user.id))
        try:
            db.session.add(bl)
            db.session.commit()
            return marshal(bl, bl_fields)

        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'Error Updating'}


class BucketlistResource(Resource):
    """Resource for single bucketlist operations."""

    decorators = [login_required]

    def get(self, id):
        """Show the bucketlist specified by id."""
        try:
            bl = db.session.query(models.Bucketlist).filter_by(id=id).one()
            return marshal(bl, bl_fields)
        except SQLAlchemyError:
            return {'message': 'No Result'}, 400

    def put(self, id):
        """Update the bucketlist specified by id."""
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        args = parser.parse_args()
        bl = db.session.query(models.Bucketlist).filter_by(id=id).one()
        bl.name = args.name
        bl.date_modified = time.strftime('%Y/%m/%d %H:%M:%S')
        try:
            db.session.commit()
            return marshal(bl, bl_fields)
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'Error Updating'}

    def delete(self, id):
        """Delete a bucketlist specified by id."""
        try:
            bq = db.session.query(models.Bucketlist).filter_by(id=id).one()
            db.session.delete(bq)
            db.session.commit()
            if bq:
                return {'message': 'Deleted'}
            else:
                return {'message': 'No Bucketlist with the given ID'}
        except SQLAlchemyError:
            db.session.rollback()
        return {'message': 'Error Deleting'}


class BucketlistItem(Resource):
    """Resource for single bucketlist items operations."""

    decorators = [login_required]

    def get(self, id, item_id):
        """Show an item from bucketlist `id` specified by `item_id`."""
        try:
            bqi = db.session.query(models.Item).filter_by(
                bucketlist_id=id, id=item_id).one()
            return marshal(bqi, bli_fields)
        except SQLAlchemyError:
            return {'message': 'No Result'}, 400

    def put(self, id, item_id):
        """Edit an item from bucketlist `id` specified by `item_id`."""
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('done')
        args = parser.parse_args()
        bli = db.session.query(models.Item).filter_by(
            bucketlist_id=id, id=item_id).one()
        bli.name = args.name
        bli.done = args.done
        bli.date_modified = time.strftime('%Y/%m/%d %H:%M:%S')
        try:
            db.session.commit()
            return marshal(bli, bli_fields)
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'Error Updating'}

    def delete(self, id, item_id):
        """Delete an item from bucketlist `id` specified by `item_id`."""
        try:
            bqi = db.session.query(models.Item).filter_by(
                bucketlist_id=id, id=item_id).one()
            db.session.delete(bqi)
            db.session.commit()
            if bqi:
                return {'message': 'Deleted'}
            else:
                return {'message': 'No Bucketlist item with the given ID'}
        except SQLAlchemyError:
            db.session.rollback()
        return {'message': 'Error Deleting'}


class BucketlistItems(Resource):
    """Resource adding bucketlist items"""

    decorators = [login_required]

    def post(self, id):
        """Add an item to specified bucketlist `id`."""
        parser = RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('date_created')
        parser.add_argument('date_modified')
        parser.add_argument('done')
        parser.add_argument('bucketlist_id')
        args = parser.parse_args()

        current_date = time.strftime('%Y/%m/%d %H:%M:%S')
        bli = models.Item(
            name=args.name, date_created=current_date,
            date_modified=current_date, done=args.done, bucketlist_id=id)

        try:
            db.session.add(bli)
            db.session.commit()
            return marshal(bli, bli_fields)
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'Error Deleting'}


class UserResource(Resource):
    """Resource for showing and adding users."""

    def get(self):
        """Show all users."""
        try:
            users = db.session.query(models.User).all()
            return marshal(users, user_fields)
        except SQLAlchemyError:
            return {'message': 'No Result'}, 400

    def post(self):
        """Add(register) a user."""
        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        if args.username is None or args.password is None:
            return {'message': 'Fields required'}
            abort(400)
        if models.User.query.filter_by(username=args.username).first() is not None:
            return {'message': 'Username taken'}
            abort(400)
        if models.User.query.filter_by(email=args.email).first() is not None:
            return {'message': 'Email taken'}
            abort(400)
        user = models.User(username=args.username, email=args.email)
        user.hash_password(args.password)
        try:
            db.session.add(user)
            db.session.commit()
            return {'message': 'user created'}, 201
        except SQLAlchemyError:
            db.session.rollback()
            return {'message': 'Error creating user'}

