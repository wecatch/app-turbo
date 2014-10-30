#-*- coding:utf-8 -*-

from datetime import datetime, timedelta

from pymongo import DESCENDING, ASCENDING

from models.user import model as user_model

from helpers import settings


MODEL_SLOTS = ['FoodComment']


class FoodComment(user_model.FoodComment):
        
    _user = user_model.User()

    def format_show_time(self, v, now, start, end):
        diff = now - v
        if diff.seconds < 60:
            s = ('%s%s') % (diff.seconds, '秒前')
        elif diff.seconds >= 60 and diff.seconds < 3600:
            s = ('%s%s') % (diff.seconds / 60, '分钟前')
        elif diff.seconds >= 3600 and (v > start and v < end):
            s = ('%s%s') % ('今天', datetime.strftime(v, format='%H:%M'))
        else:
            s = datetime.strftime(v, format='%Y-%m-%d %H:%M')

        return s
