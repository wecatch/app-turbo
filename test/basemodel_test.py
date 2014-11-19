#-*- coding:utf-8 -*-

import os
import sys
import unittest
import datetime
import json
import StringIO

import realpath

from models.base import BaseModel
from bson.objectid import ObjectId

class Model(BaseModel):
    pass


class Tag(Model):

    name = 'tag'
    field = {
        'list':     (list, []),
        'imgid':    (ObjectId, None),
        'uid':      (ObjectId, None),
        'name':     (basestring, None),
        'atime':    (datetime.datetime, None),
        'up':       (dict, {}),
    }


class BaseModelTest(unittest.TestCase):

    def setUp(self):
        self.m = Tag()

    def tearDown(self):
        del self.m 

    def test_insert(self):
        pass

    def test_save(self):
        pass

    def test_find_one(self):
        pass

    def test_find(self):
        pass

    def test_update(self):
        with self.assertRaises(Exception):
            self.m.update({},{'hello': 0}) 
        
        self.m.update({},{'$set':{'hellow': 0}})

    def test_remove(self):
        pass

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
        l = self.m.find(limit=10, wrapper=True)
        for i in l:
            pass
        self.assertTrue(len(list(l)) == 0)
       
        # test find return default generator and if checker
        def test_if(s):
            if s:
                return True 
            return False

        self.assertTrue(test_if(self.m.find({'_id':'sd'}, limit=10, wrapper=True)))
        self.assertTrue(test_if(self.m.find({'_id':'sd'}, limit=10)))

        # test find wrapper=True 
        for i in self.m.find({}, skip=0, limit=3, wrapper=True):
            self.assertTrue(i['rd'] is None)

        # test find wrapper=True 
        for i in self.m.find({}, skip=0, limit=3, wrapper=False):
            with self.assertRaises(KeyError):
                i['rd']


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
        pass

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
        print one

if __name__ == '__main__':
    unittest.main()
