class AppConfig(object):

    def __init__(self):
        self.app_name = None
        self.urls = []
        self.error_handler = None
        self.lang = 'zh_CN'
        self.app_setting = None
        self.web_application_setting = None
        self.project_name = None
        self.log_level = None

    @property
    def get_log_level(self):
        import logging
        log_level = logging.INFO if app_config.log_level is None else app_config.log_level
        return log_level


app_config = AppConfig()