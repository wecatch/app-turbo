# -*- coding:utf-8 -*-

from turbo.flux import Mutation, dispatch, register, register_dispatch

from . import mutation_types


@register_dispatch('user', mutation_types.INCREASE)
def increase(rank):
    pass


def decrease(rank):
    return dispatch('user', mutation_types.DECREASE, rank)
