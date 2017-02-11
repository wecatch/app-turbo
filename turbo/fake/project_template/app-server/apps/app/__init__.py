# -*- coding:utf-8 -*-
from turbo import register

from . import api
from . import app

register.register_group_urls('', [
    ('/', app.HomeHandler),
    ('/plus', app.IncHandler),
    ('/minus', app.MinusHandler),
])

register.register_group_urls('/v1', [
    ('', api.HomeHandler),
])
