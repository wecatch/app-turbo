#-*- coding:utf-8 -*-

import turbo.log

from store import actions

from base import BaseHandler

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self):
        self.render('index.html')


class IncHandler(BaseHandler):

    _get_params = {
        'option': [
            ('value', int, 0)
        ]
    }

    def get(self):
        self._data = actions.increase(self._params['value'])
        self.write(str(self._data))


class MinusHandler(BaseHandler):

    _get_params = {
        'option': [
            ('value', int, 0)
        ]
    }

    def get(self):
        self._data = actions.decrease(self._params['value'])
        self.write(str(self._data))