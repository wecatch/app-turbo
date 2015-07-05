#-*- coding:utf-8 -*-


import turbo.log

from base import BaseHandler
from helpers import user as user_helper

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class ApiHandler(BaseHandler):

    def GET(self, *args, **kwargs):
        self._data = {
            'msg': 'hello turbo world'
        }