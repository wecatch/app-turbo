# -*- coding:utf-8 -*-

import os
import sys
from datetime import datetime
import time
import logging 
import json

from bson.objectid import ObjectId

from turbo.log import util_log


class TurboEscape(object):

    @classmethod
    def to_list_str(cls, value):
        """递归序列化list
        """
        for index, v in enumerate(value):
            if isinstance(v, dict):
                value[index] = cls.to_dict_str(v)
                continue

            if isinstance(v, list):
                value[index] = cls.to_list_str(v)
                continue

            value[index] = cls.default_encode(v)

        return value

    @classmethod
    def to_dict_str(cls, value):
        """递归序列化dict
        """
        for k, v in value.items():
            if isinstance(v, dict):
                value[k] = cls.to_dict_str(v)
                continue

            if isinstance(v, list):
                value[k] = cls.to_list_str(v)
                continue

            value[k] = cls.default_encode(v)

        return value

    @classmethod
    def default_encode(cls, v):
        """数据类型转换
        """
        if isinstance(v, ObjectId):
            return unicode(v)

        if isinstance(v, datetime):
            return cls.format_time(v)

        return v

    @staticmethod
    def format_time(dt):
        """datetime format
        """
        return time.mktime(dt.timetuple())

    @classmethod
    def recursive_to_str(cls, v):
        if isinstance(v, list):
            return cls.to_list_str(v)

        if isinstance(v, dict):
            return cls.to_dict_str(v)

        return cls.default_encode(v)

    @staticmethod
    def to_objectid(objid):
        """字符对象转换成objectid
        """  
        if objid is None:
            return objid
            
        try:
            objid = ObjectId(objid)
        except:
            util_log.error("%s is invalid objectid" % objid)
            return None
        
        return objid

    @staticmethod
    def json_encode(data):
        try:
            return json.dumps(data)
        except Exception as e:
            util_log.error(e)

    @staticmethod
    def json_decode(data):
        try:
            return json.loads(data)
        except Exception as e:
            util_log.error(e)

    @staticmethod
    def to_int(value, default=None):
        try:
            return int(value)
        except ValueError as e:
            util_log.error(e)

    @staticmethod
    def to_float(value, default=None):
        try:
            return float(value)
        except ValueError as e:
            util_log.error(e)

    @staticmethod
    def to_datetime(t, micro=True):
        if micro:
            return datetime.fromtimestamp(t/1000)
        else:
            return datetime.fromtimestamp(t)

    @staticmethod
    def to_time(t, micro=False):
        if micro:
            return time.mktime(t.timetuple())*1000
        else:
            return time.mktime(t.timetuple())


escape = TurboEscape()


def get_base_dir(currfile, dir_level_num=3):
    """
    find certain path according to currfile
    """
    root_path = os.path.abspath(currfile)
    for i in range(0, dir_level_num):
        root_path = os.path.dirname(root_path)

    return root_path


def join_sys_path(currfile, dir_level_num=3):
    """
    find certain path then load into sys path
    """
    if os.path.isdir(currfile):
        root_path = currfile
    else:
        root_path = get_base_dir(currfile, dir_level_num)
    
    sys.path.append(root_path)


def import_object(name, package_space=None):
    if name.count('.') == 0:
        return __import__(name, package_space, None)

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), package_space, None, [str(parts[-1])], 0)
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])
