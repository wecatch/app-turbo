# -*- coding:utf-8 -*-

import turbo.log

from base import BaseHandler
from models.blog.model import Blog

logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def GET(self):
        self._data = [{'id': i.id, 'title': i.title} for i in self.db.query(Blog).add_columns(
            Blog.id, Blog.title).all()]
