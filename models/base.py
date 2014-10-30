# -*- coding:utf-8 -*-

from datetime import datetime
import time

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

import db as _db 

from settings import MONGO_DB_MAPPING as _MONGO_DB_MAPPING

class BaseModel(_db.BaseModel):

    def __init__(self, db_name='test'):
        super(BaseModel, self).__init__(db_name, _MONGO_DB_MAPPING)
