#-*- coding:utf-8 -*-

import os
import sys
import unittest
import random
import time
import threading

from turbo.cache import object_cache


DATA = 'abcdfg'

THREAD_COUNT = 0

def load_data(value=None):
    while True:
        new_value = random.choice(DATA)
        if new_value != value:
            break

    return new_value

def log(msg):
    print msg

class ObjectCacheTestThread(threading.Thread):

    def __init__(self, oc, key, value, expire=5):
        super(ObjectCacheTestThread, self).__init__()
        self.oc = oc
        self.key = key
        self.expire = expire

    def run(self):
        start = time.time()
        while time.time() - start < self.expire:
            self.oc.get(self.key)

def object_cache_target(key, value):
    return object_cache.ObjectCache.get(key) == value

def trace_object_cache_run(func, key, value):
    global THREAD_COUNT
    if func(key ,value):
        THREAD_COUNT += 1

class ObjectCacheTest(unittest.TestCase):

    def setUp(self):
        self.oc = object_cache.ObjectCache()

    def tearDown(self):
        del self.oc

    def test_create(self):
        log('test create')
        key = self.oc.create(load_data, expire=30)
        self.assertTrue(key is not None)
        log('the key is {}'.format(key))
        log('test create end')
    
    def test_given_name(self):
        log('test given name')
        key = self.oc.create(load_data, 'cache_key', expire=30)
        self.assertTrue(key == 'cache_key')
        log('the key is {}'.format(key))
        log('test create end')
    
    def test_invalid_name(self):
        log('test invalid given name')
        with self.assertRaises(TypeError):
            key = self.oc.create(load_data, {'s': 10}, expire=30)
            self.assertEqual(key, None)

    def test_get(self):
        key = self.oc.create(load_data, expire=30)
        self.assertTrue(self.oc.get(key) in DATA)

    def test_expire(self):
        '''
        create object cache, wait until the value is expired
        make sure the new value is different to old value
        '''
        log('test expire start')
        expire = 5
        start = time.time()
        key = self.oc.create(load_data, expire=expire)
        old_value = self.oc.get(key)
        while time.time() - start < expire :
            log('{} in life period, the value is {}'.format(key,self.oc.get(key)))
            self.assertEqual(self.oc.get(key), old_value)
            time.sleep(1)

        log('{} is expired now'.format(key))

        self.assertTrue(self.oc.get(key, old_value) in DATA)
        self.assertTrue(self.oc.get(key) != old_value)
        
        log('{} new value is {}'.format(key, self.oc.get(key)))
        log('test expire end')

    def test_multi_thread(self):
        log('test multi thread start')
        key = self.oc.create(load_data)
        value = self.oc.get(key)
        threads_number = 3
        thread_list = []
        for i in range(threads_number):
            i = threading.Thread(target=trace_object_cache_run, args=(object_cache_target, key, value))
            thread_list.append(i)
            i.start()

        for i in thread_list:
            i.join()

        self.assertEqual(threads_number, THREAD_COUNT)

        log('test multi thread end')


if __name__ == '__main__':
    unittest.main()
