#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import sys
import signal
import random
import time
import logging
import requests
import multiprocessing
import time
import os


from turbo import app
from turbo.conf import app_config
from turbo import register
from turbo.session import RedisStore

app_config.app_name = 'app_test'
app_config.web_application_setting = {
    'xsrf_cookies': False,
    'cookie_secret': 'asdf/asdfiw872*&^2/'
}

from turbo.test.util import unittest


class HomeHandler(app.BaseHandler):

    session_initializer = {
        'time': time.time(),
        'uid': None,
    }

    def get(self):
        assert self.session.uid is None
        assert self.session.session_id is not None
        self.write('get')

    def post(self):
        self.session.uid = '7787'
        self.write('post')

    def put(self):
        assert self.session.uid == '7787'
        self.write('put')


class RedisStoreHandler(app.BaseHandler):

    session_initializer = {
        'time': time.time(),
        'uid': None,
    }

    session_store = RedisStore(timeout=3600)

    def get(self):
        assert self.session.uid is None
        assert self.session.session_id is not None
        self.write('get')

    def post(self):
        self.session.uid = '7787'
        self.write('post')

    def put(self):
        assert self.session.uid == '7787'
        self.write('put')


def run_server():
    register.register_url('/', HomeHandler)
    register.register_url('/redis', RedisStoreHandler)
    app.start()


class SessionTest(unittest.TestCase):

    def setUp(self):
        server = multiprocessing.Process(target=run_server)
        server.start()
        self.home_url = 'http://localhost:8888'
        self.redis_url = 'http://localhost:8888/redis'
        self.pid = server.pid
        time.sleep(1)

    def tearDown(self):
        os.kill(self.pid, signal.SIGKILL)
        
    def test_session(self):
        resp = requests.get(self.home_url, headers={'refer':'http://127.0.0.1:8888'})
        self.assertEqual(resp.status_code, 200)
        cookies = resp.cookies
        resp = requests.post(self.home_url, cookies=cookies)
        self.assertEqual(resp.status_code, 200)

        resp = requests.put(self.home_url, cookies=cookies)
        self.assertEqual(resp.status_code, 200)

    def test_redis_store_session(self):
        resp = requests.get(self.redis_url, headers={'refer':'http://127.0.0.1:8888'})
        self.assertEqual(resp.status_code, 200)
        cookies = resp.cookies
        resp = requests.post(self.redis_url, cookies=cookies)
        self.assertEqual(resp.status_code, 200)

        resp = requests.put(self.redis_url, cookies=cookies)
        self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
