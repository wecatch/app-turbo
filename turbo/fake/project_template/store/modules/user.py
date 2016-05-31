from turbo.flux import Mutation, register

mutation = Mutation(__file__)

@register(mutation)
def increase_rank(rank):
    return rank+1


@register(mutation)
def decrease_rank(rank):
    return rank-1