from __future__ import absolute_import, division, print_function, with_statement

import time
import os
import socket
import multiprocessing
import signal
import shutil
import tempfile
import logging


import requests

from turbo.test.util import unittest
from turbo import app
from turbo.conf import app_config
from turbo import register
from turbo.template import turbo_jinja2

sess = requests.session()
sess.keep_alive = False

app_config.app_name = 'app_test'
app_config.app_setting['template'] = 'jinja2'
tmp_source = tempfile.mkdtemp()
TEMPLATE_PATH  = os.path.join(tmp_source, "templates")
app_config.web_application_setting = {
    'xsrf_cookies': False,
    'cookie_secret': 'adasfd',
    'template_path': TEMPLATE_PATH,
    'debug': True,
}

#logger = logging.getLogger()


class HomeHandler(app.BaseHandler):

    def get(self):
        self.render('index.html')

    @turbo_jinja2
    def render_string(self, *args, **kwargs):
        pass


PID = None
URL = None


def run_server(port):
    register.register_url('/', HomeHandler)
    register.register_url('', HomeHandler)
    app.start(port)


def is_used(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('localhost', port)) == 0:
        return True

    return False


def setUpModule():
    port = 10000
    while True:
        if not is_used(port):
            break
        port += 1
            
    server = multiprocessing.Process(target=run_server, args=(port,))
    server.start()
    global PID, URL
    URL = 'http://localhost:%s'%port
    PID = server.pid


def tearDownModule():
    os.kill(PID, signal.SIGKILL)


HTML = """{{'abcdefg' | upper}}"""

class AppTest(unittest.TestCase):

    def setUp(self):
        global URL 
        self.home_url = URL
        try:
            shutil.rmtree(TEMPLATE_PATH)
        except Exception, e:
            pass
        os.makedirs(TEMPLATE_PATH)
        with open(os.path.join(TEMPLATE_PATH, 'index.html'), 'w') as f:
            f.write(HTML)

    def test_get(self):
        time.sleep(3)
        resp = sess.get(self.home_url)
        self.assertEqual(resp.text.strip().isupper(), True)

    def tearDown(self):
        try:
            shutil.rmtree(TEMPLATE_PATH)
        except Exception, e:
            pass
        finally:
            os.removedirs(tmp_source)


if __name__ == '__main__':
    unittest.main()
