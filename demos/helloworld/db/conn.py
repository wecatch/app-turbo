# -*- coding:utf-8 -*-

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pymongo import (
    MongoReplicaSetClient,
    MongoClient,
    read_preferences
)
import gridfs

import setting

mc = MongoClient(host='localhost')

# test
test = mc['test']
test_files = gridfs.GridFS(mc['test_files'])

# egg
food = mc['food']
food_files = gridfs.GridFS(mc['food_files'])

# user
user = mc['user']
user_files = gridfs.GridFS(mc['user_files'])


engine = create_engine('mysql+pymysql://root:@localhost/blog?charset=utf8', encoding='utf8', echo=True)
DBSession = sessionmaker(bind=engine)
