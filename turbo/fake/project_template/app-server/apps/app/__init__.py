
from turbo import register

import app


register.register_group_urls('', [
    ('/', app.HomeHandler),
])
