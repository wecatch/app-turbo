from __future__ import absolute_import, division, print_function, with_statement

from tornado.util import ObjectDict
from copy import deepcopy


class AppConfig(object):
    
    __cookie_session_config = ObjectDict(
        name='session_id',
        cookie_domain=None,
        cookie_path=None,
        expired=86400,  # 24 hours in seconds
        secret_key='fLjUfxqXtfNoIldA0A0J' # generate session id 
    )

    __header_session_config = ObjectDict(
        name='session_id',
        secret_key='fLjUfxqXtfNoIldA0A0J' # generate session id 
    )

    def __init__(self):
        self.app_name = ''
        self.urls = []
        self.error_handler = None
        self.app_setting = {}
        self.web_application_setting = {}
        self.project_name = None
        self.session_config = deepcopy(self.__cookie_session_config)

    @property
    def log_level(self):
        import logging
        level = self.app_setting.get('log', {}).get('log_level')
        if level is None:
            return logging.INFO

        return level

app_config = AppConfig()
