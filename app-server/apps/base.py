# -*- coding:utf-8 -*-


import tornado.web
import tornado.escape

from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId

from settings import (
    CDN as _CDN,
    LANG as _LANG,
)
from utils import (
    escape as _es,
    httputil as _ht,
)
from core.exceptions import ResponseError
from conf import locale, global_setting

import loggers
logger = loggers.getLogger(__file__)

class BaseBaseHandler(tornado.web.RequestHandler):
    '''
    request parameter:
        _get_params = {
                'need':[
                    ('skip', int), 
                    ('limit', int), 
                ],
                'option':[
                    ('jsoncallback', basestring, None),
                ]
            }

    '''

    _required_params = [('jsoncallback', basestring, None), ('skip', int, 0), ('limit', int, 0)]
    _types = [ObjectId, None, basestring, int, float, list, file]
    _params = None
    _data = None

    context = None
    template_path = None

    def initialize(self):
        self.context = self.get_context()
        self.template_path = ''

    def render(self, template_name, **kwargs):
        super(BaseBaseHandler, self).render(('%s%s') % (self.template_path, template_name),
                                            context=self.context, **kwargs)

    def sort_by(self, sort):
        return {1: ASCENDING, -1: DESCENDING}.get(sort, ASCENDING)

    # request context
    def get_context(self):
        return {

        }

    def static_url(self, path, include_host=None, v=None, **kwargs):
        is_debug = self.application.settings.get('debug', False)
        
        # In debug mode, load static files from localhost
        if is_debug or not (is_debug ^ _CDN['is']):
            return super(BaseBaseHandler, self).static_url(path, include_host, **kwargs)

        v = kwargs.get('v', '')

        return ('{host}/{path}?v={v}' if v else '{host}/{path}').format(host=_CDN['host'], path=path, v=v)

    @staticmethod
    def to_objectid(objid):
        return _es.to_objectid(objid)

    @staticmethod
    def to_int(value):
        return _es.to_int(value)

    @staticmethod
    def to_float(value):
        return _es.to_float(value)

    @staticmethod
    def utf8(v):
        return tornado.escape.utf8(v)

    @staticmethod
    def encode_http_params(**kw):
        return _ht.encode_http_params(**kw)

    @staticmethod
    def json_encode(data):
        return _es.json_encode(data)

    @staticmethod
    def json_decode(data):
        return _es.json_decode(data)

    @staticmethod
    def recur_to_str(v):
        return _es.recursive_to_str(v)

    def wo_json(self, data):
        callback = self.get_argument('jsoncallback', None)
        if callback:
            return self.write('%s(%s)' % (callback, self.json_encode(data)))

        self.write(self.json_encode(data))

    def ri_json(self, data):
        return self.json_decode(data)

    @property
    def parameter(self):
        '''
        according to request method config to filter all request paremter
        if value is invalid then set None
        '''
        method = self.request.method.lower()
        arguments = self.request.arguments
        files = self.request.files

        params = getattr(self, '_%s_params' % method, None)
        if params is None:
            return {}

        rpd = {}  # request parameter dict

        def filter_parameter(key, tp, default=None):
            if tp not in self._types:
                raise ValueError("%s parameter expected types %s" % (key, self._types))

            if tp != file:
                if key not in arguments:
                    rpd[key] = default
                    return

                if tp in [ObjectId, int, float]:
                    rpd[key] = getattr(self, 'to_%s' % getattr(tp, '__name__').lower())(self.get_argument(key))
                    return

                if tp == basestring:
                    rpd[key] = self.get_argument(key, strip=False)
                    return

                if tp == list:
                    rpd[key] = self.get_arguments(key)
                    return

            if tp == file:
                if key not in files:
                    rpd[key] = default
                    return

                rpd[key] = self.request.files[key]

        for key, tp in params.get('need', []):
            if tp == list:
                filter_parameter(key, tp, [])
            else:
                filter_parameter(key, tp)

        for option_params in [params.get('option', []), self._required_params]:
            for key, tp, default in option_params:
                filter_parameter(key, tp, default)

        return rpd

    def http_error(self, status_code=404, **kwargs):
        raise tornado.web.HTTPError(status_code)


class BaseHandler(BaseBaseHandler):

    MAX_COUNT = 50

    def get_context(self):
        context = super(BaseHandler, self).get_context()
        context.update({

        })

        return context

    def get(self, *args, **kwargs):
        try:
            self.GET(*args, **kwargs)
        except ResponseError as e:
            e.msg = locale.LANG_MESSAGE[_LANG].get(e.code)
            resp = self.init_resp(e.code, e.msg)
        except Exception as e:
            logger.exception(e)
            resp = self.init_resp(1)
        else:
            resp = self.init_resp()

        self.wo_resp(resp)

    def post(self, *args, **kwargs):
        try:
            self.POST(*args, **kwargs)
        except ResponseError as e:
            e.msg = locale.LANG_MESSAGE[_LANG].get(e.code)
            resp = self.init_resp(e.code, e.msg)
        except Exception as e:
            logger.exception(e)
            resp = self.init_resp(1)
        else:
            resp = self.init_resp()

        self.wo_resp(resp)

    def POST(self, *args, **kwargs):
        pass

    def GET(self, *args, **kwargs):
        pass

    def wo_resp(self, resp):
        if resp['code'] != 0:
            return self.wo_json(resp)

        if isinstance(self._data, dict):
            resp['data'].update(self._data)

        return self.wo_json(resp)

    def get_current_user(self):
        return {
            'uid': self.to_objectid('53dc9f72c4e1fd6d1d9b1585'),
            'nickname': u'三月沙',
            'from': 'qq',
        }

    @staticmethod
    def init_resp(code=0):
        resp = {
            'code': code,
            'msg': locale.LANG_MESSAGE[_LANG].get(code),
            'data': {},
        }

        return resp

    def check_xsrf_cookie(self):
        pass

