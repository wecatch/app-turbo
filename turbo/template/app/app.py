#-*- coding:utf-8 -*-

from base import BaseHandler

import turbo.log

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

	def get(self):
		self.render('index.html')


class ApiHandler(BaseHandler):

	def GET(self, route=None, *args, **kwargs):
		self.route('route', *args, **kwargs)

	def do_route(self, *args, **kwargs):
        logger.info('api handler is calling')
		self.data = {
			'hello': 'world'
		}