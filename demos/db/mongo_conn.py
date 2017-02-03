# -*- coding:utf-8 -*-

import os


from pymongo import (
    MongoReplicaSetClient,
    MongoClient,
    read_preferences
)
from motor import MotorClient

import gridfs


mc = MongoClient(host='localhost')
motor_client = MotorClient(host='localhost')

# test
test = mc['test']
test_files = gridfs.GridFS(mc['test_files'])

# user
user = mc['turbo_app']
user_files = gridfs.GridFS(mc['turbo_app_files'])


tag = motor_client['turbo_app']
