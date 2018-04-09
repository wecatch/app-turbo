# -*- coding:utf-8 -*-

from turbo.util import basestring_type as basestring

from apps import base

from . import setting




class BaseHandler(base.BaseHandler):

    _get_required_params = [('who', str, None)]

    def initialize(self):
        super(BaseHandler, self).initialize()
        self.template_path = setting.TEMPLATE_PATH
