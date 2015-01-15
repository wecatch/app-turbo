# -*- coding:utf-8 -*-

import turbo.app 

import settings


class MixinHandler(turbo.app.BaseHandler):
    pass


class BaseHandler(MixinHandler):

    _session = None
    
    def initialize(self):
        super(BaseHandler, self).initialize()
        self._params = self.parameter
        self._skip = 0
        self._limit = 0

    def prepare(self):
        super(BaseHandler, self).prepare()

        self._skip = abs(self._params['skip']) if self._params.get('skip', None) else 0
        self._limit = abs(self._params['limit']) if self._params.get('limit', None) else 20