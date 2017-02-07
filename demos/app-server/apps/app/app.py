# -*- coding:utf-8 -*-


import turbo.log
from turbo.flux import state as turbo_state
import tornado.gen

from . import base
from helpers import user as user_helper
from models.user import model as user_model

BaseHandler = base.BaseHandler
logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('index.html', metric=turbo_state.metric)


class AsynHandler(BaseHandler):

    @tornado.gen.coroutine
    def get(self):
        result = yield user_model.Tag().find_many(limit=10)
        self.render('tag.html', result=result)


class ApiHandler(BaseHandler):

    def GET(self, *args, **kwargs):
        self._data = {
            'msg': 'hello turbo world'
        }
