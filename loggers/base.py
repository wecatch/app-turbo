#-*- coding:utf-8 -*-

import os
import logging

import setting

_formater = logging.Formatter('%(levelname)s:%(asctime)s %(name)s:%(lineno)d:%(funcName)s %(message)s')

def _getSimpleHanlder(logfile, maxBytes=50*1024*1024, backupCount=3):
    #root logger default warning change to debug
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    from logging import handlers
    fh = handlers.RotatingFileHandler(logfile, maxBytes=maxBytes, backupCount=backupCount)
    fh.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    fh.setFormatter(_formater)
    ch.setFormatter(_formater)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


def getLogger(currfile, logfile=None, maxBytes=500*1024*1024, backupCount=3):
    if logfile:
        return _getSimpleHanlder(logfile, maxBytes, backupCount)

    if not logging.root.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(_formater)
        logging.root.addHandler(ch)
    
    #normal logger name
    if isinstance(currfile, basestring) and currfile.strip():
        return logging.getLogger(currfile)  

    path = os.path.abspath(currfile)
    if not os.path.isfile(path):
        raise Exception("%s is invalid module" % currfile)

    file_name = os.path.basename(path)
    dot_index = file_name.rfind('.')
    if dot_index < 0:
        raise Exception("%s is invliad python file" % currfile)
    
    module_name = file_name[0:dot_index]
    logger_name_list = [module_name]
    
    # find server root dir util find it or to root dir '/'
    while 1:
        path = os.path.dirname(path)     
        dirname = os.path.basename(path)
        if dirname == setting.SERVER_NAME or dirname == '/':
            break
        logger_name_list.append(dirname)

    logger_name_list.reverse()

    return logging.getLogger('.'.join(logger_name_list))
