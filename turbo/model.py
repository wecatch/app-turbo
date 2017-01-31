# -*- coding:utf-8 -*-
from __future__ import (
    absolute_import,
    division,
    print_function,
    with_statement,
)
import warnings

from bson.objectid import ObjectId
from pymongo import DESCENDING, collection

from turbo import mongo_model
from turbo.mongo_model import MixinModel  # noqa E401  compatibility for turbo below 0.4.5


class BaseBaseModel(mongo_model.AbstractModel):
    """class implement almost all mongodb collection method
    """

    def __init__(self, db_name='test', _mongo_db_mapping=None):
        self.__collect, self.__gridfs = super(
            BaseBaseModel, self)._init(db_name, _mongo_db_mapping)

    def __getattr__(self, k):
        attr = getattr(self.__collect, k)
        if isinstance(attr, collection.Collection):
            raise AttributeError(
                "model object '%s' has not attribute '%s'" % (self.name, k))
        return attr

    def sub_collection(self, name):
        return self.__collect[name]

    def insert(self, doc_or_docs, **kwargs):
        """Insert method
        """
        check = kwargs.pop('check', True)
        if isinstance(doc_or_docs, dict):
            if check is True:
                doc_or_docs = self._valid_record(doc_or_docs)
            result = self.__collect.insert_one(doc_or_docs, **kwargs)
            return result.inserted_id
        else:
            if check is True:
                for d in doc_or_docs:
                    d = self._valid_record(d)
            result = self.__collect.insert_many(doc_or_docs, **kwargs)
            return result.inserted_ids

    def save(self, to_save, **kwargs):
        """save method
        """
        check = kwargs.pop('check', True)
        if check:
            self._valid_record(to_save)
        if '_id' in to_save:
            self.__collect.replace_one(
                {'_id': to_save['_id']}, to_save, **kwargs)
            return to_save['_id']
        else:
            result = self.__collect.insert_one(to_save, **kwargs)
            return result.inserted_id

    def update(self, filter_, document, multi=False, **kwargs):
        """update method
        """
        self._valide_update_document(document)
        if multi:
            return self.__collect.update_many(filter_, document, **kwargs)
        else:
            return self.__collect.update_one(filter_, document, **kwargs)

    def remove(self, filter_=None, **kwargs):
        """collection remove method
        warning:
            if you want to remove all documents,
            you must override _remove_all method to make sure
            you understand the result what you do
        """
        if isinstance(filter_, dict) and filter_ == {}:
            raise ValueError('not allowed remove all documents')

        if filter_ is None:
            raise ValueError('not allowed remove all documents')

        if kwargs.pop('multi', False) is True:
            return self.__collect.delete_many(filter_, **kwargs)
        else:
            return self.__collect.delete_one(filter_, **kwargs)

    def insert_one(self, doc_or_docs, **kwargs):
        """Insert method
        """
        check = kwargs.pop('check', True)
        if check is True:
            self._valid_record(doc_or_docs)

        return self.__collect.insert_one(doc_or_docs, **kwargs)

    def insert_many(self, doc_or_docs, **kwargs):
        """Insert method
        """
        check = kwargs.pop('check', True)
        if check is True:
            for i in doc_or_docs:
                i = self._valid_record(i)

        return self.__collect.insert_many(doc_or_docs, **kwargs)

    def find_one(self, filter_=None, *args, **kwargs):
        """find_one method
        """
        wrapper = kwargs.pop('wrapper', False)
        if wrapper is True:
            return self._wrapper_find_one(filter_, *args, **kwargs)

        return self.__collect.find_one(filter_, *args, **kwargs)

    def find(self, *args, **kwargs):
        """collection find method

        """
        wrapper = kwargs.pop('wrapper', False)
        if wrapper is True:
            return self._wrapper_find(*args, **kwargs)

        return self.__collect.find(*args, **kwargs)

    @mongo_model.convert_to_record
    def _wrapper_find_one(self, filter_=None, *args, **kwargs):
        """Convert record to a dict that has no key error
        """
        return self.__collect.find_one(filter_, *args, **kwargs)

    @mongo_model.convert_to_record
    def _wrapper_find(self, *args, **kwargs):
        """Convert record to a dict that has no key error
        """
        return self.__collect.find(*args, **kwargs)

    def update_one(self, filter_, document, **kwargs):
        """update method
        """
        self._valide_update_document(document)
        return self.__collect.update_one(filter_, document, **kwargs)

    def update_many(self, filter_, document, **kwargs):
        self._valide_update_document(document)
        return self.__collect.update_many(filter_, document, **kwargs)

    def delete_many(self, filter_):
        if isinstance(filter_, dict) and filter_ == {}:
            raise ValueError('not allowed remove all documents')

        if filter_ is None:
            raise ValueError('not allowed remove all documents')

        return self.__collect.delete_many(filter_)

    def find_by_id(self, _id, projection=None):
        """find record by _id
        """
        if isinstance(_id, list) or isinstance(_id, tuple):
            return list(self.__collect.find(
                {'_id': {'$in': [self._to_primary_key(i) for i in _id]}}, projection))

        document_id = self._to_primary_key(_id)

        if document_id is None:
            return None

        return self.__collect.find_one({'_id': document_id}, projection)

    def remove_by_id(self, _id):
        if isinstance(_id, list) or isinstance(_id, tuple):
            return self.__collect.delete_many(
                {'_id': {'$in': [self._to_primary_key(i) for i in _id]}})

        return self.__collect.remove({'_id': self._to_primary_key(_id)})

    def find_new_one(self, *args, **kwargs):
        cur = list(self.__collect.find(
            *args, **kwargs).limit(1).sort('_id', DESCENDING))
        if cur:
            return cur[0]

        return None

    def get_as_dict(self, condition=None, projection=None, skip=0, limit=0, sort=None):
        as_list = self.__collect.find(
            condition, projection, skip=skip, limit=limit, sort=sort)

        as_dict, as_list = {}, []
        for i in as_list:
            as_dict[i['_id']] = i
            as_list.append(i)

        return as_dict, as_list

    def inc(self, filter_, key, num=1, multi=False):
        if multi:
            self.__collect.update_many(filter_, {'$inc': {key: num}})
        else:
            self.__collect.update_one(filter_, {'$inc': {key: num}})

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

    def create(self, *args, **kwargs):
        warnings.warn("create is deprecated. Use insert or insert_one "
                      "instead", DeprecationWarning, stacklevel=2)
        return self.insert(*args, **kwargs)


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
            attrs = {'name': name, 'field': {'_id': ObjectId()}}

        return type(str(name), (cls, ), attrs)()
