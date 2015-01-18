#-*- coding:utf-8 -*-

import os
import logging

from turbo.app import app_config

formater = logging.Formatter('%(levelname)s:%(asctime)s %(name)s:%(lineno)d:%(funcName)s %(message)s')


def init_logger(logger, logfile, maxBytes, backupCount):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formater)
    logger.addHandler(ch)
    
    if logfile:
        fh = logging.handlers.RotatingFileHandler(logfile, maxBytes=maxBytes, backupCount=backupCount)
        fh.setLevel(logging.INFO if app_config.log_level is None else app_config.log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def getLogger(currfile, logfile=None, maxBytes=500*1024*1024, backupCount=3):

    if not logging.root.handlers:
        init_logger(logging.root, logfile, maxBytes, backupCount)

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

        return logging.getLogger('.'.join(logger_name_list))

    if isinstance(currfile, basestring) and currfile.strip():
        logger = logging.getLogger(currfile)

        if logger.handlers:
            return logger

        return init_logger(logger, logfile, maxBytes, backupCount)

    return logging.getLogger()