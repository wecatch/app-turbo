from __future__ import absolute_import, division, print_function, with_statement

import unittest

from turbo.flux import Mutation, register, dispatch, register_dispatch

mutation = Mutation('flux_test')

@register(mutation)
def inc_rank(rank):
    return rank+1


@register(mutation)
def dec_rank(rank):
    return rank-1


@register_dispatch('flux_test', 'inc_rank')
def increment(rank):
    pass

def decrease(rank):
    return dispatch('flux_test', 'dec_rank', rank)


class FluxTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_increment(self):
        self.assertEqual(increment(10), 11)

    def test_decrease(self):
        self.assertEqual(decrease(10), 9)

if __name__ == '__main__':
    unittest.main()

