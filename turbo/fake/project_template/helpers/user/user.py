# -*- coding:utf-8 -*-

from datetime import datetime, timedelta

from pymongo import ASCENDING, DESCENDING

from helpers import settings
from models.user import model as user_model

MODEL_SLOTS = ['User']


class User(user_model.User):

    def hello_user(self):
        self.instance('user.User').find_one()
