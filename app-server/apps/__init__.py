#-*- conding:utf-8 -*-
from settings import INSTALLED_APPS

for item in INSTALLED_APPS:
    exec('import '+ item)