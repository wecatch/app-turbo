from turbo.flux import Mutation, register

mutation = Mutation(__file__)

@register(mutation)
def inc_rank(uid, rank):
    return rank+1


@register(mutation)
def dec_rank(uid, rank):
    return rank-1
