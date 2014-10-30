#-*- coding:utf-8 -*-

import unittest

import realpath

from helpers import food as wallpaper 

import helpers

import helpers.food as db_wallpaper

class HelperTest(unittest.TestCase):

    def test_model(self):
        self.assertTrue(callable(wallpaper['food'].find_one))
    
    def test_import_helper(self):
        self.assertTrue(callable(helpers.food['food'].find_one))
    
    def test_import_helper_two(self):
        self.assertTrue(callable(db_wallpaper['food'].find_one))

if __name__ == '__main__':
    unittest.main()
