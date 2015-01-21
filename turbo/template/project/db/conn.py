# -*- coding:utf-8 -*-

import os

from pymongo import (
    MongoReplicaSetClient,
    MongoClient,
    read_preferences
)
import gridfs

import setting

if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '__test__')):
    mc = MongoClient(host='localhost')
    mc.read_preference = read_preferences.ReadPreference.SECONDARY
else:
    mc = MongoReplicaSetClient(host=','.join(setting.HOSTS), replicaSet=setting.REPL_SET_NAME)

# test
test = mc['test']
test_files = gridfs.GridFS(mc['test_files'])

# user 
user = mc['user']
user_files = gridfs.GridFS(mc['user_files'])