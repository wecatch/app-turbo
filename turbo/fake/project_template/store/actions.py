from turbo.flux import Mutation, register, dispatch, register_dispatch

import mutation_types

@register_dispatch('user', mutation_types.INCREASE)
def increase(rank):
    pass


def decrease(rank):
    return dispatch('user', mutation_types.DECREASE, rank)