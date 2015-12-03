from app import db


class Bucketlist(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	date_created = db.Column(db.DateTime)
	date_modified = db.Column(db.DateTime)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	date_created = db.Column(db.DateTime)
	date_modified = db.Column(db.DateTime)
	done = db.Column(db.Boolean)
	bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(128))


