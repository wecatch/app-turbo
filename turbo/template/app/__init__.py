
from turbo import register

import app


register.register_group_urls('', [
	('/', app.HomeHandler, 'home'),
	('/index', app.HomeHandler, 'index'),
])

register.register_url('/v1/api', app.ApiHandler)
