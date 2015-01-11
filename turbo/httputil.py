import urllib


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

    return '&'.join([_fo(_en(k), _en(v)) for k, v in kw.items() if v is not None])
