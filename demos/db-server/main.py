# -*- coding:utf-8 -*-

import tornado.options
import turbo.app
import turbo.register
from tornado.options import define, options

import setting

# uncomment this to init state manager: store
# import store

turbo.register.register_app(
    setting.SERVER_NAME,
    setting.TURBO_APP_SETTING,
    setting.WEB_APPLICATION_SETTING,
    __file__,
    globals()
)

define("port", default=8888, type=int)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    turbo.app.start(options.port)
