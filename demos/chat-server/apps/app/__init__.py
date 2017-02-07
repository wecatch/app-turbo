
from turbo import register

from . import app


register.register_group_urls('', [
    (r"/", app.MainHandler),
    (r"/a/message/new", app.MessageNewHandler),
    (r"/a/message/updates", app.MessageUpdatesHandler),
])
