import os
import logging

from turbo.conf import app_config
from turbo.util import join_sys_path, get_base_dir
from turbo import logger


def regisger_app(app_name, app_setting, web_application_setting, mainfile):
    """insert current project root path into sys path

    """
    app_config.app_name = app_name
    app_config.app_setting = app_setting
    app_config.project_name = os.path.basename(get_base_dir(mainfile, 2))
    app_config.web_application_setting = web_application_setting
    logger.init_file_logger(logging.getLogger(), app_setting.log_path, app_setting.log_size, app_setting.log_count)

def register_url(url, handler, name=None, kwargs=None):
    """insert url into tornado application handlers group
    
    :arg str url: url 
    :arg object handler: url mapping handler 
    """
    if kwargs and name:
        app_config.urls.append((url, handler, kwargs, name))
        return

    if kwargs:
        app_config.urls.append((url, handler, kwargs))
        return

    if name:
        app_config.urls.append((url, handler, None, name))
        return


def register_group_urls(prefix, urls):
    for item in urls:
        args = [None, None]
        url, handler = item[0:2]
        if item[2:] == 2:
            args = item[2:]
        if item[2:] == 1:
            args = [item[2], None]
            
        register_url(prefix+url, handler, *args)
