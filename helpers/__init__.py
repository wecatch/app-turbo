#-*- coding:utf-8 -*-

from settings import INSTALLED_HELPERS as _INSTALLED_HELPERS

import turbo.helper

turbo.helper.install_helper(_INSTALLED_HELPERS, globals())
