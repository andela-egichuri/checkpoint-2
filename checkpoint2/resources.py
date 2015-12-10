from flask_restful import Resource, Api


# /bucketlists/
class Bucketlists(Resource):
	def get(self):
		pass

	def post(self):
		pass


# /bucketlists/<id>
class Bucketlist(Resource):
	def get(self, id):
		return id

	def put(self, id):
		pass

	def delete(self, id):
		pass

# /bucketlists/<id>/items/<item_id>
class BucketlistItem(Resource):
	def get(self, id, item_id):
		return id + ' ' + item_id

	def put(self, id, item_id):
		pass

	def delete(self, id, item_id):
		pass

# /bucketlists/<id>/items/
class BucketlistItems(Resource):
	def post(self, id):
		pass


class User(Resource):
	def get(self):
		pass

	def post(self):
		pass

	def put(self):
		pass

	def delete(self):
		pass

