#-*- coding:utf-8 -*-

from apps import base

import setting

class BaseHandler(base.BaseHandler):

    _get_required_params = [('who', basestring, None)]

    def initialize(self):
        super(BaseHandler,self).initialize()
        self.template_path = setting.TEMPLATE_PATH
