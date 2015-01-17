#-*- conding:utf-8 -*-
from tornado.util import import_object

from settings import INSTALLED_APPS


for item in INSTALLED_APPS:
    import_object('apps'+'.'+item)