#-*- coding:utf-8 -*-

import en
import zh_CN

"""
code range describe the response message from the server

0~999: define error code  定义错误码

0: success

1~99: base response error 基础错误 用于调试，正式上线不对外开放
1: '未知错误',
2: 'url 找不到',
3: '缺少必要的参数',
4: '参数类型错误',
5: '无数据'

"""


LANG_MESSAGE = {
    'zh_CN': zh_CN.MESSAGE,
    'en': en.MESSAGE,
}
