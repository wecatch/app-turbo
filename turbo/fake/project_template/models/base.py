#  -*- coding:utf-8 -*-

import time
from datetime import datetime

import turbo.model
from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

from .settings import MONGO_DB_MAPPING as _MONGO_DB_MAPPING

_PACKAGE_SPACE = globals()


class BaseModel(turbo.model.BaseModel):

    # for import_model work
    package_space = _PACKAGE_SPACE

    def __init__(self, db_name='test'):
        super(BaseModel, self).__init__(db_name, _MONGO_DB_MAPPING)
