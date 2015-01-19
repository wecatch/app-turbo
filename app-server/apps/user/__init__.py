
from turbo import register

import app


register.register_group_urls('', [
    ('/', app.HomeHandler),
    ('/index', app.HomeHandler, 'index'),
    ('/home', app.HomeHandler, 'home'),
])

register.register_url('/v1/api', app.ApiHandler)
