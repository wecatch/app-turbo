
from turbo import register

import app


register.register_group_urls('', [
    ('/', app.HomeHandler),
    ('/index', app.HomeHandler, 'index'),
    ('/hello', app.HomeHandler, 'home'),
    ('/motor', app.AsynHandler),
])

register.register_url('/v1/hello', app.ApiHandler)
