# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from .setting import DB_SETTING, DRIVERNAME


# mysql blog
blog_engine = create_engine(
    URL(DRIVERNAME, **DB_SETTING), encoding='utf8', echo=True)
DBSession = sessionmaker(bind=blog_engine)
