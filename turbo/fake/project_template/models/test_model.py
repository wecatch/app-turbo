#-*- coding:utf-8 -*-

from base import *

class Test(Model):

    """
    field:
        open = {'qq':{
                'gender':'',
                'nickname':'',
                'uid':'',
                'token':'',
                'avatar':'',
        }, 'sina':{}}
        addr:居住地
        home:家乡
    """
    name = 'test'
    field = {
        # 'field1':           (dict, {})          ,
        # 'field2':           (list, {})          ,
        # 'field3':           (basestring(), {})  ,
        # 'field4':           (objectid, {})      ,
        'status':           (int, 0)            ,
        'ctime':            (datetime, None)    ,
        'utime':            (time, None)        ,
    }

