from __future__ import absolute_import, division, print_function, with_statement


import os
import logging
import logging.handlers

from turbo.conf import app_config


_formatter = logging.Formatter('%(levelname)s:%(asctime)s %(name)s:%(lineno)d:%(funcName)s %(message)s')


def _init_file_logger(logger, level, log_path, log_size, log_count):
    """
    one logger only have one level RotatingFileHandler 
    """
    if level not in [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]:
        level = logging.DEBUG

    for h in logger.handlers:
        if isinstance(h, logging.handlers.RotatingFileHandler):
            if h.level == level:
                return

    fh = logging.handlers.RotatingFileHandler(log_path, maxBytes=log_size, backupCount=log_count)
    fh.setLevel(level)
    fh.setFormatter(_formatter)
    logger.addHandler(fh)
    

def _init_stream_logger(logger, level=None):
    ch = logging.StreamHandler()
    ch.setLevel(level or logging.DEBUG)
    ch.setFormatter(_formatter)
    logger.addHandler(ch)


def _module_logger(path):
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

    return logging.getLogger('.'.join(logger_name_list))


def getLogger(currfile=None, level=None, log_path=None, log_size=500*1024*1024, log_count=3):
    # init logger first
    logger = None

    # py module logger
    if currfile is not None:
        path = os.path.abspath(currfile)
        if os.path.isfile(path):
            logger = _module_logger(path)
        elif isinstance(currfile, basestring) and currfile.strip():
            #normal logger
            logger = logging.getLogger(currfile)

        logger.setLevel(level or app_config.log_level)

    if not logger:
        logger = logging.getLogger()

    # keep the root logger at least have one streamhandler
    if not logger.root.handlers:
        _init_stream_logger(logger.root, level)

    if log_path:
        _init_file_logger(logger, level, log_path, log_size, log_count)

    return logger


# Logger objects for internal turbo use
app_log = getLogger('turbo.app')
model_log = getLogger('turbo.model', level=logging.WARNING)
util_log = getLogger('turbo.util')
helper_log = getLogger('turbo.helper')
session_log = getLogger('turbo.session')