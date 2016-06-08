from turbo.flux import Mutation, register, State

mutation = Mutation(__file__)
state = State(__file__)

state.qps = 0

@register(mutation)
def inc_qps():
    state.qps += 1