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

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
