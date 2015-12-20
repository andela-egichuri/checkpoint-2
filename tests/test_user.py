import os
import unittest
import flask.ext.testing
from .test_base import BaseTestCase
from checkpoint2.app import app, db
from checkpoint2.models import User



class TestUser(BaseTestCase):
    def test_user_can_log_in(self):
        import ipdb; ipdb.set_trace()

    def test_user_can_log_out(self):
        pass



if __name__ == '__main__':
    unittest.main()