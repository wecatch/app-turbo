#-*- coding:utf-8 -*-

from datetime import datetime, timedelta

from pymongo import DESCENDING, ASCENDING

from models.test import model as test_model

from helpers import settings


MODEL_SLOTS = ['Test']


class Test(test_model.Test):
    
    def hello_test(self):
        self.instance('test.Test').find_one()
