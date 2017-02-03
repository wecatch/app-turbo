# -*- coding:utf-8 -*-

from db.mongo_conn import (
    test as _test,
    user as _user,
    test_files as _test_files,
    user_files as _user_files,
    tag as _tag
)

from db.mysql_conn import blog_engine

MONGO_DB_MAPPING = {
    'db': {
        'test': _test,
        'user': _user,
        'tag': _tag,
    },
    'db_file': {
        'test': _test_files,
        'user': _user_files,
    }
}


DB_ENGINE_MAPPING = {
    'blog': blog_engine,
}
