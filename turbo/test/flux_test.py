from __future__ import absolute_import, division, print_function, with_statement

import unittest

from turbo.flux import Mutation, register, dispatch, register_dispatch, State

mutation = Mutation('flux_test')

@register(mutation)
def increase_rank(rank):
    return rank+1


@register(mutation)
def decrease_rank(rank):
    return rank-1


@register_dispatch('flux_test', 'increase_rank')
def increase(rank):
    pass

def decrease(rank):
    return dispatch('flux_test', 'decrease_rank', rank)

state = State()
state.count = 0

class FluxTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_state(self):
        state.count += 1
        self.assertEqual(state.count, 1)
        state.count += 1
        self.assertEqual(state.count, 2)

    def test_increment(self):
        self.assertEqual(increase(10), 11)

    def test_decrease(self):
        self.assertEqual(decrease(10), 9)

if __name__ == '__main__':
    unittest.main()
