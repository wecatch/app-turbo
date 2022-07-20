from __future__ import absolute_import, division, print_function, with_statement

import multiprocessing
import os
import signal

from bson.objectid import ObjectId
import requests
from turbo import app
from turbo import register
from turbo.conf import app_config
from turbo.util import (
    basestring_type as basestring,
    file_types
)

from util import unittest, port_is_used, get_free_tcp_port

app_config.app_name = 'app_test'
app_config.web_application_setting = {
    'xsrf_cookies': False,
    'cookie_secret': 'adasfd'
}


class HomeHandler(app.BaseHandler):

    def get(self):
        assert not self.is_ajax()
        self.write('get')

    def post(self):
        self.write('post')

    def put(self):
        self.write('put')


class ApiHandler(app.BaseHandler):
    _get_required_params = [
        ('skip', int, 0),
        ('limit', int, 20),
    ]

    _get_params = {
        'need': [
            ('action', None),
        ],
        'option': [
            ('who', basestring, 'python'),
            ('str_key', str, 'python'),
            ('bool', bool, False),
            ('int', int, 0),
            ('float', float, 0),
            ('objectid', ObjectId, None),
            ('list', list, []),
        ]
    }

    _post_required_params = [
        ('skip', int, 0),
        ('limit', int, 20),
    ]

    _post_params = {
        'need': [
            ('who', basestring),
            ('app_test', file_types)
        ],
    }

    def GET(self):
        self._params = self.parameter

        assert self._params['skip'] == 0
        assert self._params['limit'] == 20
        assert self._params['who'] == 'python'
        assert self._params['action'] is None
        assert self._params['list'] == []
        assert self._params['str_key'] == 'python'
        assert self.is_ajax()

        self._data = {
            'value': self._params['who']
        }

    def POST(self):
        self._params = self.parameter

        assert self._params['skip'] == 0
        assert self._params['limit'] == 10

        self._data = {
            'value': self._params['who'],
            'file_name': self._params['app_test'][0].filename
        }

    def PUT(self):
        self._data = {
            'api': {
                'put': 'value'
            }
        }

    def DELETE(self):
        raise Exception('value error')

    def wo_json(self, data):
        self.write(self.json_encode(data, indent=4))


PID = None
URL = None


def run_server(port):
    register.register_url('/', HomeHandler)
    register.register_url('', HomeHandler)
    register.register_url('/api', ApiHandler)
    app.start(port)


def setUpModule():
    port = get_free_tcp_port()
    server = multiprocessing.Process(target=run_server, args=(port,))
    server.start()
    global PID, URL
    URL = 'http://localhost:%s' % port
    PID = server.pid


def tearDownModule():
    os.kill(PID, signal.SIGKILL)


class AppTest(unittest.TestCase):

    def setUp(self):
        global URL
        self.home_url = URL
        self.api_url = URL + '/api'

    def test_get(self):
        resp = requests.get(self.home_url)
        self.assertEqual(resp.status_code, 200)

    def test_post(self):
        resp = requests.post(self.home_url)
        self.assertEqual(resp.status_code, 200)

    def test_get_api(self):
        resp = requests.get(self.api_url, headers={
            'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['res']['value'], 'python')

    def test_delete_api(self):
        resp = requests.delete(self.api_url, headers={
            'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['msg'], 'Unknown Error')

    def test_post_api(self):
        with open(os.path.abspath(__file__), 'rb') as file:
            resp = requests.post(self.api_url, headers={
                'X-Requested-With': 'XMLHttpRequest'},
                                 data={'limit': 10, 'who': 'ruby'}, files={'app_test': file})
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json()['res']['value'], 'ruby')
            self.assertEqual(resp.json()['res']['file_name'], 'app_test.py')

    def test_404(self):
        resp = requests.get(self.home_url + '/hello')
        self.assertTrue(resp.content.find(b'404') != -1)

    def test_context(self):
        """TODO test context
        """
        pass


if __name__ == '__main__':
    unittest.main()
