from __future__ import absolute_import, division, print_function, with_statement

import os
import signal
import sys
import unittest
import random
import time
import threading
import logging
import requests
import multiprocessing

from turbo import app
from turbo.conf import app_config
from turbo import register

app_config.app_name = 'app_test'
app_config.web_application_setting = {}

logger = logging.getLogger()

print(logger.level)


class HomeHandler(app.BaseBaseHandler):

    def get(self):
        logger.info('get')


def run_server():
    register.register_url('/', HomeHandler)
    app.start()


class AppTest(unittest.TestCase):

    def setUp(self):
        server = multiprocessing.Process(target=run_server)
        server.start()
        self.localhost = 'http://localhost:8888'
        self.pid = server.pid
        logger.warning(self.pid)

    def tearDown(self):
        os.kill(self.pid, signal.SIGKILL)

    def test_get(self):
        resp = requests.get(self.localhost)
        logger.warning(resp.status_code)


if __name__ == '__main__':
    unittest.main()