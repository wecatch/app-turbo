# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import sys
import socket

from bson.objectid import ObjectId

if sys.version_info < (2, 7):
    import unittest2 as unittest  # noqa E401
else:
    import unittest  # noqa E401


def port_is_used(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('localhost', port)) == 0:
        return True

    return False


def get_free_tcp_port():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.bind(('', 0))
    addr, port = tcp.getsockname()
    tcp.close()
    return port


fake_ids = [
    ObjectId('586a01b6ed80083a5087c7d7'),
    ObjectId('586a01b6ed80083a5087c7d8'),
    ObjectId('586a01b6ed80083a5087c7d9'),
    ObjectId('586a01b6ed80083a5087c7da'),
    ObjectId('586a01b6ed80083a5087c7dc'),
    ObjectId('586a01b6ed80083a5087c7dd'),
    ObjectId('586a01b6ed80083a5087c7de'),
    ObjectId('586a01b6ed80083a5087c7df'),
    ObjectId('586a01b6ed80083a5087c7e0'),
    ObjectId('586a01b6ed80083a5087c7e1'),
    ObjectId('586a01b6ed80083a5087c7e2'),
    ObjectId('586a01b6ed80083a5087c7e3'),
    ObjectId('586a01b6ed80083a5087c7e5'),
    ObjectId('586a01b6ed80083a5087c7e6'),
    ObjectId('586a01b6ed80083a5087c7e7'),
    ObjectId('586a01b6ed80083a5087c7e8'),
    ObjectId('586a01b6ed80083a5087c7ea'),
    ObjectId('586a01b6ed80083a5087c7eb'),
    ObjectId('586a01b6ed80083a5087c7ec'),
    ObjectId('586a01b6ed80083a5087c7ed'),
    ObjectId('586a01b6ed80083a5087c7ee'),
    ObjectId('586a01b6ed80083a5087c7ef'),
    ObjectId('586a01b6ed80083a5087c7f0'),
    ObjectId('586a01b6ed80083a5087c7f1'),
    ObjectId('586a01b6ed80083a5087c7f3'),
    ObjectId('586a01b6ed80083a5087c7f4'),
    ObjectId('586a01b6ed80083a5087c7f5'),
    ObjectId('586a01b6ed80083a5087c7f6'),
    ObjectId('586a01b6ed80083a5087c7f8'),
    ObjectId('586a01b6ed80083a5087c7f9'),
    ObjectId('586a01b6ed80083a5087c7fa'),
    ObjectId('586a01b6ed80083a5087c7fb'),
    ObjectId('586a01b6ed80083a5087c7fc'),
    ObjectId('586a01b6ed80083a5087c7fd'),
    ObjectId('586a01b6ed80083a5087c7fe'),
    ObjectId('586a01b6ed80083a5087c7ff'),
    ObjectId('586a01b6ed80083a5087c801'),
    ObjectId('586a01b6ed80083a5087c802'),
    ObjectId('586a01b6ed80083a5087c803'),
    ObjectId('586a01b6ed80083a5087c804'),
    ObjectId('586a01b6ed80083a5087c806'),
    ObjectId('586a01b6ed80083a5087c807'),
    ObjectId('586a01b6ed80083a5087c808')
]

fake_ids_2 = [
    ObjectId('586a09f9ed80083a5087c809'),
    ObjectId('586a09f9ed80083a5087c80a'),
]
