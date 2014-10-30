#-*- coding:utf-8 -*-

from base import BaseHandler

import loggers

from helpers import user

logger = loggers.getLogger(__file__)


class ListCommentHandler(BaseHandler):

    _get_params = {
            'need':[
                ('page', int),
            ],
            'option':[
                ('name', basestring, None),
            ]
        }

    def GET(self, route, _id):
        skip = self._params['skip']
        limit = self._params['limit']

        callback = getattr(self, 'do_%s_comment'%route, None)
        self._data = callback(route, _id) if callback else self.http_error(404)

    def do_food_comment(self, route, _id):
        return {'cos': []}


class FoodHandler(BaseHandler):

    def get(self, _id):
        logger.info('a')
        self.render('index.html')