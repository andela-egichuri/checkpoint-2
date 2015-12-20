import os
import unittest
import flask.ext.testing
from .test_base import BaseTestCase
from checkpoint2.app import app, db
from checkpoint2.models import Bucketlist, Item


class TestBucketList(BaseTestCase):
    def test_bucketlist_creation_requires_authentication(self):
        response = self.client.post('/bucketlists/', data=dict(
            name='Bucketlist Name'))
        success_response = self.client.post('/bucketlists/', data=dict(
            name='Success Bucketlist Name'), headers={'token': self.token})
        bl = Bucketlist.query.filter_by(name='Success Bucketlist Name').one()
        self.assertEqual(bl.name, 'Success Bucketlist Name')
        self.assert_401(response)
        self.assert_200(success_response)

    def test_bucketlist_creation_succeeds_with_token(self):
        response = self.client.post('/bucketlists/', data=dict(
            name='Bucketlist Name'), headers={'token': self.token})
        bl = Bucketlist.query.filter_by(name='Bucketlist Name').one()
        self.assertIsInstance(response.json, dict)

    def test_get_bucketlists_requires_authentication(self):
        bl = Bucketlist.query.all()
        no_auth = self.client.get('/bucketlists/')
        get_bl = self.client.get('/bucketlists/', headers={'token': self.token})
        self.assertGreater(len(bl), 0)
        self.assert_401(no_auth)
        self.assert_200(get_bl)

    def test_update_bucketlists_requires_authentication(self):
        no_auth = self.client.put('/bucketlists/%s' % self.bl1.json['id'])
        put_bl = self.client.put('/bucketlists/%s' % self.bl1.json['id'], data=dict(
            name='Edited Bucketlist Name'), headers={'token': self.token})
        bl = Bucketlist.query.filter_by(id=self.bl1.json['id']).one()
        self.assertEqual(bl.name, 'Edited Bucketlist Name')
        self.assert_401(no_auth)
        self.assert_200(put_bl)

    def test_del_bucketlists_requires_authentication(self):
        no_auth = self.client.delete('/bucketlists/%s' % (self.bl1.json['id']))
        del_bl = self.client.delete('/bucketlists/%s' % (self.bl1.json['id']), headers={'token': self.token})
        bl = Bucketlist.query.all()
        self.assert_401(no_auth)
        self.assert_200(del_bl)

    def test_bucketlist_item_creation_requires_authentication(self):
        response = self.client.post('/bucketlists/%s/items/' % self.bl1.json['id'], data=dict(
            name='Bucketlist Item Name', done='0'))
        success_response = self.client.post('/bucketlists/%s/items/' % self.bl1.json['id'], data=dict(
            name='Success Bucketlist Item Name', done='0'), headers={'token': self.token})
        bli = Item.query.filter_by(name='Success Bucketlist Item Name').one()
        self.assertEqual(bli.name, 'Success Bucketlist Item Name')
        self.assert_401(response)
        self.assert_200(success_response)

    def test_update_bucketlist_item_requires_authentication(self):
        no_auth = self.client.put('/bucketlists/%s/items/%s' % (self.bl1.json['id'], self.bli1.json['id']))
        put_bl = self.client.put('/bucketlists/%s/items/%s' % (self.bl1.json['id'], self.bli1.json['id']), data=dict(
            name='Edited Bucketlist Item Name', done='1'), headers={'token': self.token})
        bli = Item.query.filter_by(id=self.bli1.json['id']).one()
        self.assertEqual(bli.name, 'Edited Bucketlist Item Name')
        self.assert_401(no_auth)
        self.assert_200(put_bl)

    def test_del_bucketlist_item_requires_authentication(self):
        count_before = Item.query.all()
        no_auth = self.client.delete('/bucketlists/%s/items/%s' % (self.bl1.json['id'], self.bli1.json['id']))
        del_bl = self.client.delete('/bucketlists/%s/items/%s' % (self.bl1.json['id'], self.bli1.json['id']), headers={'token': self.token})
        count_after = Item.query.all()
        self.assertEqual(len(count_after), len(count_before) - 1)
        self.assert_401(no_auth)
        self.assert_200(del_bl)

    def test_bucketlist_pagination(self):
        get_bl = self.client.get('/bucketlists/?limit=3', headers={'token': self.token})
        get_all = self.client.get('/bucketlists/', headers={'token': self.token})
        self.assertEqual(len(get_bl.json), 3)
        self.assertEqual(len(get_all.json), 5)

    def test_search_by_name(self):
        search_bl = self.client.get('/bucketlists/?q=First', headers={'token': self.token})
        self.assertEqual(search_bl.json[0]['name'], 'First Bucketlist')


if __name__ == '__main__':
    unittest.main()