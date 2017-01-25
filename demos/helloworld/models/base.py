# -*- coding:utf-8 -*-

from datetime import datetime
import time

from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# todo change name
import turbo.model
import turbo.util

from .settings import (
    MONGO_DB_MAPPING as _MONGO_DB_MAPPING,
    DB_ENGINE_MAPPING as _DB_ENGINE_MAPPING,
)


class BaseModel(turbo.model.BaseModel):

    _PACKAGE_SPACE = globals()

    def __init__(self, db_name='test'):
        super(BaseModel, self).__init__(db_name, _MONGO_DB_MAPPING)

    def get_count(self, spec=None):
        return self.find(spec=spec).count()


class SqlBaseModel(object):

    def __init__(self, db_name='test'):
        engine = _DB_ENGINE_MAPPING[db_name]
        self.Base = declarative_base(bind=engine)
        self.Session = self.create_session(engine)

    def create_session(self, engine):
        return sessionmaker(bind=engine)