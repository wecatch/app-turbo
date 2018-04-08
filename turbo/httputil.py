from __future__ import absolute_import, division, print_function, with_statement

from turbo.util import basestring_type, unicode_type, PY3, to_basestring

if PY3:
    from urllib.parse import quote
else:
    from urllib import quote


def is_empty(v):
    if isinstance(v, basestring_type):
        if not v:
            return True
    if v is None:
        return True

    return False


def utf8(v):
    return v.encode('utf-8') if isinstance(v, unicode_type) else str(v)


def encode_http_params(**kw):
    '''
    url paremeter encode
    '''
    try:
        _fo = lambda k, v: '{name}={value}'.format(
            name=k, value=to_basestring(quote(v)))
    except:
        _fo = lambda k, v: '%s=%s' % (k, to_basestring(quote(v)))

    _en = utf8

    return '&'.join([_fo(k, _en(v)) for k, v in kw.items() if not is_empty(v)])
