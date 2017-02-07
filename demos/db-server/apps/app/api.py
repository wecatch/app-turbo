# -*- coding:utf-8 -*-

import turbo.log

from . import base
from models.blog.model import Blog

BaseHandler = base.BaseHandler
logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def GET(self):
        self._data = [{'id': i.id, 'title': i.title} for i in self.db.query(Blog).add_columns(
            Blog.id, Blog.title).all()]
