# -*- coding:utf-8 -*-

import inspect
import os
import sys
from datetime import datetime, date
import time
import json
from collections import Iterable
import copy
import base64

from bson.objectid import ObjectId

from turbo.log import util_log

PY3 = sys.version_info >= (3,)

if PY3:
    unicode_type = str
    basestring_type = str
    file_types = 'file'
    from base64 import decodebytes, encodebytes
else:
    # The names unicode and basestring don't exist in py3 so silence flake8.
    unicode_type = unicode  # noqa
    basestring_type = basestring  # noqa
    file_types = file
    from base64 import encodestring as encodebytes, decodestring as decodebytes

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
        return unicode_type(v)

    if isinstance(v, datetime):
        return format_time(v)

    if isinstance(v, date):
        return format_time(v)

    return v


def to_str(v, encode=None):
    """convert any list, dict, iterable and primitives object to string
    """
    if isinstance(v, basestring_type):
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
        util_log.error('%s is invalid objectid' % objid)
        return None

    return objid


def json_encode(data, **kwargs):
    try:
        return json.dumps(data, **kwargs)
    except:
        util_log.error('Uncaught exception in json_encode', exc_info=True)


def json_decode(data, **kwargs):
    try:
        return json.loads(data, **kwargs)
    except:
        util_log.error('Uncaught exception in json_decode', exc_info=True)


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
        return datetime.fromtimestamp(t / 1000)
    else:
        return datetime.fromtimestamp(t)


def to_time(t, micro=False):
    if micro:
        return time.mktime(t.timetuple()) * 1000
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
    obj = __import__('.'.join(parts[:-1]),
                     package_space, None, [str(parts[-1])], 0)
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
        if index != 0 and index != length - 1 and i.isupper():
            as_list.append('_%s' % i.lower())
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

        # os.rmdir can't be allowed to deldte not empty
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
                    print("model %s has no 'index' attribute" % attr.__name__)


_UTF8_TYPES = (bytes, type(None))


def utf8(value):
    # type: (typing.Union[bytes,unicode_type,None])->typing.Union[bytes,None]
    """Converts a string argument to a byte string.

    If the argument is already a byte string or None, it is returned unchanged.
    Otherwise it must be a unicode string and is encoded as utf8.
    """
    if isinstance(value, _UTF8_TYPES):
        return value
    if not isinstance(value, unicode_type):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.encode("utf-8")


_BASESTRING_TYPES = (basestring_type, type(None))


def to_basestring(value):
    """Converts a string argument to a subclass of basestring.

    In python2, byte and unicode strings are mostly interchangeable,
    so functions that deal with a user-supplied argument in combination
    with ascii string constants can use either and should return the type
    the user supplied.  In python3, the two types are not interchangeable,
    so this method is needed to convert byte strings to unicode.
    """
    if isinstance(value, _BASESTRING_TYPES):
        return value
    if not isinstance(value, bytes):
        raise TypeError(
            "Expected bytes, unicode, or None; got %r" % type(value)
        )
    return value.decode("utf-8")


def get_func_name(func):
    name = getattr(func, 'func_name', None)
    if not name:
        name = getattr(func, '__name__', None)
    return name

