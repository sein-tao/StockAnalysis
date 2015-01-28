# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 20:49:57 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
import pandas as pd
import os.path
pd.set_option('display.encoding', 'utf8')
workDir = "E:\\home\\StockAnalysis"

def test_file(base):
    return os.path.join(workDir, "test_data", base)

def tuple_str(self, sep=" "):
        return sep.join(map(str, self))

import pprint
pp = pprint.pprint

def pl(l):
    for i in l:
        print str(i)

def df(namedtuplelist):
    if not isinstance(namedtuplelist, list):
        raise TypeError("namedtuplelist is not a list")
    if len(namedtuplelist) == 0: return []
    return pd.DataFrame(namedtuplelist, columns=namedtuplelist[0]._fields)

def getter(attr):
    return lambda self: self.__getattribute__(attr)

# for pd.DataFrame
def df_addrow(self, row):
    self.loc[self.shape[0],:] = row

#import collections
#def NamedTuple(typename, fieldnames, **kargs):
#    origin = collections.namedtuple(typename, fieldnames)
#    def _str(self, sep=" "):
#        return "%s(%s)" %(self.__class__.__name__, sep.join(map(str, self)))
#    origin.__repr__ = lambda self: _str(self, sep=kargs.get('strsep', " "))
#    @staticmethod
#    def _getter(attr):
#        return lambda self: self.__getattribute__(attr)
#    origin.getter = _getter
#    return origin
