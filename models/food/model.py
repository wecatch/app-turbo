#-*- coding:utf-8 -*-

from base import *


class Food(Model):

    name = 'food'
    field = {
        'name':             (basestring, None)  ,
        'desc':             (basestring, None)  ,
        'cid':              (ObjectId, None)    ,
        'rank':             (int, 0)            ,
        'atime':            (datetime, None)    ,
    }

