#-*- coding:utf-8 -*-

from base import BaseHandler

import turbo.log

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.render('index.html')


class ApiHandler(BaseHandler):

    def GET(self, route=None, *args, **kwargs):
        self.route('route', *args, **kwargs)

    def do_route(self, *args, **kwargs):
        print logger.handlers
        logger.info('msg')
        self.data = {
            'hello': 'world',
            'h': logger.handlers
        }