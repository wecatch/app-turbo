#-*- conding:utf-8-*-

import time
import uuid
import inspect


class DataObject(object):
    '''
    object cahced by app
    '''
    
    def __init__(self, key, data_source, expire):
        self.key = key
        self.expire = expire
        self.data_source = data_source
        self.last_visit_atime = time.time()
        self.value = None

    def is_expired(self):
        return time.time() - self.last_visit_atime > self.expire

    def update_visit_time(self):
        self.last_visit_atime = time.time()


class ObjectCache(object):
    """App local cache object 

    Attribute:
        _data: cache all data
    """
    _data = {}

    @staticmethod
    def create(data_source, name=None, expire=600):
        """
        args:
            data_source: load data, a callable object
            name: given by developer to mark the cache data 
            expire: cache expire time

        return:
            obj_key: the key that finally is used to mark the cache data 
        """
        if not callable(data_source):
            raise Exception("data_source %s must be callable " % data_source)
        
        if not isinstance(expire, int):
            raise Exception("expire %s must be int type" % expire)

        if name:
            try:
                hash(name)
            except TypeError:
                raise TypeError("name %s is unhashable"% name)
            obj_key = name
        else:
            obj_key = uuid.uuid4()

        obj_data = DataObject(obj_key, data_source, expire)
        ObjectCache._data[obj_key] = obj_data

        return obj_key

    @staticmethod
    def get(obj_key, *args, **kwargs):
        if obj_key not in ObjectCache._data:
            raise Exception("%s is invalid key" % obj_key)

        obj_data = ObjectCache._data[obj_key]

        if obj_data.value is None or obj_data.is_expired():
            obj_data.value = obj_data.data_source(*args, **kwargs)
            obj_data.update_visit_time()

        return obj_data.value

    @staticmethod
    def remove(obj_key):
        if obj_key in ObjectCache._data:
            ObjectCache._data[obj_key].value = None
