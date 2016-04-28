#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

from datetime import datetime
import copy
import time
import logging


from bson.objectid import ObjectId

from turbo.util import escape as es, camel_to_underscore
from turbo.test.util import unittest

class EscapeTest(unittest.TestCase):

    def setUp(self):
        child = {
                'id': ObjectId(), 
                'atime':datetime.now(), 
                'number': 10 , 
                'name':'hello world', 
                'mail':None,
            }
        self.record = {
                'id': ObjectId(), 
                'atime':datetime.now(), 
                'number': 10 , 
                'name':'hello world',
                'child': child, 
                'childs': [copy.deepcopy(child) for i in xrange(3)], 
            }

        self.values = [copy.deepcopy(self.record) for i in xrange(3)]

    def tearDown(self):
        del self.record
        del self.values

    def test_to_dict_str(self):
        self.check_value_type(es.to_dict_str(self.record))
    
    def test_default_encode(self):
        now = datetime.now()
        objid = ObjectId()
        number = 10
        self.assertEqual(es.default_encode(now), time.mktime(now.timetuple()))
        self.assertEqual(es.default_encode(objid), unicode(objid))
        self.assertEqual(es.default_encode(number), number)
    
    def test_recursive_to_str(self):
        now = datetime.now()
        objid = ObjectId()
        number = 10
        self.check_value_type(es.to_str(self.record))
        self.check_value_type(es.to_str(self.values))
        self.check_value_type(es.to_str(now))
        self.check_value_type(es.to_str(objid))
        self.check_value_type(es.to_str(number))
    
    def test_no_attribute(self):
        with self.assertRaises(AttributeError):
            es.create_objectid()

    def test_tobjectid(self):
        es.to_int('s')

    def test_json_encode(self):
        self.assertTrue(es.json_encode(es.to_str(self.values), indent=4) is not None)
    
    def test_json_decode(self):
        self.assertTrue(type(es.json_decode(
            es.json_encode(es.to_str(self.values), indent=4)
            )).__name__ == 'list'
        )
        
        #error test
        self.assertTrue(type(es.json_decode(
            es.json_encode(es.to_str(self.values), invlaid=4)
            )).__name__ == 'NoneType'
        )   


    def test_to_list_str(self):
        [self.check_value_type(v)  for v in es.to_list_str(self.values)]
    
    def test_camel_to_underscore(self):
        self.assertEqual(camel_to_underscore('HelloWorld'), 'hello_world')

    def check_value_type(self, v):
        if isinstance(v, list):
            [self.check_value_type(v1) for v1 in v]
            return

        if isinstance(v, dict):
            [self.check_value_type(v1) for k1, v1 in v.items()]
            return 

        self.assertTrue(self.check_base_value_type(v))

    def log(self, msg):
        logging.info(msg) 

    def check_base_value_type(self, v):
        return isinstance(v, int) or isinstance(v, float)  or isinstance(v, basestring) or v is None

if __name__ == '__main__':
    unittest.main()
