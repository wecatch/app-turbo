#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement


from turbo.test.util import unittest

from turbo.util import import_object

TEST_MODULES = [
    'turbo.test.escape_test',
    'turbo.test.basemodel_test',
    'turbo.test.log_test',
    'turbo.test.httputil_test',
    'turbo.test.app_test',
    'turbo.test.session_test',
    'turbo.test.util_test',
    'turbo.test.flux_test',
    'turbo.test.jinja2_test',
]


def main():
    testSuite = unittest.TestSuite()
    for module in TEST_MODULES:
        suite = unittest.TestLoader().loadTestsFromName(module)
        testSuite.addTest(suite)

    return testSuite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(main())
