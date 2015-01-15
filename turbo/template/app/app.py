#-*- coding:utf-8 -*-

from base import BaseHandler

from turbo import logger

logger = logger.getLogger(__file__)


class HomeHandler(BaseHandler):

	def get(self, *args, **kwargs):
		self.render('index.html')


class ApiHandler(BaseHandler):

	def GET(self, route, *args, **kwargs):
		self.route(route, *args, **kwargs)

	def do_route(self, *args, **kwargs):
		self.data = {
			'hello': 'world'
		}