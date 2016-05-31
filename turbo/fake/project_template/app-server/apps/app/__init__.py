
from turbo import register

import app, api


register.register_group_urls('', [
    ('/', app.HomeHandler),
    ('/plus', app.IncHandler),
    ('/minus', app.MinusHandler),
])

register.register_group_urls('/v1', [
    ('', api.HomeHandler),
])
