#-*- coding:utf-8 -*-


class ResponseMsg(Exception):

    def __init__(self, code='', msg=''):
        self.code = code
        self.msg = msg 
        super(ResponseMsg, self).__init__(msg)

    def __str__(self):
        return '%s %s'%(self.code, self.msg)


class ResponseError(ResponseMsg):

    def __init__(self, code='', msg=''):
        super(ResponseError, self).__init__(code, msg)
