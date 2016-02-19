#-*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement


from turbo.test.util import unittest

from turbo.util import import_object

TEST_MODULES = [
    'escape_test',
    'basemodel_test',
    'log_test',
    'httputil_test',
    'app_test',
    'session_test',
    'util_test',
]


def main():
    testSuite = unittest.TestSuite()
    for module in TEST_MODULES:
        suite = unittest.TestLoader().loadTestsFromName(module)
        testSuite.addTest(suite)

    return testSuite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(main())
