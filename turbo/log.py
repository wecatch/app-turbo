
import os
import logging

from turbo.conf import app_config


formatter = logging.Formatter('%(levelname)s:%(asctime)s %(name)s:%(lineno)d:%(funcName)s %(message)s')


def init_file_logger(logger, log_path, log_size, log_count):
    fh = logging.handlers.RotatingFileHandler(log_path, maxBytes=log_size, backupCount=log_count)
    fh.setLevel(app_config.get_log_level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    

def init_logger(logger):
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def getLogger(currfile=None, log_path=None, log_size=500*1024*1024, log_count=3):

    if not logging.root.handlers:
        root_logger = logging.getLogger()
        root_logger.setLevel(app_config.get_log_level)
        init_logger(root_logger)
        if log_path:
            init_file_logger(root_logger, log_path, log_size, log_count)

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
        logger.setLevel(app_config.get_log_level)

        if logger.handlers:
            return logger

        return logging.getLogger(currfile)

    return logging.getLogger()

# Logger objects for internal turbo use
app_log = getLogger('turbo.app')
model_log = getLogger('turbo.model')
util_log = getLogger('turbo.util')
helper_log = getLogger('turbo.helper')