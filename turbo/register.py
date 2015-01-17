from turbo.app import app_config
from turbo.util import join_sys_path, import_object


def regisger_app(app_name, app_setting, main_file):
	"""insert current project root path into sys path

	"""
	join_sys_path(main_file, dir_level_num=2)
	app_config.app_name = app_name
	app_config.app_setting = app_setting
	

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
		name, handler, **args = item
		register_url(url, handler, **args)