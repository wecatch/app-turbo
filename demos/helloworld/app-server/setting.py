import os
import sys
from tornado.util import ObjectDict

# app name
APP_NAME = 'demo'

# app base bapth
BASE_APP_DIR = os.path.dirname(os.path.abspath(__file__))
# project base path
BASE_PROJECT_DIR = os.path.dirname(BASE_APP_DIR)
sys.path.append(BASE_PROJECT_DIR)

# tornado web application settings
# details in http://www.tornadoweb.org/en/stable/web.html#tornado.web.Application.settings
WEB_APPLICATION_SETTING = ObjectDict(
    static_path=os.path.join(BASE_APP_DIR, "static"),
    template_path=os.path.join(BASE_APP_DIR, "templates"),
    xsrf_cookies=True,
    cookie_secret="xxx-xxx-xxx",
)

# turbo app setting 
APP_SETTING = ObjectDict(
    log=ObjectDict(
        log_path=os.path.join("/var/log/", APP_NAME+'.log'),
        log_size=500*1024*1024,
        log_count=3,
    )
)

# check if app start in debug
if os.path.exists(os.path.join(BASE_APP_DIR, '__test__')):
    WEB_APPLICATION_SETTING['debug'] = True
    APP_SETTING.log.log_path = os.path.join("", APP_NAME+'.log')