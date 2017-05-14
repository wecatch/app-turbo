# -*- coding:utf-8 -*-

from .base import *


class User(Model):

    """
    email: user account
    passwd: user account passwd
    atime: added time
    """
    index = [
        tuple([('email', 1)])
    ]
    name = 'user'

    field = {
        'email': (str, ''),
        'passwd': (str, ''),
        'atime': (datetime, None),
    }
