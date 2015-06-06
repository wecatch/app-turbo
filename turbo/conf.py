from __future__ import absolute_import, division, print_function, with_statement

from tornado.util import ObjectDict


_cookie_session_config = ObjectDict(
    cookie_name='session_id',
    cookie_domain=None,
    cookie_path=None,
    expired=86400,  # 24 hours in seconds
    ignore_expiry=True,
    secret_key='fLjUfxqXtfNoIldA0A0J'
    ignore_change_ip=True,
    expired_message='Session expired',
)

_header_session_config = ObjectDict(
    header_name='session_id',
    expired=86400,  # 24 hours in seconds
    ignore_expiry=True,
    secret_key='fLjUfxqXtfNoIldA0A0J'
    ignore_change_ip=True,
    expired_message='Session expired',
)

class AppConfig(object):

    def __init__(self):
        self.app_name = ''
        self.urls = []
        self.error_handler = None
        self.app_setting = {}
        self.web_application_setting = {}
        self.project_name = None
        self.session_config = {
            'cookie': _cookie_session_config,
            'header': _header_session_config,
        }


    @property
    def log_level(self):
        import logging
        level = self.app_setting.get('log', {}).get('log_level')
        if level is None:
            return logging.INFO

        return level

app_config = AppConfig()
