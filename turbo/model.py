# -*- coding:utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    with_statement,
)

from bson.objectid import ObjectId
from pymongo import DESCENDING, collection

from turbo import mongo_model
from turbo.log import model_log


class BaseBaseModel(mongo_model.AbstractModel):
    """class implement almost all mongodb collection method
    """

    def __init__(self, db_name='test', _MONGO_DB_MAPPING=None):
        self.__collect, self.__gridfs = super(
            BaseBaseModel, self)._init(db_name, _MONGO_DB_MAPPING)

    def __getattr__(self, k):
        attr = getattr(self.__collect, k)
        if isinstance(attr, collection.Collection):
            raise AttributeError("model object '%s' has not attribute '%s'" % (self.name, k))
        return attr

    def sub_collection(self, name):
        return self.__collect[name]

    def insert(self, doc_or_docs, **kwargs):
        """Insert method
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
        """save method
        """
        return self.__collect.save(to_save, **kwargs)

    def find_one(self, spec_or_id=None, *args, **kwargs):
        """find_one method
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

    @mongo_model.convert_to_record
    def _wrapper_find_one(self, spec_or_id=None, *args, **kwargs):
        """Convert record to a dict that has no key error
        """
        return self.__collect.find_one(spec_or_id, *args, **kwargs)

    @mongo_model.convert_to_record
    def _wrapper_find(self, *args, **kwargs):
        """Convert record to a dict that has no key error
        """
        return self.__collect.find(*args, **kwargs)

    def update(self, filter_, document, multi=False, **kwargs):
        """update method
        """
        for opk in document.keys():
            if not opk.startswith('$') or opk not in self._operators:
                raise ValueError("invalid document update operator")

        if not document:
            raise ValueError("empty document update not allowed")
        
        if multi:
            return self.__collect.update_many(filter_, document, **kwargs)
        else:
            return self.__collect.update_one(filter_, document, **kwargs)
    
    def update_one(self, filter_, document, **kwargs):
        """update method
        """
        for opk in document.keys():
            if not opk.startswith('$') or opk not in self._operators:
                raise ValueError("invalid document update operator")

        if not document:
            raise ValueError("empty document update not allowed")
        
        return self.__collect.update_one(filter_, document, **kwargs)
    
    def update_many(self, filter_, document, **kwargs):
        """update method
        """
        for opk in document.keys():
            if not opk.startswith('$') or opk not in self._operators:
                raise ValueError("invalid document update operator")

        if not document:
            raise ValueError("empty document update not allowed")
        
        return self.__collect.update_one(filter_, document, **kwargs)

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

        if kwargs.pop('multi') is True:
            return self.__collect.delete_many(spec_or_id)
        else:
            return self.__collect.delete_one(spec_or_id)

    def delete_many(self, filter_):
        if isinstance(filter_, dict) and filter_== {}:
            raise ValueError("not allowed remove all documents")

        if filter_ is None:
            raise ValueError("not allowed remove all documents")

        return self.__collect.delete_many(spec_or_id)

    def put(self, value, **kwargs):
        if value:
            return self.__gridfs.put(value, **kwargs)
        return None

    def delete(self, _id):
        return self.__gridfs.delete(self.to_objectid(_id))

    def get(self, _id):
        return self.__gridfs.get(self.to_objectid(_id))

    def read(self, _id):
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

    def find_and_modify(
            self, query=None, update=None, upsert=False, sort=None, full_response=False, **kwargs):
        return self.__collect.find_and_modify(
            query=query, update=update, upsert=upsert, sort=sort, full_response=full_response, **kwargs)

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

        as_list = self.__collect.find(condition, column, skip=skip, limit=limit, sort=sort)

        as_dict, as_list = {}, []
        for i in as_list:
            as_dict[str(i['_id'])] = i
            as_list.append(i)

        return as_dict, as_list

    def create(self, record=None, **args):
        """Init the new record with field dict
        """
        if isinstance(record, list) or isinstance(record, tuple):
            for i in record:
                i = self._valid_record(i)

        if isinstance(record, dict):
            record = self._valid_record(record)

        return self.__collect.insert(record, **args)

    def inc(self, spec_or_id, key, num=1):
        self.__collect.update(spec_or_id, {'$inc': {key: num}})


class BaseModel(BaseBaseModel):
    """Business model
    """

    @classmethod
    def create_model(cls, name, field=None):
        """dynamic create new model
        :args field table field, if field is None or {}, this model can not use create method
        """
        if field:
            attrs = {'name': name, 'field': field}
        else:
            def create(self, *args, **kwargs):
                raise NotImplementedError()
            attrs = {'name': name, 'field': {'_id': ObjectId()}, 'create': create}

        return type(str(name), (cls, ), attrs)()
