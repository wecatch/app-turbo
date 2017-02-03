import sys
import os
import random

import tornado.gen

sys.path.insert(0, 
    os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )
)

from models.user.model import Tag


@tornado.gen.coroutine
def init_tag():
    tb_tag = Tag()
    for i in range(10):
        result = yield tb_tag.insert({'name': random.choice('abcdefghjklpoiuytrewq')})
        print(result)


if __name__ == '__main__':
    tornado.ioloop.IOLoop.current().run_sync(lambda: init_tag())

