# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement


from datetime import datetime
import inspect
import time
import functools
from collections import defaultdict

from turbo.util import import_object

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING, collection
import tornado.ioloop

from turbo.log import model_log
from turbo.util import escape as _es


_record = lambda x: defaultdict(lambda: None, x)


def convert_to_record(func):
    """wrap mongodb record to a dict record

    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        if result is not None:
            if isinstance(result, dict):
                return _record(result)
            
            return (_record(i) for i in result)

        return result

    return wrapper


class MixinModel(object):

    @staticmethod
    def utctimestamp(seconds=None):
        if seconds:
            return long(time.mktime(time.gmtime(seconds)))
        else:
            return long(time.mktime(time.gmtime()))

    @staticmethod
    def timestamp():
        return long(time.time())

    @staticmethod
    def datetime(dt=None):
        if dt:
            return datetime.strptime(dt, '%Y-%m-%d %H:%M')
        else:
            return datetime.now()

    @staticmethod
    def utcdatetime(dt=None):
        if dt:
            return datetime.strptime(dt, '%Y-%m-%d %H:%M')
        else:
            return datetime.utcnow()

    @classmethod
    def to_one_str(cls, value, *args, **kwargs):
        """string化的单个record对象
        """
        if kwargs.get('wrapper'):
            return cls._wrapper_to_one_str(value)

        return _es.to_dict_str(value)

    @classmethod
    def to_str(cls, values, callback=None):
        """string化的多个record组成的list对象
        """
        if callback and callable(callback):
            if isinstance(values, dict):
                return callback(_es.to_str(values))

            return [callback(_es.to_str(i)) for i in values]
            
        return _es.to_str(values)

    @staticmethod
    @convert_to_record
    def _wrapper_to_one_str(value):
        return _es.to_dict_str(value)

    @staticmethod
    def default_encode(v):
        return _es.default_encode(v)

    @staticmethod
    def json_encode(v):
        return _es.json_encode(v)

    @staticmethod
    def json_decode(v):
        return _es.json_decode(v)

    @staticmethod
    def to_objectid(objid):
        return _es.to_objectid(objid)

    @staticmethod
    def create_objectid():
        """return ObjectId
        """
        return ObjectId()

    _instance = {}

    @classmethod
    def instance(cls, name):
        """
        instance application model
        """
        if not cls._instance.get(name):
            model_name = name.split('.')
            ins_name = '.'.join(['models', model_name[0], 'model', model_name[1]])
            cls._instance[name] = cls.import_model(ins_name)()

        return cls._instance[name]

    @classmethod
    def import_model(cls, ins_name):
        try:
            package_space = getattr(cls,  'package_space')
        except AttributeError:
            raise NotImplementedError
        else:
            return import_object(ins_name, package_space)

    @staticmethod
    def default_record():
        """
        generate one default record which return '' when key is empty 
        """
        return defaultdict(lambda: '')


def collection_method_call(turbo_connect_ins, name):
    def outwrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if name in turbo_connect_ins._write_operators:
                turbo_connect_ins._model_ins.write_action_call(name, *args, **kwargs)

            if name in turbo_connect_ins._read_operators:
                turbo_connect_ins._model_ins.read_action_call(name, *args, **kwargs)

            return func(*args, **kwargs)

        return wrapper

    return outwrapper


class TurboConnect(object):

    _write_operators = frozenset([
        'insert',
        'save',
        'update',
        'find_and_modify',
        'bulk_write',
        'insert_one',
        'insert_many',
        'replace_one',
        'update_one',
        'update_many',
        'delete_one',
        'delete_many',
        'find_one_and_delete',
        'find_one_and_replace',
        'find_one_and_update',
        'create_index',
        'drop_index',
        'create_indexes',
        'drop_indexes',
        'drop',
        'remove',
        'ensure_index',
        'rename',
        ])

    _read_operators = frozenset([
        'find',
        'find_one',
        'count',
        'index_information',
        ])

    def __init__(self, model_ins, db_collect=None):
        self._model_ins = model_ins
        self._collect = db_collect

    def __getattr__(self, name):
        collection_method = getattr(self._collect, name)
        if callable(collection_method):
            return collection_method_call(self, name)(collection_method)

        return collection_method

    def __getitem__(self, name):
        return self._collect[name]


class BaseBaseModel(MixinModel):
    """mongodb 基础api 访问

    name = None                            mongodb collection name
    field = None                           collection key
    column = None                          need to query field
    index = [
        tuple([('uid', 1)])                
    ]                                      query index
    """

    _operators = frozenset([
        '$set',
        '$unset',
        '$rename',
        '$currentDate',
        '$inc',
        '$max',
        '$min',
        '$mul',
        '$setOnInsert',

        '$addToSet',
        '$pop',
        '$pushAll',
        '$push',
        '$pull'])


    def __init__(self, db_name='test', _MONGO_DB_MAPPING=None):
        if _MONGO_DB_MAPPING is None:
            raise Exception("db mapping is invalid")

        # databases
        self.__db = _MONGO_DB_MAPPING['db']
        # databases file
        self.__db_file = _MONGO_DB_MAPPING['db_file']

        #databse name
        if db_name not in self.__db or self.__db.get(db_name, None) is None:
            raise Exception("%s is invalid databse" % db_name)

        # collection name
        if not self.name:
            raise Exception("%s is invalid collection name" % self.name)

        # collection field
        if not self.field or not isinstance(self.field, dict):
            raise Exception("%s is invalid collection field" % self.field)

        # collect as private variable
        collect = getattr(self.__db.get(db_name, object), self.name, None)
        if collect is None:
            raise Exception("%s is invalid collection" % self.name)

        # replace pymongo collect with custome connect
        self.__collect = TurboConnect(self, collect)

        # gridfs as private variable
        self.__gridfs = self.__db_file.get(db_name, None)
        if self.__gridfs is None:
            model_log.info("%s is invalid gridfs" % self.__gridfs)

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def __getitem__(self, k):
        return getattr(self, k)
    
    def __getattr__(self, k):
        attr = getattr(self.__collect, k)
        if isinstance(attr, collection.Collection):
            raise AttributeError("model object '%s' has not attribute '%s'"%(self.name, k))

        return attr

    def sub_collection(self, name):
        return self.__collect[name] 

    def __str__(self):
        if isinstance(self.field, dict):
            return unicode(self.field)

        return None

    # pymongo collection method
    def insert(self, doc_or_docs, **kwargs):
        """collection insert method
        args:
            w(optional):(integer or string) If this is a replica set,
            write operations will block until they have been replicated to the specified number or tagged set of servers.
            w=<int> always includes the replica set primary (e.g. w=3 means write to the primary and wait until replicated to two secondaries).
            Passing w=0 disables write acknowledgement and all other write concern options.

            wtimeout(optional): (integer) Used in conjunction with w.
            Specify a value in milliseconds to control how long to wait for write propagation to complete.
            If replication does not complete in the given timeframe, a timeout exception is raised.

        """
        check = kwargs.pop('check', False)
        if check is True:
            return self.create(doc_or_docs, **kwargs)

        return self.__collect.insert(doc_or_docs, **kwargs)

    def save(self, to_save, **kwargs):
        """collection save method

        """
        return self.__collect.save(to_save, **kwargs)

    def find_one(self, spec_or_id=None, *args, **kwargs):
        """collection find_one method

        """
        wrapper = kwargs.pop('wrapper', False)
        if wrapper is True:
            return self._wrapper_find_one(spec_or_id, *args, **kwargs)

        return self.__collect.find_one(spec_or_id, *args, **kwargs)

    def find(self, *args, **kwargs):
        """collection find method

        """
        wrapper = kwargs.pop('wrapper', False)
        if wrapper is True:
            return self._wrapper_find(*args, **kwargs)

        return self.__collect.find(*args, **kwargs)

    @convert_to_record
    def _wrapper_find_one(self, spec_or_id=None, *args, **kwargs):
        """convert record to a dict that has no key error

        """
        return self.__collect.find_one(spec_or_id, *args, **kwargs)

    @convert_to_record
    def _wrapper_find(self, *args, **kwargs):
        """convert record to a dict that has no key error

        """
        return self.__collect.find(*args, **kwargs)

    def update(self, spec, document, multi=False, **kwargs):
        """collection update method

        """
        for opk in document.keys():
            if not opk.startswith('$') or opk not in self._operators:
                raise ValueError("invalid document update operator")

        if not document:
            raise ValueError("empty document update not allowed")           

        return self.__collect.update(spec, document, multi=multi, **kwargs)

    def remove(self, spec_or_id=None, **kwargs):
        """collection remove method
        warning:
            if you want to remove all documents,
            you must override _remove_all method to make sure
            you understand the result what you do
        """
        if isinstance(spec_or_id, dict) and spec_or_id == {}:
            raise ValueError("not allowed remove all documents")

        if spec_or_id is None:
            raise ValueError("not allowed remove all documents")

        return self.__collect.remove(spec_or_id, **kwargs)

    # gridfs method
    def put(self, value, **kwargs):
        """gridfs put method
        """
        if value:
            return self.__gridfs.put(value, **kwargs)

        return None

    def delete(self, _id):
        """gridfs delete method
        """
        return self.__gridfs.delete(self.to_objectid(_id))

    def get(self, _id):
        """gridfs get method
        """
        return self.__gridfs.get(self.to_objectid(_id))

    def read(self, _id):
        """gridfs read method
        """
        return self.__gridfs.get(self.to_objectid(_id)).read()

    def find_by_id(self, _id, column=None):
        """find record by _id
        """
        if isinstance(_id, list) or isinstance(_id, tuple):
            return (self.find_by_id(i, column) for i in _id if i)

        document_id = self.to_objectid(_id)

        if document_id is None:
            return None

        return self.__collect.find_one({'_id': document_id}, column)

    def remove_by_id(self, _id):
        if isinstance(_id, list) or isinstance(_id, tuple):
            return (self.remove_by_id(i) for i in _id)

        return self.__collect.remove({'_id': self.to_objectid(_id)})

    def find_and_modify(self, query=None, update=None, upsert=False, sort=None, full_response=False, **kwargs):
        return  self.__collect.find_and_modify(query=query, update=update, upsert=upsert, sort=sort, full_response=full_response, **kwargs)

    def ensure_index(self, key_or_list, cache_for=300, **kwargs):
        return self.__collect.ensure_index(key_or_list, cache_for=cache_for, **kwargs)

    def find_new_one(self, *args, **kwargs):
        cur = list(self.__collect.find(*args, **kwargs).limit(1).sort('_id', DESCENDING))
        if cur:
            return cur[0]

        return None

    def get_as_column(self, condition=None, column=None, skip=0, limit=0, sort=None):
        if column is None:
            column = self.column

        return self.find(condition, column, skip=skip, limit=limit, sort=sort)

    def get_as_dict(self, condition=None, column=None, skip=0, limit=0, sort=None):
        if column is None:
            column = self.column

        l = self.__collect.find(condition, column, skip=skip, limit=limit, sort=sort)

        as_dict, as_list = {}, []
        for i in l:
            as_dict[unicode(i['_id'])] = i
            as_list.append(i)

        return as_dict, as_list

    def create(self, record=None, **args):
        """init the new record
        function:
            创建一个新的record，并为数据一致性做初始化
        """
        if isinstance(record, list) or isinstance(record, tuple):
            for i in record:
                i = self._valid_record(i)

        if isinstance(record, dict):
            record = self._valid_record(record)

        return self.__collect.insert(record, **args)

    def _valid_record(self, record):
        if not isinstance(record, dict):
            raise Exception("%s record is not dict" % record)

        rset = set(record.keys())
        fset = set(self.field.keys())

        try:
            rset.remove('_id')
        except Exception as e:
            pass

        try:
            fset.remove('_id')
        except Exception as e:
            pass

        if not (fset ^ rset) <= fset:
            raise Exception("record keys is not equal to fields keys %s" % (list((fset ^ rset)-fset)))

        for k, v in self.field.items():
            if k not in record:
                if v[0] is datetime and not v[1]:
                    record[k] = self.datetime()
                    continue

                if v[0] is time and not v[1]:
                    record[k] = self.timestamp()
                    continue

                record[k] = v[1]

        return record

    def inc(self, spec_or_id, key, num=1):
        self.__collect.update(spec_or_id, {'$inc': {key: num}})

    def write_action_call(self, name, *args, **kwargs):
        """
        execute when write action occurs, note: in this method write action must be called asynchronously
        """
        pass

    def read_action_call(self, name, *args, **kwargs):
        """
        execute when read action occurs, note: in this method read action must be called asynchronously
        """
        pass


class BaseModel(BaseBaseModel):
    """全局公共业务方法

    """

    @classmethod
    def create_model(cls, name, field=None):
        """
        dynamic create new model
        :args field table field, if field is None or {}, this model can not use create method
        """
        if field:
            attrs = {'name': name, 'field': field}
        else:
            def create(self, *args, **kwargs):
                raise NotImplementedError()
            attrs = {'name': name, 'field': {'_id': ObjectId()}, 'create': create}

        return type(str(name), (cls, ), attrs)()
