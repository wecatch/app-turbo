#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement


import os
import sys
import datetime
import json
import StringIO
import inspect
from copy import deepcopy


from turbo.model import BaseModel
from turbo.test.util import unittest
from turbo.util import escape
from bson.objectid import ObjectId


class EscapeTest(unittest.TestCase):


    def test_inc(self):
        pass

    def test_to_str(self):
        data = {
            'v1': 10,
            'v2': datetime.datetime.now(),
            'v3': ObjectId(),
            'v4': 'value',
        }
        
        self.assertTrue(isinstance(json.dumps(escape.to_str([deepcopy(data) for i in range(10)])), basestring))
        self.assertTrue(isinstance(json.dumps(escape.to_str(deepcopy(data))), basestring))


if __name__ == '__main__':
    unittest.main()
