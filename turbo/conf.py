from __future__ import absolute_import, division, print_function, with_statement

from copy import deepcopy

class ObjectDict(dict):
    """Makes a dictionary behave like an object, with attribute-style access.
    """
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

        def __setattr__(self, name, value):
            self[name] = value


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
        self.web_application_setting = {'debug': False}
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
