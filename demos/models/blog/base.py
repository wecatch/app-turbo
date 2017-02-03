# -*- coding:utf-8 -*-
from models.base import SqlBaseModel


class Model(SqlBaseModel):

    def __init__(self):
        super(Model, self).__init__(db_name='blog')


Base = Model().Base
