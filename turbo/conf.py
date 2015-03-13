class AppConfig(object):

    def __init__(self):
        self.app_name = None
        self.urls = []
        self.error_handler = None
        self.app_setting = {}
        self.web_application_setting = None
        self.project_name = None

    @property
    def log_level(self):
        import logging
        level = self.app_setting.get('log', {}).get('log_level')
        if level is None:
            return logging.INFO

        return level

app_config = AppConfig()