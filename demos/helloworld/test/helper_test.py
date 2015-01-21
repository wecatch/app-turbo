#-*- coding:utf-8 -*-

import unittest

import realpath

from helpers import user as wallpaper 

import helpers

import helpers.user as db_wallpaper

class HelperTest(unittest.TestCase):

    def test_model(self):
        self.assertTrue(callable(wallpaper['user'].find_one))
    
    def test_import_helper(self):
        self.assertTrue(callable(helpers.user['user'].find_one))
    
    def test_import_helper_two(self):
        self.assertTrue(callable(db_wallpaper['user'].find_one))

if __name__ == '__main__':
    unittest.main()
