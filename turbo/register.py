from collections import namedtuple

Handler2url = namedtuple('Handler2url', 'prefix urls')

def regisger_app():
    pass

def register_url(prefix, urls):
    return Handler2url(prefix, urls)