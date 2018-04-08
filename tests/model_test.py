# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import datetime
import json

from bson.objectid import ObjectId
import gridfs
from pymongo import MongoClient
from turbo.model import BaseModel
from turbo.util import PY3, basestring_type as basestring, utf8
from util import unittest, fake_ids, fake_ids_2

if PY3:
    from io import StringIO
else:
    from cStringIO import StringIO

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
        self.tb_tag = Tag()
        self._make_data()

    def tearDown(self):
        self._clear_data()
        del self.tb_tag

    def _make_data(self):
        for index, i in enumerate(fake_ids):
            self.tb_tag.insert_one({'_id': i, 'value': index})

    def _clear_data(self):
        for index, i in enumerate(fake_ids):
            self.tb_tag.remove_by_id(i)

        for index, i in enumerate(fake_ids_2):
            self.tb_tag.remove_by_id(i)

    def test_insert(self):
        _id = self.tb_tag.insert({'value': 0})
        self.assertIsNot(_id, None)
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

        result = self.tb_tag.insert(record)
        self.assertIsInstance(result, ObjectId)

        # insert one
        _id = self.tb_tag.insert({'_id': fake_ids_2[0]})
        self.assertEqual(_id, fake_ids_2[0])
        result = self.tb_tag.find_by_id(fake_ids_2[0])
        self.assertEqual(result['value'], 0)

        # insert not field
        with self.assertRaises(Exception):
            result = self.tb_tag.insert({'nokey': 10})

        # check
        _id = self.tb_tag.insert({'imgid': None})
        self.assertIsNot(_id, None)
        result = self.tb_tag.find_by_id(_id)
        self.assertEqual(result['value'], 0)
        self.tb_tag.remove_by_id(_id)

        docs = [{'_id': i} for i in fake_ids_2[1:]]
        result = self.tb_tag.insert(docs)
        self.assertEqual(1, len(result))
        for i in result:
            self.assertIn(i, fake_ids_2)
        result = self.tb_tag.find_by_id(fake_ids_2[1:])
        self.assertEqual(1, len(result))
        for i in result:
            self.assertEqual(i['value'], 0)

    def test_save(self):
        _id = self.tb_tag.save({'value': 0})
        self.assertIsNot(_id, None)
        _id = self.tb_tag.save({'_id': _id, 'value': 10})
        result = self.tb_tag.find_by_id(_id)
        self.assertEqual(result['value'], 10)
        self.tb_tag.remove_by_id(_id)

    def test_update(self):
        with self.assertRaises(ValueError):
            self.tb_tag.update({}, {'hello': 0})

        self.tb_tag.update({}, {'$set': {'hello': 0}})

        # update all empty
        with self.assertRaises(ValueError):
            self.tb_tag.update({}, {})

        # update one
        self.tb_tag.update({'_id': fake_ids[0]}, {'$set': {'value': 11}})
        result = self.tb_tag.find_by_id(fake_ids[0])
        self.assertEqual(result['value'], 11)

        # update one
        result = self.tb_tag.update({'_id': {'$in': fake_ids[1:11]}}, {
                                    '$set': {'value': 11}})
        self.assertEqual(result.matched_count, 1)
        if result.modified_count is not None:
            self.assertEqual(result.modified_count, 1)

        # update many
        result = self.tb_tag.update({'_id': {'$in': fake_ids[2:12]}}, {
                                    '$set': {'value': -1}}, multi=True)
        print(result)
        self.assertEqual(result.matched_count, 10)
        # modified_count 反应的是实际修改的文档数目，如果要修改键的值和修改值是相同的，文档不会被修改
        if result.modified_count is not None:
            self.assertEqual(result.modified_count, 10)

    def test_remove(self):
        # not allow remove all
        with self.assertRaises(Exception):
            self.tb_tag.remove({})

        result = self.tb_tag.find_by_id(fake_ids[0])
        self.assertEqual(result['_id'], fake_ids[0])

        self.tb_tag.remove({'_id': fake_ids[0]})
        result = self.tb_tag.find_by_id(fake_ids[0])
        self.assertEqual(result, None)

        # remove one
        self.tb_tag.remove({'_id': {'$in': fake_ids[2:12]}})
        result = self.tb_tag.find_by_id(fake_ids[2:12])
        self.assertEqual(len(list(result)), 9)
        # remove many
        self.tb_tag.remove({'_id': {'$in': fake_ids[3:13]}}, multi=True)
        result = self.tb_tag.find_by_id(fake_ids[3:13])
        self.assertEqual(len(list(result)), 0)

    def test_insert_one(self):
        result = self.tb_tag.insert_one({'value': 0})
        self.assertIsNot(result.inserted_id, None)

    def test_find_one(self):
        _id = self.tb_tag.insert({'value': 100})
        self.assertEqual(self.tb_tag.find_one({'_id': _id})['value'], 100)
        with self.assertRaises(KeyError):
            self.tb_tag.find_one({'_id': _id})['nokey']
        self.assertIsNone(
            self.tb_tag.find_one({'_id': _id}, wrapper=True)['nokey'])

        self.assertIsNone(self.tb_tag.find_one(
            {'_id': ObjectId()}, wrapper=True))

    def test_find(self):
        self.assertGreater(len(list(self.tb_tag.find())), 0)
        for i in list(self.tb_tag.find()):
            with self.assertRaises(KeyError):
                i['nokey']

        for i in list(self.tb_tag.find(wrapper=True)):
            self.assertIsNone(i['nokey'])

    def test_update_one(self):
        with self.assertRaises(ValueError):
            self.tb_tag.update_one({}, {'hello': 0})

        self.tb_tag.update_one({}, {'$set': {'hellow': 0}})

    def test_update_many(self):
        with self.assertRaises(ValueError):
            self.tb_tag.update_many({}, {'hello': 0})

        self.tb_tag.update_many({}, {'$set': {'value': 1}})
        for i in list(self.tb_tag.find()):
            self.assertEqual(i['value'], 1)

    def test_delete_many(self):
        with self.assertRaises(Exception):
            self.tb_tag.delete_many({})

        for i in fake_ids:
            self.tb_tag.delete_many({'_id': i})
            self.assertIsNone(self.tb_tag.find_by_id(i))

    def test_find_by_id(self):
        self.assertEqual(self.tb_tag.find_by_id(
            fake_ids[0])['_id'], fake_ids[0])
        for index, i in enumerate(self.tb_tag.find_by_id(fake_ids[0:10])):
            self.assertEqual(i['_id'], fake_ids[index])

    def test_remove_by_id(self):
        for i in fake_ids[0:10]:
            self.tb_tag.remove_by_id(i)
            self.assertIsNone(self.tb_tag.find_by_id(i))

        result = self.tb_tag.remove_by_id(fake_ids[10:20])
        for i in fake_ids[10:20]:
            self.assertIsNone(self.tb_tag.find_by_id(i))
        self.assertEqual(result.deleted_count, 10)

    def test_get_as_dict(self):
        as_dict, as_list = self.tb_tag.get_as_dict(
            {'_id': {'$in': fake_ids[0:10]}})
        for index, i in enumerate(as_dict.keys()):
            self.assertIn(i, fake_ids[0:10])

        for i in as_list:
            self.assertIn(i['_id'], fake_ids[0:10])

    def test_to_objectid(self):
        self.assertTrue(self.tb_tag.to_objectid(None) is None)
        self.assertEqual(self.tb_tag.to_objectid('52c8fb6f1d41c820f1124350'),
                         ObjectId('52c8fb6f1d41c820f1124350'), 'to_objectid is fail')

    def test_create_model(self):
        self.assertEqual(self.tb_tag.create_model(
            'tag').find_one() is not None, True)

    def test_pymongo_collection_method(self):
        self.assertEqual(self.tb_tag.full_name, 'test.tag')

    def test_sub_collection(self):
        self.assertEqual(self.tb_tag.sub_collection(
            'test').full_name, 'test.tag.test')

    def test_inc(self):
        for index, i in enumerate(self.tb_tag.find_by_id(fake_ids[0:3])):
            self.assertEqual(i['value'], index)

        self.tb_tag.inc(
            {'_id': {'$in': fake_ids[0:3]}}, 'value', 1, multi=True)
        for index, i in enumerate(self.tb_tag.find_by_id(fake_ids[0:3])):
            self.assertEqual(i['value'], index + 1)

        self.tb_tag.inc({'_id': fake_ids[4]}, 'value', 1)
        self.assertEqual(self.tb_tag.find_by_id(fake_ids[4])['value'], 5)

    def test_to_str(self):
        one = self.tb_tag.to_str(self.tb_tag.find(limit=10))
        self.assertTrue(isinstance(json.dumps(one), basestring))

    def test_to_one_str(self):
        one = self.tb_tag.to_one_str(self.tb_tag.find_one())
        self.assertTrue(isinstance(json.dumps(one), basestring))

    def test_write_action_call(self):
        def func(se, name, *args, **kwargs):
            self.assertEqual(name, 'save')

        def func2(se, name, *args, **kwargs):
            self.assertEqual(name, 'find')

        self.tb_tag.save({'value': 0})
        self.tb_tag.find()

    def test_default_encode(self):
        self.assertTrue(isinstance(
            self.tb_tag.default_encode(ObjectId()), basestring))
        self.assertTrue(isinstance(
            self.tb_tag.default_encode(datetime.datetime.now()), float))
        self.assertEqual(self.tb_tag.default_encode('string'), 'string')

    def test_put(self):
        value = 'hello word'
        s = StringIO()
        s.write(value)
        # put
        file_id = self.tb_tag.put(utf8(s.getvalue()))
        self.assertTrue(isinstance(file_id, ObjectId))

        # get
        one = self.tb_tag.get(file_id)
        self.assertTrue(getattr(one, 'read', False), 'test get fail')
        self.assertEqual(one.read(), utf8(value))

    def test_create(self):
        _id = self.tb_tag.create({'value': 0})
        self.assertIsNot(_id, None)
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

        result = self.tb_tag.create(record)
        self.assertIsInstance(result, ObjectId)

        # create one
        _id = self.tb_tag.create({'_id': fake_ids_2[0]})
        self.assertEqual(_id, fake_ids_2[0])
        result = self.tb_tag.find_by_id(fake_ids_2[0])
        self.assertEqual(result['value'], 0)

        # create not field
        with self.assertRaises(Exception):
            result = self.tb_tag.create({'nokey': 10})

        # check
        _id = self.tb_tag.create({'imgid': None})
        self.assertIsNot(_id, None)
        result = self.tb_tag.find_by_id(_id)
        self.assertEqual(result['value'], 0)
        self.tb_tag.remove_by_id(_id)

        docs = [{'_id': i} for i in fake_ids_2[1:]]
        result = self.tb_tag.create(docs)
        self.assertEqual(1, len(result))
        for i in result:
            self.assertIn(i, fake_ids_2)
        result = self.tb_tag.find_by_id(fake_ids_2[1:])
        self.assertEqual(1, len(result))
        for i in result:
            self.assertEqual(i['value'], 0)

    def log(self, one):
        print(one)


if __name__ == '__main__':
    unittest.main()
