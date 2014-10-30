#-*- coding:utf-8 -*-

from datetime import datetime, timedelta

from pymongo import DESCENDING, ASCENDING

from models.food import model as food_model
from models.user import model as user_model

from helpers import settings


MODEL_SLOTS = ['Food']


class Food(food_model.Food):

    _user = user_model.User()

    def get_user_create_food(self, uid, skip=0, limit=1, order='new'):
        pass
