# -*- coding:utf-8 -*-

from db.conn import (
    test as _test,    
    user as _user,   

    test_files as _test_files, 
    user_files as _user_files, 
)

MONGO_DB_MAPPING = {
    'db': {
        'test': _test,
        'user': _user,
    },
    'db_file': {
        'test': _test_files,
        'user': _user_files,
    }
}
