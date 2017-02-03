#-*- coding:utf-8 -*-

import os
import sys
import unittest
import datetime
import json
import StringIO

import realpath

from models.user import model
from bson.objectid import ObjectId


class AdeskModelTest(unittest.TestCase):

    def setUp(self):
        self.m = model.User()

    def tearDown(self):
        del self.m

    def test_create(self):
        self.assertTrue(isinstance(self.m.create(
            {'email': 'test@test.com'}), ObjectId))

    def test_insert(self):
        pass

    def test_save(self):
        pass

    def test_find_one(self):
        pass

    def test_find(self):
        pass

    def test_update(self):
        pass

    def test_remove(self):
        pass

if __name__ == '__main__':
    unittest.main()
