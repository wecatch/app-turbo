#-*- coding:utf-8 -*-

from tornado.options import define, options

import setting

import apps
import turbo.register
import turbo.app


define("port", default=8888, type=int)

if __name__ == '__main__':
	turbo.register.regisger_app(setting.APP_NAME, setting.APP_SETTING, setting.WEB_APPLICATION_SETTING, __file__)
    turbo.app.start(port)