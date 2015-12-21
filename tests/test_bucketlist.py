import os
import unittest
import flask.ext.testing
from .test_base import BaseTestCase
from checkpoint2.app import app, db
from checkpoint2.models import Bucketlist, Item


class TestBucketList(BaseTestCase):
    """Class to test bucketlists"""

    def test_bucketlist_creation_requires_authentication(self):
        """Test the method to create a new bucket list requires authentication.

        If the user is authenticated a 401 UNAUTHORIZED response should be returned
        With an authentication token a 200 OK response should be returned.
        The Bucketlist table should contain a bucketlist called `Success
        Bucketlist Name`
        """
        response = self.client.post('/bucketlists/', data=dict(
            name='Bucketlist Name'))
        success_response = self.client.post('/bucketlists/', data=dict(
            name='Success Bucketlist Name'), headers={'token': self.token})
        bl = Bucketlist.query.filter_by(name='Success Bucketlist Name').one()
        self.assertEqual(bl.name, 'Success Bucketlist Name')
        self.assert_401(response)
        self.assert_200(success_response)

    def test_get_bucketlists_requires_authentication(self):
        """Test the method to list created bucketlists requires authentication.

        If the user is authenticated a 401 UNAUTHORIZED response should be returned
        With an authentication token a 200 OK response should be returned. Since
        the SetUp function adds test bucketlists the successful response should
        contain 1 or more items
        """
        bl = Bucketlist.query.all()
        no_auth = self.client.get('/bucketlists/')
        get_bl = self.client.get('/bucketlists/', headers={'token': self.token})
        self.assertGreater(len(bl), 0)
        self.assert_401(no_auth)
        self.assert_200(get_bl)

    def test_update_bucketlists_requires_authentication(self):
        """Test the method to update a bucketlist requires authentication.

        If the user is authenticated a 401 UNAUTHORIZED response should be returned
        With an authentication token a 200 OK response should be returned.
        The Bucketlist table should contain a bucketlist called `Edited Bucketlist
        Name`
        """
        no_auth = self.client.put('/bucketlists/{0}'.format(self.bl1.json['id']))
        put_bl = self.client.put('/bucketlists/{0}'.format(self.bl1.json['id']), data=dict(
            name='Edited Bucketlist Name'), headers={'token': self.token})
        bl = Bucketlist.query.filter_by(id=self.bl1.json['id']).one()
        self.assertEqual(bl.name, 'Edited Bucketlist Name')
        self.assert_401(no_auth)
        self.assert_200(put_bl)

    def test_del_bucketlists_requires_authentication(self):
        """Test the method to delete a bucketlist requires authentication.

        If the user is authenticated a 401 UNAUTHORIZED response should be returned
        With an authentication token a 200 OK response and a Deleted message
        should be returned. The Bucketlist table should contain one item less
        from the initial count defined in SetUp
        """
        no_auth = self.client.delete('/bucketlists/{0}'.format(self.bl1.json['id']))
        del_bl = self.client.delete('/bucketlists/{0}'.format(self.bl1.json['id']), headers={'token': self.token})
        bl = Bucketlist.query.all()
        self.assertEqual(del_bl.json['message'], 'Deleted')
        self.assertEqual(len(bl), self.initial_count - 1)
        self.assert_401(no_auth)
        self.assert_200(del_bl)

    def test_bucketlist_item_creation_requires_authentication(self):
        """Test the method to create a bucketlist item requires authentication.

        If the user is authenticated a 401 UNAUTHORIZED response should be returned
        With an authentication token a 200 OK response should be returned.
        The Item table should contain a bucket called `Success Bucketlist Item
        Name`
        """
        response = self.client.post('/bucketlists/{0}/items/'.format(self.bl1.json['id']), data=dict(
            name='Bucketlist Item Name', done='0'))
        success_response = self.client.post('/bucketlists/{0}/items/'.format(self.bl1.json['id']), data=dict(
            name='Success Bucketlist Item Name', done='0'), headers={'token': self.token})
        bli = Item.query.filter_by(name='Success Bucketlist Item Name').one()
        self.assertEqual(bli.name, 'Success Bucketlist Item Name')
        self.assert_401(response)
        self.assert_200(success_response)

    def test_update_bucketlist_item_requires_authentication(self):
        """Test the method to update a bucketlist item requires authentication.

        If the user is authenticated a 401 UNAUTHORIZED response should be returned
        With an authentication token a 200 OK response should be returned.
        The Item table should contain a bucketlist item called `Edited Bucketlist
        Item Name`
        """
        no_auth = self.client.put('/bucketlists/{0}/items/{1}'.format(
            self.bl1.json['id'], self.bli1.json['id']))
        put_bl = self.client.put('/bucketlists/{0}/items/{1}'.format(
            self.bl1.json['id'], self.bli1.json['id']), data=dict(
            name='Edited Bucketlist Item Name', done='1'), headers={'token': self.token})
        bli = Item.query.filter_by(id=self.bli1.json['id']).one()
        self.assertEqual(bli.name, 'Edited Bucketlist Item Name')
        self.assert_401(no_auth)
        self.assert_200(put_bl)

    def test_del_bucketlist_item_requires_authentication(self):
        """Test the method to delete a bucketlist item requires authentication.

        If the user is authenticated a 401 UNAUTHORIZED response should be returned
        With an authentication token a 200 OK response and a Deleted message
        should be returned. The Item table should contain one entry less
        from the count before deletion
        """
        count_before = Item.query.all()
        no_auth = self.client.delete('/bucketlists/{0}/items/{1}'.format(
            self.bl1.json['id'], self.bli1.json['id']))
        del_bl = self.client.delete('/bucketlists/{0}/items/{1}'.format(
            self.bl1.json['id'], self.bli1.json['id']), headers={'token': self.token})
        count_after = Item.query.all()
        self.assertEqual(del_bl.json['message'], 'Deleted')
        self.assertEqual(len(count_after), len(count_before) - 1)
        self.assert_401(no_auth)
        self.assert_200(del_bl)

    def test_bucketlist_pagination(self):
        """Test bucketlist pagination.

        Querying all items should return a json result with 5 items. With a limit
        only the number of items specified should be returned
        """
        get_bl = self.client.get('/bucketlists/?limit=3', headers={'token': self.token})
        get_all = self.client.get('/bucketlists/', headers={'token': self.token})
        self.assertEqual(len(get_bl.json), 3)
        self.assertEqual(len(get_all.json), 5)

    def test_search_by_name(self):
        """Test bucketlist search.

        Specifying a search term should return bucketlists containing the search
        term in their name
        """
        search_bl = self.client.get('/bucketlists/?q=First', headers={'token': self.token})
        self.assertEqual(search_bl.json[0]['name'], 'First Bucketlist')


if __name__ == '__main__':
    unittest.main()