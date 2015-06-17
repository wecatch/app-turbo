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
        #self.set_cookie('v', 's')
        #self.set_cookie('session_id', 'f8ffc9a62c64c98f369eff0d61b5bfe6c4fb7b2e')
        print(self.request.headers)
        print(self._new_cookie)

        self.write('get')

    def post(self):
        self.session.uid = '7787'
        self.write('post')

    def put(self):
        assert self.session.uid == '7787'
        self.write('put')


def run_server():
    register.register_url('/', HomeHandler)
    app.start()


class SessionTest(unittest.TestCase):

    def setUp(self):
        server = multiprocessing.Process(target=run_server)
        server.start()
        self.home_url = 'http://localhost:8888'
        self.pid = server.pid
        time.sleep(1)

    def tearDown(self):
        os.kill(self.pid, signal.SIGKILL)
        
    def test_session(self):
        resp = requests.get(self.home_url, headers={'refer':'http://127.0.0.1:8888'})
        self.assertEqual(resp.status_code, 200)
        print(resp.cookies)

        resp = requests.post(self.home_url)
        self.assertEqual(resp.status_code, 200)

        resp = requests.put(self.home_url)
        self.assertEqual(resp.status_code, 200)

if __name__ == '__main__':
    unittest.main()
