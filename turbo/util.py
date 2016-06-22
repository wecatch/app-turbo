# -*- coding:utf-8 -*-

import inspect
import os
import sys
from datetime import datetime, date
import time
import logging 
import json
from collections import Iterable
import copy

from bson.objectid import ObjectId

from turbo.log import util_log

try:
    basestring
except Exception as e:
    basestring = str

def to_list_str(value, encode=None):
    """recursively convert list content into string

    :arg list value: The list that need to be converted.
    :arg function encode: Function used to encode object.
    """
    result = []
    for index, v in enumerate(value):
        if isinstance(v, dict):
            result.append(to_dict_str(v, encode))
            continue

        if isinstance(v, list):
            result.append(to_list_str(v, encode))
            continue

        if encode:
            result.append(encode(v))
        else:
            result.append(default_encode(v))

    return result


def to_dict_str(origin_value, encode=None):
    """recursively convert dict content into string
    """
    value = copy.deepcopy(origin_value)
    for k, v in value.items():
        if isinstance(v, dict):
            value[k] = to_dict_str(v, encode)
            continue

        if isinstance(v, list):
            value[k] = to_list_str(v, encode)
            continue

        if encode:
            value[k] = encode(v)
        else:
            value[k] = default_encode(v)

    return value


def default_encode(v):
    """convert ObjectId, datetime, date into string
    """
    if isinstance(v, ObjectId):
        return unicode(v)

    if isinstance(v, datetime):
        return format_time(v)
    
    if isinstance(v, date):
        return format_time(v)

    return v


def to_str(v, encode=None):
    """convert any list, dict, iterable and primitives object to string
    """
    if isinstance(v, basestring):
        return v

    if isinstance(v, dict):
        return to_dict_str(v, encode)

    if isinstance(v, Iterable):
        return to_list_str(v, encode)

    if encode:
        return encode(v)
    else:
        return default_encode(v)


def format_time(dt):
    """datetime format
    """
    return time.mktime(dt.timetuple())


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


def json_encode(data, **kwargs):
    try:
        return json.dumps(data, **kwargs)
    except Exception as e:
        util_log.error("Uncaught exception in json_encode", exc_info=True)


def json_decode(data, **kwargs):
    try:
        return json.loads(data, **kwargs)
    except Exception as e:
        util_log.error("Uncaught exception in json_decode", exc_info=True)


def to_int(value, default=None):
    try:
        return int(value)
    except ValueError as e:
        util_log.error(e)


def to_float(value, default=None):
    try:
        return float(value)
    except ValueError as e:
        util_log.error(e)


def to_datetime(t, micro=False):
    if micro:
        return datetime.fromtimestamp(t/1000)
    else:
        return datetime.fromtimestamp(t)


def to_time(t, micro=False):
    if micro:
        return time.mktime(t.timetuple())*1000
    else:
        return time.mktime(t.timetuple())


class Escape(object):
    
    __slots__ = ['to_list_str', 'to_dict_str', 'default_encode', 'format_time', 'to_objectid', 
        'to_str', 'to_time', 'to_datetime', 'to_int', 'to_float', 'json_decode', 'json_encode', '__gl']

    def __init__(self, module):
        self.__gl = module

    def __getattr__(self, name):
        if name in self.__slots__:
            return self.__gl.get(name)

        raise AttributeError('escape has no attribute %s' % name)


escape = Escape(globals())


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


def camel_to_underscore(name):
    """
    convert CamelCase style to under_score_case
    """
    as_list = []
    length = len(name)
    for index, i in enumerate(name):
        if index !=0 and index != length-1 and i.isupper():
            as_list.append('_%s'%i.lower())
        else:
            as_list.append(i.lower())

    return ''.join(as_list)


def remove_folder(path, foldername):
    if not foldername:
        return 

    if not os.path.isdir(path):
        return

    dir_content = os.listdir(path)
    if not dir_content:
        return 

    for item in dir_content:
        child_path = os.path.join(path, item)

        if not os.path.isdir(child_path):
            continue

        if item != foldername:
            remove_folder(child_path, foldername)
            continue

        #os.rmdir can't be allowed to deldte not empty
        for root, dirs, files in os.walk(child_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

            for name in dirs:
                os.rmdir(os.path.join(root, name))
        try:
            os.rmdir(child_path)
        except Exception as e:
            raise e


def remove_file(path, filename):
    if not filename:
        return 

    if not os.path.isdir(path):
        return

    dir_content = os.listdir(path)
    if not dir_content:
        return 

    for item in dir_content:
        child_path = os.path.join(path, item)

        if os.path.isdir(child_path):
            remove_file(child_path, filename)
            continue

        if item != filename:
            continue

        try:
            os.remove(child_path)
        except Exception as e:
            raise e


def remove_extension(path, extension):
    if not extension:
        return 

    if not os.path.isdir(path):
        return

    dir_content = os.listdir(path)
    if not dir_content:
        return 

    for item in dir_content:
        child_path = os.path.join(path, item)

        if os.path.isdir(child_path):
            remove_extension(child_path, extension)
            continue

        name, ext = os.path.splitext(item)

        if ext != extension:
            continue

        try:
            os.remove(child_path)
        except Exception as e:
            raise e


def build_index(model_list):
    from turbo.model import BaseModel
    for m in model_list:
        for attr_name in dir(m):
            attr = getattr(m, attr_name)
            if inspect.isclass(attr) and issubclass(attr, BaseModel) and hasattr(attr, 'name'):
                if hasattr(attr, 'index'):
                    for index in attr.index:
                        attr().create_index(index, background=True)
                else:
                    print("model %s has no 'index' attribute"%attr.__name__)
