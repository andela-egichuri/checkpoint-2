import os
import unittest
import flask.ext.testing
from .test_base import BaseTestCase
from checkpoint2.app import app, db
from checkpoint2.models import Bucketlist



class TestBucketList(BaseTestCase):
    def test_bucketlist_creation_requires_authentication(self):
        pass

    def test_bucketlist_creation_succeeds_with_token(self):
        pass

    def test_bucketlist_pagination(self):
        pass


if __name__ == '__main__':
    unittest.main()