#-*- coding:utf-8 -*-

from base import *

class User(Model):

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
    name = 'user'
    field = {
        'name':             (basestring, '')  ,
        'gender':           (basestring, '')  ,
        'addr':             (dict, {'a': '', 'c': '', 'p': ''}),
        'home':             (dict, {'a': '', 'c': '', 'p': ''}),
        'avatar':           (dict, {"25":'', "36":None, "50":None, 'o':None}),
        'phone':            (basestring, '')  ,
        'desc':             (basestring, '')  ,

        'email':            (basestring, '')  ,
        'passwd':           (basestring, '')  ,
        'open':             (dict, {})          ,
        'lastlogin':        (datetime, None)    ,

        'sn':               (int, 0)            ,

        'atime':            (datetime, None)    ,
        'ctime':            (time, None)        ,
    }


class U2food(Model): 
    """
    field:
        uid-> u
        fid-> f
        atime-> t
    """
    name = 'u2food'

    field = {
        'u':               (ObjectId, None)    ,
        'f':               (ObjectId, None)    ,
        't':               (datetime, None)    ,
    }



class FoodComment(Model):

    name = 'food_comment'

    field = {
        'fid':             (ObjectId, None)   ,
        'uid':             (ObjectId, None)   ,
        'up':              (list, [])         ,
        'size':            (int, 0)           ,
        'content':         (basestring, None) ,
        'atime':           (datetime, None)   ,
    }
