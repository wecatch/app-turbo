#-*- coding:utf-8 -*-

from turbo.test.util import unittest

from turbo.util import import_object

TEST_MODULES = [
    'escape_test',
    'basemodel_test',
    'log_test',
    'httputil_test',
    'app_test',
]


def main():
    testSuite = unittest.TestSuite()
    for module in TEST_MODULES:
        suite = unittest.TestLoader().loadTestsFromName(module)
        testSuite.addTest(suite)

    result = unittest.TestResult()
    testSuite.run(result)
    print result


if __name__ == '__main__':
    main()