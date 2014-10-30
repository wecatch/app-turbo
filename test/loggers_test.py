#-*- coding:utf-8 -*-

import os
import sys
import unittest
import random
import time
import threading

import realpath

import loggers

logger = loggers.getLogger(__file__)

class GetLoggerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_logger(self):
        self.assertEqual(logger.name, 'root.test.loggers_test')


if __name__ == '__main__':
    unittest.main()
