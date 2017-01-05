# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import sys
import socket

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest


def port_is_used(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(('localhost', port)) == 0:
        return True

    return False
