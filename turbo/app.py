# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function

import os

import tornado.web
import tornado.httpserver
import tornado.escape
import tornado.ioloop
from tornado.options import define, options
from tornado.util import ObjectDict

from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId

from turbo.core.exceptions import ResponseError
from turbo.util import escape as _es
import turbo.httputil as _ht 
from turbo.log import app_log

from turbo.conf import app_config

class BaseBaseHandler(tornado.web.RequestHandler):
    """
    config request parameter like this:
    _get_params = {
            'need':[
                ('skip', int),
                ('limit', int),
            ],
            'option':[
                ('jsoncallback', basestring, None),
            ]
        }

    """

    #override in subclass
    _required_params = [('skip', int, 0), ('limit', int, 0)] 
    _types = [ObjectId, None, basestring, int, float, list, file, bool]
    _data = None

    def initialize(self):
        # request context
        self.context = self.get_context()

        # app template path if exist must end with slash like user/
        self.template_path = ''

    def render(self, template_name, **kwargs):
        super(BaseBaseHandler, self).render('%s%s' % (self.template_path, template_name), context=self.context, **kwargs)

    def sort_by(self, sort):
        return {1: ASCENDING, -1: DESCENDING}.get(sort, ASCENDING)

    # request context
    def get_context(self):
        return {

        }

    def to_objectid(self, objid):
        return _es.to_objectid(objid)

    def to_int(self, value):
        return _es.to_int(value)

    def to_float(self, value):
        return _es.to_float(value)

    def to_bool(self, value):
        return bool(value)

    def to_str(self, v):
        return _es.to_str(v)

    def utf8(self, v):
        return tornado.escape.utf8(v)

    def encode_http_params(self, **kw):
        """
        url parameter encode
        """
        return _ht.encode_http_params(**kw)

    def json_encode(self, data):
        return _es.json_encode(data)

    def json_decode(self, data):
        return _es.json_decode(data)

    # write output json
    def wo_json(self, data):
        callback = self.get_argument('jsoncallback', None)
        if callback:
            return self.write('%s(%s)' % (callback, self.json_encode(data)))

        self.write(self.json_encode(data))       

    # read in json
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

        rpd = {}  # request parameter dict

        def filter_parameter(key, tp, default=None):
            if tp not in self._types:
                raise ValueError("%s parameter expected types %s" % (key, self._types))

            if tp != file:
                if key not in arguments:
                    rpd[key] = default
                    return

                if tp in [ObjectId, int, float, bool]:
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
        
        for key, tp, default in self._required_params:
            filter_parameter(key, tp, default)
        
        params = getattr(self, '_%s_params' % method, None)
        if params is None:
            return rpd

        #need arguments
        try:
            for key, tp in params.get('need', []):
                if tp == list:
                    filter_parameter(key, tp, [])
                else:
                    filter_parameter(key, tp)
        except ValueError as e:
            app_log.error('%s request need arguments parse error: %s' % (method, e))
            raise ValueError(e)
        except Exception as e:
            app_log.error('%s request need arguments parse error: %s' % (method, e))
            raise e

        #option arguments
        for key, tp, default in params.get('option', []):
            filter_parameter(key, tp, default)

        return rpd

    def head(self, *args, **kwargs):
        self._method_call('HEAD', *args, **kwargs)

    def get(self, *args, **kwargs):
        self._method_call('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        self._method_call('POST', *args, **kwargs)

    def delete(self, *args, **kwargs):
        self._method_call('DELETE', *args, **kwargs)

    def patch(self, *args, **kwargs):
        self._method_call('PATCH', *args, **kwargs)

    def put(self, *args, **kwargs):
        self._method_call('PUT', *args, **kwargs)

    def options(self, *args, **kwargs):
        self._method_call('OPTIONS', *args, **kwargs)

    def _method_call(self, method, *args, **kwargs):
        api_call = getattr(self, method)
        try:
            api_call(*args, **kwargs)
        except ResponseError as e:
            resp = self.init_resp(e.code, e.msg)
        except tornado.web.HTTPError as e:
            raise tornado.web.HTTPError(e)
        except Exception as e:
            app_log.error(e, exc_info=True)
            resp = self.init_resp(1)
        else:
            resp = self.init_resp()

        self.wo_resp(resp)

    @staticmethod
    def init_resp(code=0, msg=None):
        """
        responsibility for rest api code msg
        can override for other style 

        :args code 0, rest api code 
        :args msg None, rest api msg

        """
        resp = {
            'code': code,
            'msg': msg,
            'res': {},
        }
        return resp

    def wo_resp(self, resp):
        """
        can override for other style
        """
        if resp['code'] != 0:
            return self.wo_json(resp)

        if isinstance(self._data, dict):
            resp['res'].update(self._data)

        return self.wo_json(resp)

    def HEAD(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)

    def GET(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)

    def POST(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)

    def DELETE(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)

    def PATCH(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)

    def PUT(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)

    def OPTIONS(self, *args, **kwargs):
        raise tornado.web.HTTPError(405)

    def route(self, route, *args, **kwargs):
        getattr(self,  "do_%s"%route, lambda *args, **kwargs: None)(*args, **kwargs)



class BaseHandler(BaseBaseHandler):
    pass


class ErrorHandler(tornado.web.RequestHandler):

    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        self.render('404.html', error_code=self._status_code)


def start(port=8888):
    app_log.info(app_config.app_name+' app start')
    tornado.web.ErrorHandler = app_config.error_handler or ErrorHandler
    application = tornado.web.Application(app_config.urls, **app_config.web_application_setting)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
