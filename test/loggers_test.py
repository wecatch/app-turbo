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
currpath = os.path.abspath(__file__)

class GetLoggerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_logger(self):
        self.assertEqual(logger.name, 'test.loggers_test')
        logger_one = loggers.getLogger('logger.one')
        self.assertEqual(logger_one.name, 'logger.one')
        logger_two = loggers.getLogger('logger.two', 'loggers_test.log')
        self.assertEqual(logger_two.name, 'logger.two')
        self.assertEqual(len(logger_two.handlers), 2)
        logger_two.info('hello world')

if __name__ == '__main__':
    unittest.main()
