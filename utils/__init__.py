import sys
import os

def _app_path_load(dir_level_num=3):
    app_root_path = os.path.abspath(__file__)
    for i in range(0, dir_level_num):
        app_root_path = os.path.dirname(app_root_path)
    
    sys.path.append(app_root_path)


_app_path_load(2)
