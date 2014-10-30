# -*- coding:utf-8 -*-

from db.conn import (
    test as _test,    
    food as _food,      
    user as _user,   

    test_files as _test_files, 
    food_files as _food_files, 
    user_files as _user_files, 
)

MONGO_DB_MAPPING = {
    'db': {
        'test': _test,
        'food': _food,
        'user': _user,
    },
    'db_file': {
        'test': _test_files,
        'food': _food_files,
        'user': _user_files,
    }
}
