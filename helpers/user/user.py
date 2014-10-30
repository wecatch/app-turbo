#-*- coding:utf-8 -*-

from datetime import datetime, timedelta

from pymongo import DESCENDING, ASCENDING

from models.user import model as user_model
from models.food import model as food_model

from helpers import settings


MODEL_SLOTS = ['User']


class User(user_model.User):
    pass
