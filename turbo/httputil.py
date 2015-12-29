from __future__ import absolute_import, division, print_function, with_statement

try:
    basestring
except Exception as e:
    basestring = str

import urllib


def is_empty(v):
    if isinstance(v, basestring):
        if not v:
            return True
    if v is None:
        return True

    return False


def utf8(v):
    return v.encode('utf-8') if isinstance(v, unicode) else str(v)


def encode_http_params(**kw):
    '''
    url paremeter encode
    '''
    try:
        _fo = lambda k, v: '{name}={value}'.format(name=k, value=urllib.quote(v),)
    except:
        _fo = lambda k, v: '%s=%s' % (k,urllib.quote(v))

    _en = utf8 

    return '&'.join([_fo(_en(k), _en(v)) for k, v in kw.items() if not is_empty(v)])
