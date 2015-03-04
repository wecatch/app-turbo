#-*- coding:utf-8 -*-

from settings import INSTALLED_HELPERS

import turbo.helper

turbo.helper.install_helper(INSTALLED_HELPERS, globals())
