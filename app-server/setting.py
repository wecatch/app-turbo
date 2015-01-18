import os

# app name
APP_NAME = 'demo'

# app base bapth
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# tornado web application settings
# details in http://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings
WEB_APPLICATION_SETTING = dict(
    "static_path": os.path.join(BASE_DIR, "static"),
    "template_path": os.path.join(BASE_DIR, "templates"),
    "xsrf_cookies": True,
    "cookie_secret": "xxx-xxx-xxx",
)

# turbo app setting 
APP_SETTING = dict(
    "log_path": os.path.join("/var/log/", APP_NAME),
    "log_size": 500*1024*1024,
    "log_count": 3,
)

# check if app start in debug
if os.path.exists(os.path.join(BASE_DIR, '__test__')):
    APPLICATION_SETTING['debug'] = True
    APP_SETTING['log_path'] = os.path.join("", APP_NAME)