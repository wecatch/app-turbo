# -*- coding:utf-8 -*-

from datetime import datetime
import time

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

#todo change name
import turbo.model

from settings import MONGO_DB_MAPPING as _MONGO_DB_MAPPING


class MixinModel(turbo.model.MixinModel):
    pass


class BaseModel(turbo.model.BaseModel, MixinModel):

    def __init__(self, db_name='test'):
        super(BaseModel, self).__init__(db_name, _MONGO_DB_MAPPING)

    def get_count(self, spec=None):
        return self.find(spec=spec).count()
