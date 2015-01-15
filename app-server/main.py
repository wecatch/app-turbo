#-*- coding:utf-8 -*-

import logging
import sys
import os

import tornado.web
import tornado.httpserver
import tornado.options

from tornado.options import define, options

import setting

import turbo

turbo.register.regisger_app(setting)

turbo.register.start()


from turbo.register import regisger_app
from turbo.util import join_sys_path


from apps import urlpatterns

define("port", default=8888, type=int)

logger = logging.getLogger()

class ErrorHandler(tornado.web.RequestHandler):

    def initialize(self,status_code):
        self.set_status(status_code)

    def prepare(self):
        self.render('404.html',error_code = self._status_code)


class Application(tornado.web.Application):
    def __init__(self):

        handlers = urlpatterns

        settings = dict(
                template_path = setting.TEMPLATE_PATH,
                static_path = setting.STATIC_PATH,
                xsrf_cookies = setting.XSRF_COOKIES,
                cookie_secret = setting.COOKIE_SECRET, 
                login_url="/login",
                autoescape=None,  
                debug = setting.DEBUG,
                )

        tornado.web.Application.__init__(self, handlers, **settings)
        tornado.web.ErrorHandler = ErrorHandler


def main():
    print 'system started ...'
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application(),xheaders=True)
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()


if __name__ == '__main__':
    main()
