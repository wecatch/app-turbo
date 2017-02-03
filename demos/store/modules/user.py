from turbo.flux import Mutation, register, State

mutation = Mutation(__file__)
state = State(__file__)


@register(mutation)
def increase_rank(rank):
    return rank + 1


@register(mutation)
def dec_rank(rank):
    return rank - 1
