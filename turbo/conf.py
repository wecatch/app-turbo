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


app_config = AppConfig()