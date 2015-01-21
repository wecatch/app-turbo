# -*- coding: utf-8 -*-
__author__ = 'zhyq'

import os

# app path
CUR_PATH = os.path.dirname(os.path.abspath(__file__))

# app start status
DEBUG = False

if os.path.exists(os.path.join(CUR_PATH, '__test__')):
    DEBUG = True