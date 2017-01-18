# -*- coding:utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    with_statement
)
import sys
import os

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.util import unittest  # noqa E402


def main():
    testSuite = unittest.TestSuite()
    suite = unittest.TestLoader().discover('tests', pattern='*_test.py')
    testSuite.addTest(suite)

    return testSuite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(main())
