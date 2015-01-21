#-*- coding:utf-8 -*-

from base import *

class User(Model):

    """
    field:
        email: 
        passwd:
    """
    name = 'user'
    field = {
        'email':            (basestring, '')  ,
        'passwd':           (basestring, '')  ,
        'atime':            (datetime, None)  ,
        'ctime':            (time, None)      ,
    }

