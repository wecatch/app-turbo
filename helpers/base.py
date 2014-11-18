#-*- coding:utf-8 -*-
from pymongo import DESCENDING, ASCENDING

from settings import COLLECTION_PREFIX as _PREFIX

class Helper(dict):

    __prefix = _PREFIX

    def __setitem__(self, k, v):
        return super(Helper, self).setdefault('%s%s'%(self.__prefix, self.__convert_name(k)), v)

    def __getattr__(self, name):
        collect = self.get(name, None)
        if collect is None:
            raise Exception("%s model is not found" % name)

        return collect

    def __convert_name(self, name):
        as_list = []
        length = len(name)
        for index, i in enumerate(name):
            if index !=0 and index != length-1 and i.isupper():
                as_list.append('_%s'%i.lower())
            else:
                as_list.append(i.lower())

        return ''.join(as_list)
