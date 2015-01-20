#-*- coding:utf-8 -*-

from settings import INSTALLED_HELPERS

import turbo.helper

for item in INSTALLED_HELPERS:
    turbo.helper.install_helper(INSTALLED_HELPERS, globals())
