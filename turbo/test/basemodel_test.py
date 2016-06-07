#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement


import os
import sys
import datetime
import json
import StringIO
import inspect


from turbo.model import BaseModel
from turbo.test.util import unittest
from bson.objectid import ObjectId

from pymongo import MongoClient
import gridfs

mc = MongoClient()


class Tag(BaseModel):

    name = 'tag'
    field = {
        'list':     (list, []),
        'imgid':    (ObjectId, None),
        'uid':      (ObjectId, None),
        'name':     (basestring, None),
        'value':    (int, 0),
        'atime':    (datetime.datetime, None),
        'up':       (dict, {}),
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

    def tearDown(self):
        del self.m 

    def test_insert(self):
        _id = self.m.insert({'value': 0})
        self.assertIsNot(_id, None)

    def test_write_action_call(self):
        def func(se, name, *args, **kwargs):
            self.assertEqual(name, 'save')

        def func2(se, name, *args, **kwargs):
            self.assertEqual(name, 'find')

        self.m.save({'value': 0})
        self.m.find()

    def test_save(self):
        _id = self.m.insert({'value': 0})
        self.assertIsNot(_id, None)

    def test_find_one(self):
        _id = self.m.insert({'value': 0})
        self.assertIsNot(self.m.find_one(), None)

    def test_find(self):
        self.assertGreater(list(self.m.find()), 0)

    def test_update(self):
        with self.assertRaises(ValueError):
            self.m.update({},{'hello': 0}) 
        
        self.m.update({},{'$set':{'hellow': 0}})

        with self.assertRaises(ValueError):
            self.m.update({},{})

    def test_remove(self):
        with self.assertRaises(Exception):
            self.m.remove({})

    def test_find_one_wrapper(self):
        # test find_one wrapper=True
        self.assertTrue(self.m.find_one(wrapper=True)['rd'] is None)
        
        # test find_one default wrapper=False
        with self.assertRaises(KeyError):
            self.m.find_one(wrapper=False)['rd']
        
        # test find_one wrapper= True and return None
        self.assertTrue(self.m.find_one({'_id':ObjectId()}, wrapper=True) is None)

    def test_find_wrapper(self):
        # test find wrapper=True return generator 
        one = self.m.find_one()
        with self.assertRaises(KeyError):
            one['keyerror']
        
        one = self.m.find_one(wrapper=True)
        self.assertEqual(one['keyerror'], None)
        
        for one in self.m.find(limit=5):
            with self.assertRaises(KeyError):
                one['keyerror']

        for one in self.m.find(limit=5, wrapper=True):
            self.assertEqual(one['keyerror'], None)

    def test_put(self):
        value = 'hello word'
        s = StringIO.StringIO()
        s.write(value)

        # put
        file_id = self.m.put(s.getvalue())
        self.assertTrue(isinstance(file_id, ObjectId))
        
        # get
        one = self.m.get(file_id)
        self.assertTrue(getattr(one,'read',False),'test get fail')
        self.assertEqual(one.read(),value)

    def test_delete(self):
        pass

    def test_find_by_id(self):
        pass

    def test_get_as_column(self):
        pass

    def test_get_as_dict(self):
        pass

    def test_to_objectid(self):
        self.assertTrue(self.m.to_objectid(None) is None)
        self.assertEqual(self.m.to_objectid('52c8fb6f1d41c820f1124350'), 
            ObjectId('52c8fb6f1d41c820f1124350'),'to_objectid is fail')

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
                {'key': ObjectId(),'key2': 'test','key3': ObjectId()},
                10,
                12,
                13,
                ['name', 'name', 'name', ObjectId(), ObjectId()],
                datetime.datetime.now(),
            ],
            'imgid':ObjectId(),
            'up':{
                'key1': ObjectId(),
                'key2': ObjectId(),
                'key3': ObjectId(),
            }
        }
        
        result = self.m.create(record)
        self.assertTrue(isinstance(result, ObjectId))

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

    def test_default_encode(self):
        self.assertTrue(isinstance(self.m.default_encode(ObjectId()), basestring))
        self.assertTrue(isinstance(self.m.default_encode(datetime.datetime.now()),float))
        self.assertEqual(self.m.default_encode('string'), 'string')
    
    def test_get_as_dict(self):
        pass

    def log(self, one):
        print(one)

if __name__ == '__main__':
    unittest.main()
