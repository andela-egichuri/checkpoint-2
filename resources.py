from app import db
import time
from flask import jsonify, abort
from flask_restful.reqparse import RequestParser
from passlib.apps import custom_app_context as pwd_context

from flask_restful import Resource, fields, marshal
import models




bli_fields = {
	'id' : fields.Integer,
	'name' : fields.String,
	'date_created' : fields.String ,
	'date_modified' : fields.String,
	'done' : fields.Boolean,
}

bl_fields = {
	'id' : fields.Integer,
	'name' : fields.String,
	'date_created' : fields.String ,
	'date_modified' : fields.String,
	'items' : fields.Nested(bli_fields)
}

# /bucketlists/
class Bucketlists(Resource):
	def get(self):
		try:
			bq = db.session.query(models.Bucketlist).all()
			return marshal(bq, bl_fields)

		except:
			return { 'Error' : 'No Result'}, 400

	def post(self):
		parser = RequestParser()
		parser.add_argument('name', type=str, required=True)
		parser.add_argument('date_created')
		parser.add_argument('date_modified')
		args = parser.parse_args()
		q = db.session.query

		bl = models.Bucketlist(name=args.name, date_created=time.strftime("%x"),
			date_modified=time.strftime("%x"))
		try:
			db.session.add(bl)
			db.session.commit()

		except:
			db.session.rollback()
			return {'Error' : 'Error Updating'}



# /bucketlists/<id>
class Bucketlist(Resource):
	def get(self, id):
		try:
			bq = db.session.query(models.Bucketlist).filter_by(id=id).one()
			return marshal(bq, bl_fields)
		except:
			return { 'Error' : 'No Result'}, 400

	def put(self, id):
		parser = RequestParser()
		parser.add_argument('name', type=str, required=True)
		parser.add_argument('date_modified')
		args = parser.parse_args()
		bl = db.session.query(models.Bucketlist).filter_by(id=id).one()
		bl.name = args.name
		bl.date_modified=time.strftime("%x")
		try:
			db.session.commit()
		except:
			db.session.rollback()
			return {'Error' : 'Error Updating'}


	def delete(self, id):
		try:
			bq = db.session.query(models.Bucketlist).filter_by(id=id).delete()
		except:
			db.session.rollback()
			return {'Error' : 'Error Deleting'}


# /bucketlists/<id>/items/<item_id>
class BucketlistItem(Resource):
	def get(self, id, item_id):
		try:
			bqi = db.session.query(models.Item).filter_by(bucketlist_id=id, id=item_id).one()
			return marshal(bqi, bli_fields)
		except:
			return { 'Error' : 'No Result'}, 400

	def put(self, id, item_id):
		parser = RequestParser()
		parser.add_argument('name', type=str, required=True)
		parser.add_argument('date_modified')
		parser.add_argument('done')
		args = parser.parse_args()
		# Get a SQL Alchemy query object
		bli = db.session.query(models.Item).filter_by(bucketlist_id=id, id=item_id).one()
		bli.name = args.name
		bli.done = args.done
		bli.date_modified=time.strftime("%x")
		try:
			db.session.commit()
		except:
			db.session.rollback()
			return {'Error' : 'Error Updating'}

	def delete(self, id, item_id):
		try:
			bqi = db.session.query(models.Item).filter_by(bucketlist_id=id, id=item_id).delete()
		except:
			db.session.rollback()
			return {'Error' : 'Error Deleting'}

# /bucketlists/<id>/items/
class BucketlistItems(Resource):
	def post(self, id):
		parser = RequestParser()
		parser.add_argument('name', type=str, required=True)
		parser.add_argument('date_created')
		parser.add_argument('date_modified')
		parser.add_argument('done')
		parser.add_argument('bucketlist_id')
		args = parser.parse_args()

		q = db.session.query

		bli = models.Item(name=args.name, date_created=time.strftime("%x"),
			date_modified=time.strftime("%x"), done=args.done, bucketlist_id=id)

		try:
			db.session.add(bli)
			db.session.commit()
		except:
			db.session.rollback()
			return {'Error' : 'Error Deleting'}




class User(Resource):
	def get(self):
		parser = RequestParser()
		parser.add_argument('username', type=str, required=True)
		parser.add_argument('password', required=True)
		args = parser.parse_args()

	def post(self):
		parser = RequestParser()
		parser.add_argument('username', type=str, required=True)
		parser.add_argument('email', required=True)
		parser.add_argument('password', required=True)
		args = parser.parse_args()

		if args.username is None or args.password is None:
			return {'Error' : 'Fields required'}
			abort(400) # missing arguments
		if models.User.query.filter_by(username=args.username).first() is not None:
			return {'Error' : 'Username exists'}
			abort(400) # existing user
		if models.User.query.filter_by(email=args.email).first() is not None:
			return {'Error' : 'Email exists'}
			abort(400) # existing user
		q = db.session.query
		password_hash = pwd_context.encrypt(args.password)
		user = models.User(username=args.username, email=args.email,
			password=password_hash)
		try:
			db.session.add(user)
			db.session.commit()
			return { 'username': user.username }, 201
		except:
			db.session.rollback()
			return {'Error' : 'Error creating user'}

	def put(self):
		pass

	def delete(self):
		pass

