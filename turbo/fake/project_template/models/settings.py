# -*- coding:utf-8 -*-

from db.conn import (
    test as _test,
    test_files as _test_files,
)

MONGO_DB_MAPPING = {
    'db': {
        'test': _test,
    },
    'db_file': {
        'test': _test_files,
    }
}
