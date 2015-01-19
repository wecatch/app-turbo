import os
import logging

from turbo.conf import app_config
from turbo.util import join_sys_path, get_base_dir
from turbo import log


def regisger_app(app_name, app_setting, web_application_setting, mainfile):
    """insert current project root path into sys path

    """
    app_config.app_name = app_name
    app_config.app_setting = app_setting
    app_config.project_name = os.path.basename(get_base_dir(mainfile, 2))
    app_config.web_application_setting = web_application_setting
    log.init_file_logger(logging.getLogger(), app_setting.log_path, app_setting.log_size, app_setting.log_count)

def register_url(url, handler, name=None, kwargs=None):
    """insert url into tornado application handlers group
    
    :arg str url: url 
    :arg object handler: url mapping handler 
    :name reverse url name
    :kwargs dict tornado handler initlize args
    """
    app_config.urls.append((url, handler, kwargs, name))


def register_group_urls(prefix, urls):
    for item in urls:
        url, handler = item[0:2]
        register_url(prefix+url, handler, *item[2:])
