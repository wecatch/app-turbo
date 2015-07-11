# -*- coding:utf-8 -*-

import turbo.app 


class MixinHandler(turbo.app.BaseHandler):
    pass


class BaseHandler(MixinHandler):
    
    def initialize(self):
        super(BaseHandler, self).initialize()
        self._params = self.parameter


    def prepare(self):
        super(BaseHandler, self).prepare()
