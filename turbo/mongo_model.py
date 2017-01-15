# -*- coding:utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    with_statement,
)

from collections import defaultdict
from datetime import datetime
import functools
import time

from bson.objectid import ObjectId
from turbo.log import model_log
from turbo.util import escape as _es, import_object


def _record(x):
    return defaultdict(lambda: None, x)


def convert_to_record(func):
    """Wrap mongodb record to a dict record with default value None
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
        """Convert single record's values to str
        """
        if kwargs.get('wrapper'):
            return cls._wrapper_to_one_str(value)

        return _es.to_dict_str(value)

    @classmethod
    def to_str(cls, values, callback=None):
        """Convert many records's values to str
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
        """Create new objectid
        """
        return ObjectId()

    _instance = {}

    @classmethod
    def instance(cls, name):
        """Instantiate a model class according to import path
        args:
            name: class import path like `user.User`
        return:
            model instance
        """
        if not cls._instance.get(name):
            model_name = name.split('.')
            ins_name = '.'.join(
                ['models', model_name[0], 'model', model_name[1]])
            cls._instance[name] = cls.import_model(ins_name)()

        return cls._instance[name]

    @classmethod
    def import_model(cls, ins_name):
        """Import model class in models package
        """
        try:
            package_space = getattr(cls, 'package_space')
        except AttributeError:
            raise ValueError('package_space not exist')
        else:
            return import_object(ins_name, package_space)

    @staticmethod
    def default_record():
        """Generate one default record that return empty str when key not exist
        """
        return defaultdict(lambda: '')


def collection_method_call(turbo_connect_ins, name):
    def outwrapper(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if name in turbo_connect_ins._write_operators:
                turbo_connect_ins._model_ins.write_action_call(
                    name, *args, **kwargs)

            if name in turbo_connect_ins._read_operators:
                turbo_connect_ins._model_ins.read_action_call(
                    name, *args, **kwargs)

            return func(*args, **kwargs)

        return wrapper

    return outwrapper


class MongoTurboConnect(object):

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
        """Sub-collection
        """
        return self._collect[name]


class AbstractModel(MixinModel):
    """
    name = None                            mongodb collection name
    field = None                           collection record map
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

    PRIMARY_KEY_TYPE = ObjectId

    def _init(self, db_name, _mongo_db_mapping):
        if _mongo_db_mapping is None:
            raise Exception("db mapping is invalid")
        # databases
        db = _mongo_db_mapping['db']
        # databases file
        db_file = _mongo_db_mapping['db_file']

        # databse name
        if db_name not in db or db.get(db_name, None) is None:
            raise Exception('%s is invalid databse' % db_name)

        # collection name
        if not self.name:
            raise Exception('%s is invalid collection name' % self.name)

        # collection field
        if not self.field or not isinstance(self.field, dict):
            raise Exception('%s is invalid collection field' % self.field)

        # collect as private variable
        collect = getattr(db.get(db_name, object), self.name, None)
        if collect is None:
            raise Exception('%s is invalid collection' % self.name)

        # replace pymongo collect with custome connect
        _collect = MongoTurboConnect(self, collect)

        # gridfs as private variable
        _gridfs = db_file.get(db_name, None)
        if _gridfs is None:
            model_log.info('%s is invalid gridfs' % _gridfs)

        return _collect, _gridfs

    def _to_primary_key(self, _id):
        if self.PRIMARY_KEY_TYPE is ObjectId:
            return self.to_objectid(_id)

        return _id

    def __setitem__(self, k, v):
        setattr(self, k, v)

    def __getitem__(self, k):
        return getattr(self, k)

    def __str__(self):
        if isinstance(self.field, dict):
            return str(self.field)
        return None

    def sub_collection(self, name):
        raise NotImplementedError()

    def find_by_id(self, _id, column=None):
        raise NotImplementedError()

    def remove_by_id(self, _id):
        raise NotImplementedError()

    def find_new_one(self, *args, **kwargs):
        """return latest one record sort by _id
        """
        raise NotImplementedError()

    def get_as_dict(self, condition=None, column=None, skip=0, limit=0, sort=None):
        raise NotImplementedError()

    def _valide_update_document(self, document):
        for opk in document.keys():
            if not opk.startswith('$') or opk not in self._operators:
                raise ValueError('invalid document update operator')

        if not document:
            raise ValueError('empty document update not allowed')

    def _valid_record(self, record):
        if not isinstance(record, dict):
            raise Exception('%s record is not dict' % record)

        rset = set(record.keys())
        fset = set(self.field.keys())
        rset.discard('_id')
        fset.discard('_id')
        if not (fset ^ rset) <= fset:
            raise Exception('record keys is not equal to fields keys %s' % (
                list((fset ^ rset) - fset)))

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
        raise NotImplementedError()

    def put(self, value, **kwargs):
        """gridfs put method
        """
        raise NotImplementedError()

    def delete(self, _id):
        """gridfs delete method
        """
        raise NotImplementedError()

    def get(self, _id):
        """gridfs get method
        """
        raise NotImplementedError()

    def read(self, _id):
        """gridfs read method
        """
        raise NotImplementedError()

    def write_action_call(self, name, *args, **kwargs):
        """Execute when write action occurs, note: in this method write action must be called asynchronously
        """
        pass

    def read_action_call(self, name, *args, **kwargs):
        """Execute when read action occurs, note: in this method read action must be called asynchronously
        """
        pass
