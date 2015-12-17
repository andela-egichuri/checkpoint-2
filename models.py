from app import db
from flask.ext.login import UserMixin
from passlib.apps import custom_app_context as pwd_context


class Bucketlist(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	date_created = db.Column(db.DateTime)
	date_modified = db.Column(db.DateTime)
	items = db.relationship('Item')
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))


class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(100))
	date_created = db.Column(db.DateTime)
	date_modified = db.Column(db.DateTime)
	done = db.Column(db.Boolean)
	bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))


class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(128))

	def hash_password(self, password):
		self.password = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def __repr__(self):
		return '<User %r>' % (self.username)
