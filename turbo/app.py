# -*- coding:utf-8 -*-
from __future__ import absolute_import, print_function

import os

try:
    basestring
except Exception as e:
    basestring = str

import tornado.web
import tornado.httpserver
import tornado.escape
import tornado.ioloop
from tornado.options import define, options
from tornado.util import ObjectDict

from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId

from turbo.core.exceptions import ResponseMsg, ResponseError
from turbo.util import escape as _es
import turbo.httputil as _ht 
from turbo.log import app_log
from turbo.conf import app_config
from turbo.session import Session, DiskStore


class Mixin(tornado.web.RequestHandler):

    @staticmethod
    def to_objectid(objid):
        """Convert string into ObjectId
        """
        return _es.to_objectid(objid)

    @staticmethod
    def to_int(value):
        """Convert string into int
        """
        return _es.to_int(value)

    @staticmethod
    def to_float(value):
        """Convert string into float
        """
        return _es.to_float(value)

    @staticmethod
    def to_bool(value):
        """Convert value into bool
        """
        return bool(value)

    @staticmethod
    def to_str(v):
        """Convert value into string
        """
        return _es.to_str(v)

    @staticmethod
    def utf8(v):
        """Convert string into utf8 string
        """
        return tornado.escape.utf8(v)

    @staticmethod
    def encode_http_params(**kw):
        """url parameter encode
        """
        return _ht.encode_http_params(**kw)

    @staticmethod
    def json_encode(data, **kwargs):
        return _es.json_encode(data, **kwargs)

    @staticmethod
    def json_decode(data, **kwargs):
        return _es.json_decode(data, **kwargs)

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With', None) == 'XMLHttpRequest'


class BaseBaseHandler(Mixin):
    """
    config request parameter like this:

    attrs:
        _get_params: need and option arguments for request hander like
                        _get_params = {
                                'need':[
                                    ('skip', int),
                                    ('limit', int),
                                ],
                                'option':[
                                    ('jsoncallback', basestring, None),
                                ]
                            }
        _post_params: the same to _get_params for post method

        _required_params: required arguments for all sub handler that element is three tuple like  [('skip', int, 0), ('limit', int, 0)]
        _get_required_params: the same to _required_params for get method
        _post_required_params: the same to _required_params for post method
        _put_required_params: the same to _required_params for put method 
        _delete_required_params: the same to _required_params for delete method
        _head_required_params: the same to _required_params for head method 
        _patch_required_params: the same to _required_params for patch method 
        _options_required_params: the same to _required_params for options method 
    
    """

    # override in subclass
    _required_params = []
    # override in subclass to extract the most need arguments
    
    _types = [ObjectId, None, basestring, str, int, float, list, file, bool]
    _data = None
    _session = None

    session_initializer = None 
    session_config = None
    session_object = None
    session_store = None # store for session

    def initialize(self):
        # app template path if exist must end with slash like user/
        # request context
        self.template_path = ''

    @property
    def session(self):
        if not self._session:
            self._session = Session(self.application, 
                self,
                self.session_store, 
                self.session_initializer, 
                self.session_config,
                self.session_object
            )

        return self._session

    def get_template_namespace(self):
        namespace = super(BaseBaseHandler, self).get_template_namespace()
        context = self.get_context()
        namespace.update({'context': context})
        return namespace

    def render_string(self, template_name, **kwargs):
        return super(BaseBaseHandler, self).render_string('%s%s' % (self.template_path, template_name), **kwargs)

    def sort_by(self, sort):
        return {1: ASCENDING, -1: DESCENDING}.get(sort, ASCENDING)

    # request context
    def get_context(self):
        return ObjectDict(session=self.session)

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

                if tp == basestring or tp == str:
                    rpd[key] = self.get_argument(key, strip=False)
                    return

                if tp == list:
                    rpd[key] = self.get_arguments(key)
                    return

            if tp == file:
                if key not in files:
                    rpd[key] = []
                    return

                rpd[key] = self.request.files[key]                
        
        required_params = getattr(self, '_required_params', None)
        if isinstance(required_params, list):
            for key, tp, default in required_params:
                filter_parameter(key, tp, default)

        #extract method required params
        method_required_params = getattr(self, '_%s_required_params' % method, None)
        if isinstance(method_required_params, list):
            for key, tp, default in method_required_params:
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
        except ResponseMsg as e:
            resp = self.init_resp(e.code, e.msg)
        except tornado.web.HTTPError as e:
            raise e
        except Exception as e:
            app_log.error('Uncaught Exception in %s %s call'%(getattr(getattr(self, '__class__'), '__name__'), method), exc_info=True)
            resp = self.init_resp(1, 'Unknown Error')
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
        if self._data is not None:
            resp['res'] = self.to_str(self._data)

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

    def on_finish(self):
        self._processor()
        super(BaseBaseHandler, self).on_finish()

    def _processor(self):
        """
        can override in son class to do some clean work after request
        """
        session_save = getattr(self.session, 'save', None)
        if session_save:
            session_save()


class BaseHandler(BaseBaseHandler):
    pass


class ErrorHandler(tornado.web.RequestHandler):

    def initialize(self, status_code):
        self.set_status(status_code)

    def prepare(self):
        t = tornado.template.Template('<h1>{{error_code}}</h1>')
        self.write(t.generate(error_code=self._status_code))
        self.finish()


def start(port=8888):
    app_log.info(app_config.app_name+' app start')
    app_config.error_handler = app_config.error_handler if app_config.error_handler else ErrorHandler
    tornado.web.ErrorHandler = app_config.error_handler
    application = tornado.web.Application(app_config.urls, **app_config.web_application_setting)
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
