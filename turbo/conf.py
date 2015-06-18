from __future__ import absolute_import, division, print_function, with_statement

from tornado.util import ObjectDict
from copy import deepcopy


class AppConfig(object):
    
    _cookie_session_config = ObjectDict(
        name='session_id',
        cookie_domain=None,
        cookie_path='/',
        cookie_expires=86400,  # cookie expired  24 hours in seconds
        secure = True,
        secret_key='fLjUfxqXtfNoIldA0A0J', # generate session id,
        timeout=86400, # session timeout 24 hours in seconds
    )

    _store_config = ObjectDict(
        diskpath='/tmp/session',
    )

    def __init__(self):
        self.app_name = ''
        self.urls = []
        self.error_handler = None
        self.app_setting = {}
        self.web_application_setting = {}
        self.project_name = None
        self.session_config = self._cookie_session_config
        self.store_config = self._store_config

    @property
    def log_level(self):
        import logging
        level = self.app_setting.get('log', {}).get('log_level')
        if level is None:
            return logging.INFO

        return level

app_config = AppConfig()
