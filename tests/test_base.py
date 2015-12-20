from flask.ext.testing import TestCase

from checkpoint2.app import app, db
from checkpoint2.config import TestingConfig


class BaseTestCase(TestCase):
    """A base test case for."""

    def create_app(self):
        app.config.from_object(TestingConfig)
        self.client = app.test_client()
        return app

    def setUp(self):
        db.create_all()
        self.create_user = self.client.post('/auth/register', data=dict(
            username='username', password='password', email='email@email.com'))
        get_token = self.client.post('/auth/login', data=dict(
            username='username', password='password'))
        self.token = get_token.json['token']
        self.bl1 = self.client.post('/bucketlists/', data=dict(
            name='First Bucketlist'), headers={'token': self.token})
        self.bl2 = self.client.post('/bucketlists/', data=dict(
            name='Second Bucketlist'), headers={'token': self.token})
        self.bl3 = self.client.post('/bucketlists/', data=dict(
            name='Third Bucketlist'), headers={'token': self.token})
        self.bl4 = self.client.post('/bucketlists/', data=dict(
            name='Forth Bucketlist'), headers={'token': self.token})
        self.bl5 = self.client.post('/bucketlists/', data=dict(
            name='Fifth Bucketlist'), headers={'token': self.token})

        self.bli1 = self.client.post('/bucketlists/%s/items/' % self.bl1.json['id'], data=dict(
            name='First Bucketlist Item Name', done='0'), headers={'token': self.token})
        self.bli2 = self.client.post('/bucketlists/%s/items/' % self.bl1.json['id'], data=dict(
            name='Second Bucketlist Item Name', done='1'), headers={'token': self.token})

        resp = self.client.get('/bucketlists/', headers={'token': self.token})
        self.initial_count = len(resp.json)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
