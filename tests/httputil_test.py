# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import turbo.httputil as hu
from util import unittest


class HttpUtilTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_encode_http_params(self):
        keyword = '美女'
        paras = hu.encode_http_params(k=10, h=2, key='ass', keyword=keyword, empty='')
        print(paras)
        self.assertEqual(sorted(paras.split('&')), [
                        'h=2', 'k=10', 'key=ass', 'keyword=%s' % hu.quote(keyword)])


if __name__ == '__main__':
    unittest.main()
