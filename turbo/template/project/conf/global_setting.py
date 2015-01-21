# -*- coding: utf-8 -*-
__author__ = 'zhyq'

import os

# app path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# app start status
DEBUG = False

if os.path.exists(os.path.join(BASE_DIR, '__test__')):
    DEBUG = True