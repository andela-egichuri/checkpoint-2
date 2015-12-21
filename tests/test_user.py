import os
import unittest
import flask.ext.testing
from .test_base import BaseTestCase
from flask.ext.login import current_user
from checkpoint2.app import app, db
from checkpoint2.models import User


class TestUser(BaseTestCase):
    """Test user functions."""

    def test_user_can_log_in(self):
        """Test login success.

        With correct login credentials a token should be returned and set the
        user online status as True.
        """
        success_response = self.client.post('/auth/login', data=dict(
            username='username', password='password'))
        user = db.session.query(User).filter_by(username='username').one()
        self.assertTrue(user.online)
        self.assertIn('token', success_response.json)
        self.assertNotIn('message', success_response.json)

    def test_wrong_login_credentials_fails(self):
        """Test login failure with wrong credentials.

        With wrong login credentials a token should not be returned. A `Login
        Failed` message should be returned
        """
        failed_response = self.client.post('/auth/login', data=dict(
            username='username', password='pass'))
        self.assertNotIn('token', failed_response.json)
        self.assertIn('message', failed_response.json)
        self.assertEqual(failed_response.json['message'], 'Login Failed')

    def test_user_can_log_out(self):
        """Test logout success.

        On logout a `logged out` message should be returned and the user online
        status as False.
        """
        get_token = self.client.post('/auth/login', data=dict(
            username='username', password='password'))
        token = get_token.json['token']
        user = db.session.query(User).filter_by(username='username').one()
        logout_response = self.client.post(
            '/auth/logout', headers={'token': token})
        self.assertFalse(user.online)
        self.assertEqual(logout_response.json['message'], 'logged out')

if __name__ == '__main__':
    unittest.main()