#-*- coding:utf-8 -*-

from apps import base

from setting import (TEMPLATE_PATH as _TEMPLATE_PATH)

class BaseHandler(base.BaseHandler):

    def initialize(self):
        super(BaseHandler,self).initialize()
        self._params = self.parameter
        self.template_path = _TEMPLATE_PATH
