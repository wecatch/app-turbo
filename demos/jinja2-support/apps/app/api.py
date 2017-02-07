# -*- coding:utf-8 -*-

import turbo.log

from . import base

BaseHandler = base.BaseHandler
logger = turbo.log.getLogger(__file__)


class HomeHandler(BaseHandler):

    def GET(self):
        pass
