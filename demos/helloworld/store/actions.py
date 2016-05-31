from turbo.flux import Mutation, register, dispatch, register_dispatch

import mutation_types

@register_dispatch('user', mutation_types.INCREMENT)
def increment(uid, rank):
    pass


def decrease(uid, rank):
    return dispatch('user', mutation_types.DECREASE, uid, rank)