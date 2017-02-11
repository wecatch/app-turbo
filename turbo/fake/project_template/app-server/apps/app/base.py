# -*- coding:utf-8 -*-

from . import setting
from apps import base


class BaseHandler(base.BaseHandler):

    def initialize(self):
        super(BaseHandler, self).initialize()
        self.template_path = setting.TEMPLATE_PATH
