# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import datetime
import json
from copy import deepcopy

from bson.objectid import ObjectId
from turbo.util import escape,  basestring_type

from util import unittest


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

        self.assertTrue(isinstance(json.dumps(escape.to_str(
            [deepcopy(data) for i in range(10)])), basestring_type))
        self.assertTrue(isinstance(json.dumps(
            escape.to_str(deepcopy(data))), basestring_type))

    def test_to_str_encode(self):
        data = {
            'v1': 10,
            'v2': datetime.datetime.now(),
            'v3': ObjectId(),
            'v4': 'value',
        }

        v = escape.to_str(data)

        self.assertTrue(isinstance(v['v1'], int))
        self.assertTrue(isinstance(v['v2'], float))
        self.assertTrue(isinstance(v['v3'], basestring_type))
        self.assertTrue(isinstance(v['v4'], basestring_type))

        def encode(v):
            return str(v)

        v = escape.to_str(data, encode)
        self.assertTrue(isinstance(v['v1'], basestring_type))
        self.assertTrue(isinstance(v['v2'], basestring_type))
        self.assertTrue(isinstance(v['v3'], basestring_type))
        self.assertTrue(isinstance(v['v4'], basestring_type))


if __name__ == '__main__':
    unittest.main()
