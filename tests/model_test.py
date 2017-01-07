#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement


import os
import sys
import datetime
import json
import StringIO
import inspect


from turbo.model import BaseModel
from bson.objectid import ObjectId

from pymongo import MongoClient
import gridfs

from util import unittest, fake_ids, fake_ids_2

mc = MongoClient()


class Tag(BaseModel):

    name = 'tag'
    field = {
        'list': (list, []),
        'imgid': (ObjectId, None),
        'uid': (ObjectId, None),
        'name': (basestring, None),
        'value': (int, 0),
        'atime': (datetime.datetime, None),
        'up': (dict, {}),
    }

    def __init__(self):
        db = {
            'db': {'test': mc['test']},
            'db_file': {'test': gridfs.GridFS(mc['test_files'])}
        }
        super(Tag, self).__init__('test', db)

    def write_action_call(self, name, *args, **kwargs):
        pass


class BaseModelTest(unittest.TestCase):

    def setUp(self):
        self.m = Tag()
        self._make_data()

    def tearDown(self):
        self._clear_data()
        del self.m

    def _make_data(self):
        for index, i in enumerate(fake_ids):
            self.m.insert_one({'_id': i, 'value': index})

    def _clear_data(self):
        for index, i in enumerate(fake_ids):
            self.m.remove_by_id(i)

    def test_insert(self):
        _id = self.m.insert({'value': 0})
        self.assertIsNot(_id, None)

    def test_save(self):
        _id = self.m.save({'value': 0})
        self.assertIsNot(_id, None)
        _id = self.m.save({'_id': _id, 'value': 10})
        result = self.m.find_by_id(_id)
        self.assertEqual(result['value'], 10)

    def test_update(self):
        with self.assertRaises(ValueError):
            self.m.update({}, {'hello': 0})

        self.m.update({}, {'$set': {'hellow': 0}})

        with self.assertRaises(ValueError):
            self.m.update({}, {})

        self.m.update({}, {'$set': {'value': 1}}, multi=True)
        for i in list(self.m.find()):
            self.assertEqual(i['value'], 1)

    def test_remove(self):
        with self.assertRaises(Exception):
            self.m.remove({})

        for i in fake_ids:
            self.m.remove({'_id': i})
            self.assertIsNone(self.m.find_by_id(i))

    def test_insert_one(self):
        result = self.m.insert_one({'value': 0})
        self.assertIsNot(result.inserted_id, None)

    def test_find_one(self):
        _id = self.m.insert({'value': 100})
        self.assertEqual(self.m.find_one({'_id': _id})['value'], 100)
        with self.assertRaises(KeyError):
            self.m.find_one({'_id': _id})['nokey']
        self.assertIsNone(
            self.m.find_one({'_id': _id}, wrapper=True)['nokey'])

        self.assertIsNone(self.m.find_one({'_id': ObjectId()}, wrapper=True))

    def test_find(self):
        self.assertGreater(list(self.m.find()), 0)
        for i in list(self.m.find()):
            with self.assertRaises(KeyError):
                i['nokey']

        for i in list(self.m.find(wrapper=True)):
            self.assertIsNone(i['nokey'])

    def test_update_one(self):
        with self.assertRaises(ValueError):
            self.m.update_one({}, {'hello': 0})

        self.m.update_one({}, {'$set': {'hellow': 0}})

    def test_update_many(self):
        with self.assertRaises(ValueError):
            self.m.update_many({}, {'hello': 0})

        self.m.update_many({}, {'$set': {'value': 1}})
        for i in list(self.m.find()):
            self.assertEqual(i['value'], 1)

    def test_delete_many(self):
        with self.assertRaises(Exception):
            self.m.delete_many({})

        for i in fake_ids:
            self.m.delete_many({'_id': i})
            self.assertIsNone(self.m.find_by_id(i))

    def test_put(self):
        value = 'hello word'
        s = StringIO.StringIO()
        s.write(value)
        # put
        file_id = self.m.put(s.getvalue())
        self.assertTrue(isinstance(file_id, ObjectId))

        # get
        one = self.m.get(file_id)
        self.assertTrue(getattr(one, 'read', False), 'test get fail')
        self.assertEqual(one.read(), value)

    def test_find_by_id(self):
        self.assertEqual(self.m.find_by_id(fake_ids[0])['_id'], fake_ids[0])
        for index, i in enumerate(self.m.find_by_id(fake_ids[0:10])):
            self.assertEqual(i['_id'], fake_ids[index])

    def test_get_as_dict(self):
        as_dict, as_list = self.m.get_as_dict({'_id': {'$in': fake_ids[0:10]}})
        for index, i in enumerate(as_dict.keys()):
            self.assertIn(i, fake_ids[0:10])

        for i in as_list:
            self.assertIn(i['_id'], fake_ids[0:10])

    def test_to_objectid(self):
        self.assertTrue(self.m.to_objectid(None) is None)
        self.assertEqual(self.m.to_objectid('52c8fb6f1d41c820f1124350'),
                         ObjectId('52c8fb6f1d41c820f1124350'), 'to_objectid is fail')

    def test_create_model(self):
        self.assertEqual(self.m.create_model('tag').find_one() is not None, True)

        with self.assertRaises(NotImplementedError):
            self.m.create_model('tag').create()

    def test_pymongo_collection_method(self):
        self.assertEqual(self.m.full_name, 'test.tag')

    def test_sub_collection(self):
        self.assertEqual(self.m.sub_collection('test').full_name, 'test.tag.test')

    def test_create(self):
        record = {
            'list': [
                {'key': ObjectId(), 'key2': 'test', 'key3': ObjectId()},
                10,
                12,
                13,
                ['name', 'name', 'name', ObjectId(), ObjectId()],
                datetime.datetime.now(),
            ],
            'imgid': ObjectId(),
            'up': {
                'key1': ObjectId(),
                'key2': ObjectId(),
                'key3': ObjectId(),
            }
        }

        result = self.m.create(record)
        self.assertIsInstance(result, ObjectId)

    def test_inc(self):
        _id = self.m.create({'value': 1})
        self.m.inc({'_id': _id}, 'value')
        self.assertEqual(self.m.find_by_id(_id)['value'], 2)

    def test_to_str(self):
        one = self.m.to_str(self.m.find(limit=10))
        self.assertTrue(isinstance(json.dumps(one), basestring))

    def test_to_one_str(self):
        one = self.m.to_one_str(self.m.find_one())
        self.assertTrue(isinstance(json.dumps(one), basestring))

    def test_write_action_call(self):
        def func(se, name, *args, **kwargs):
            self.assertEqual(name, 'save')

        def func2(se, name, *args, **kwargs):
            self.assertEqual(name, 'find')

        self.m.save({'value': 0})
        self.m.find()

    def test_default_encode(self):
        self.assertTrue(isinstance(self.m.default_encode(ObjectId()), basestring))
        self.assertTrue(isinstance(self.m.default_encode(datetime.datetime.now()), float))
        self.assertEqual(self.m.default_encode('string'), 'string')

    def log(self, one):
        print(one)


if __name__ == '__main__':
    unittest.main()