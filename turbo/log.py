
import os
import logging
import logging.handlers

from turbo.conf import app_config

_level = app_config.get_log_level or logging.warning
_formatter = logging.Formatter('%(levelname)s:%(asctime)s %(name)s:%(lineno)d:%(funcName)s %(message)s')


def _init_file_logger(logger, level, log_path, log_size, log_count):
    
    level = _level if level is None else level
    if level not in [logging.DEBUG, logging.ERROR, logging.NOTSET, logging.WARNING, logging.INFO]:
        level = logging.DEBUG

    for h in logger.handlers:
        if isinstance(h, logging.handlers.RotatingFileHandler):
            if h.level == :
                return

    fh = logging.handlers.RotatingFileHandler(log_path, maxBytes=log_size, backupCount=log_count)
    fh.setLevel(app_config.get_log_level)
    fh.setFormatter(_formatter)
    logger.addHandler(fh)
    

def _init_stream_logger(logger):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(_formatter)
    logger.addHandler(ch)


def getLogger(currfile=None, level=None, log_path=None, log_size=500*1024*1024, log_count=3):
    # init logger first
    logger = None

    # py module logger
    path = os.path.abspath(currfile)
    if os.path.isfile(path):    
        file_name = os.path.basename(path)
        module_name = file_name[0:file_name.rfind('.py')]
        logger_name_list = [module_name]

        # find project root dir util find it or to root dir '/'
        while True:
            # root path check
            path = os.path.dirname(path)
            if path == '/':
                break

            # project root path
            dirname = os.path.basename(path)
            if dirname == app_config.project_name:
                break
            logger_name_list.append(dirname)

        logger_name_list.reverse()

        logger = logging.getLogger('.'.join(logger_name_list))

    #normal logger
    if isinstance(currfile, basestring) and currfile.strip():   
        logger = logging.getLogger(currfile)
        logger.setLevel(app_config.get_log_level)
        logger = logging.getLogger(currfile)

    if not logger:
        logger = logging.getLogger()

    if logger == logging.root:
        if not logger.handlers:
            _init_stream_logger(logger)

    level = _level if level is None else level = 

    if log_path:
        _init_file_logger(logger, level, log_path, log_size, log_count)

    return logger



# Logger objects for internal turbo use
app_log = getLogger('turbo.app')
model_log = getLogger('turbo.model')
util_log = getLogger('turbo.util')
helper_log = getLogger('turbo.helper')