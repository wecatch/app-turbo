 #-*- coding:utf-8 -*-

import app

prefix = ''

urls = [
    # comments
    ('/(food|other)/([0-9a-f]{24})/comment', app.ListCommentHandler, None, 'comment'),
    ('/food/([0-9a-f]{24})', app.FoodHandler, None, 'food'),
]
