#-*- coding:utf-8 -*-

class ResponseError(Exception):

    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = msg 
        super(ResponseError, self).__init__(msg)

    def __str__(self):
        return '%s %s'%(self.code, self.msg)
