from __future__ import absolute_import, division, print_function, with_statement

import os
import logging

from turbo.conf import app_config
from turbo.util import join_sys_path, get_base_dir, import_object
import turbo.helper
from turbo.helper import install_helper


def _install_app(package_space):
    for app in getattr(import_object('apps.settings', package_space), 'INSTALLED_APPS'):
       _ = import_object('.'.join(['apps', app]), package_space)        


def register_app(app_name, app_setting, web_application_setting, mainfile, package_space):
    """insert current project root path into sys path
    """
    from turbo import log
    app_config.app_name = app_name
    app_config.app_setting = app_setting
    app_config.project_name = os.path.basename(get_base_dir(mainfile, 2))
    app_config.web_application_setting.update(web_application_setting)
    if app_setting.get('session_config'):
        app_config.session_config.update(app_setting['session_config'])
    log.getLogger(**app_setting.log)
    _install_app(package_space)


def register_url(url, handler, name=None, kwargs=None):
    """insert url into tornado application handlers group
    
    :arg str url: url 
    :handler object handler: url mapping handler 
    :name reverse url name
    :kwargs dict tornado handler initlize args
    """
    if name is None and kwargs is None:
        app_config.urls.append((url, handler))
        return

    if name is None:
        app_config.urls.append((url, handler, kwargs))
        return

    app_config.urls.append((url, handler, kwargs, name))
    

def register_group_urls(prefix, urls):
    for item in urls:
        url, handler = item[0:2]
        register_url(prefix+url, handler, *item[2:])