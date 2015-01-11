# -*- coding:utf-8 -*-

from datetime import datetime
import time
import logging 
import json

from bson.objectid import ObjectId

from turbo.log import util_log


class _Escape(object):

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
    def to_time(t, micro=True):
        if micro:
            return time.mktime(t.timetuple())*1000
        else:
            return time.mktime(t.timetuple())


escape = _Escape()


def import_object(name):
    """Imports an object by name.

    import_object('x') is equivalent to 'import x'.
    import_object('x.y.z') is equivalent to 'from x.y import z'.

    >>> import tornado.escape
    >>> import_object('tornado.escape') is tornado.escape
    True
    >>> import_object('tornado.escape.utf8') is tornado.escape.utf8
    True
    >>> import_object('tornado') is tornado
    True
    >>> import_object('tornado.missing_module')
    Traceback (most recent call last):
        ...
    ImportError: No module named missing_module
    """
    if name.count('.') == 0:
        return __import__(name, None, None)

    parts = name.split('.')
    obj = __import__('.'.join(parts[:-1]), None, None, [parts[-1]], 0)
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])