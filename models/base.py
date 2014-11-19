# -*- coding:utf-8 -*-

from datetime import datetime
import time

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

from utils.util import import_object

#todo change name
import db as _db 

from settings import MONGO_DB_MAPPING as _MONGO_DB_MAPPING


class MixinModel(_db.MixinModel):
    
    _instance = {}

    @staticmethod
    def instance(name):
        if not MixinModel._instance.get(name):
            model_name = name.split('.')
            ins_name = '.'.join(['models', model_name[0], 'model', model_name[1]])
            MixinModel._instance[name] = import_object(ins_name)()

        return MixinModel._instance[name]


class BaseModel(_db.BaseModel, MixinModel):

    def __init__(self, db_name='test'):
        super(BaseModel, self).__init__(db_name, _MONGO_DB_MAPPING)

    def get_count(self, spec=None):
        return self.find(spec=spec).count()
