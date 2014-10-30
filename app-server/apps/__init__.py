#-*- conding:utf-8 -*-

import os
import sys

from settings import INSTALLED_APPS as _INSTALLED_APPS


# load app path into sys.path
def _app_path_load(dir_level_num=3):
    app_root_path = os.path.abspath(__file__)
    for i in range(0, dir_level_num):
        app_root_path = os.path.dirname(app_root_path)

    sys.path.append(app_root_path)


def pattern(prefix, handlers):
    urls = []
    for item in handlers:

        assert len(item) in (2, 3, 4)

        if len(item) == 2:
            url_pattern = ('%s%s' % (prefix, item[0]), item[1])

        if len(item) == 3:
             url_pattern = ('%s%s' % (prefix, item[0]), item[1], item[2])

        if len(item) == 4:
            url_pattern = ('%s%s' % (prefix, item[0]), item[1], item[2], item[3])

        urls.append(url_pattern)

    return urls


# install app from settings
def _install_app():
    urlpatterns = []
    for item in _INSTALLED_APPS:
        module = __import__('.'.join(['apps', item]), None, None, [item], 0)
        try:
            urlpatterns += pattern(module.prefix, module.urls)
        except AttributeError:
            raise ImportError("No module named %s"%item)


    return urlpatterns

_app_path_load()

#router
urlpatterns = _install_app()


