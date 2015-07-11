# -*- coding:utf-8 -*-

import os

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

# user 
user = mc['user']
user_files = gridfs.GridFS(mc['user_files'])
