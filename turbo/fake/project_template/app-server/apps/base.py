# -*- coding:utf-8 -*-

import tornado.web
import turbo.app
from turbo import app_config
from turbo.core.exceptions import ResponseError, ResponseMsg
from lib.session import SessionStore, SessionObject


class MixinHandler(turbo.app.BaseHandler):
    pass


class BaseHandler(MixinHandler):

    session_initializer = {
        'uid': None,
        'avatar': None,
        'nickname': None,
    }
    session_object = SessionObject
    session_store = SessionStore()
    
    def initialize(self):
        super(BaseHandler, self).initialize()
        self._params = self.parameter

    def prepare(self):
        super(BaseHandler, self).prepare()

    def response_msg(self, msg='', code=1):
        raise ResponseMsg(code, msg)

    def response_error(self, msg='', code=1):
        raise ResponseError(code, msg)

    def http_error(self, status_code=404):
        raise tornado.web.HTTPError(status_code)

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.
        http://tornado.readthedocs.org/en/stable/_modules/tornado/web.html#RequestHandler.write_error
        """
        super(BaseHandler, self).write_error(status_code, **kwargs)


class ErrorHandler(BaseHandler):

    def initialize(self, status_code):
        super(ErrorHandler, self).initialize()
        self.set_status(status_code)
 
    def prepare(self):
        if not self.is_ajax():
            if self.get_status() == 404:
                raise self.http_error(404)
        else:
            self.wo_resp({'code': 1, 'msg': 'Api Not found'})
            self.finish()
            return

    def check_xsrf_cookie(self):
        # POSTs to an ErrorHandler don't actually have side effects,
        # so we don't need to check the xsrf token.  This allows POSTs
        # to the wrong url to return a 404 instead of 403.
        pass


from turbo.conf import app_config
app_config.error_handler = ErrorHandler