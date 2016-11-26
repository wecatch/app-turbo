# -*- coding:utf-8 -*-
from turbo import register

import api
import app

register.register_group_urls('', [
    ('/', app.HomeHandler),
    ('/plus', app.IncHandler),
    ('/minus', app.MinusHandler),
])

register.register_group_urls('/v1', [
    ('', api.HomeHandler),
])
