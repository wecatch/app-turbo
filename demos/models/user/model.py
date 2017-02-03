# -*- coding:utf-8 -*-

from .base import *


class User(Model):

    """
    email: user account
    passwd: user account passwd
    atime: added time
    """
    name = 'user'

    field = {
        'email': (basestring, ''),
        'passwd': (basestring, ''),
        'atime': (datetime, None),
    }


class Tag(MotorModel):

    """
    name: tag name
    atime: added time
    """
    name = 'tag'

    field = {
        'name': (str, ''),
        'atime': (datetime, None),
    }
