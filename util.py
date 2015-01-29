# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 20:49:57 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
import pandas as pd
import os.path
import sys
pd.set_option('display.encoding', 'utf8')
workDir = "E:\\home\\StockAnalysis"
def set_display():
    """ IPython display settings,
    Caution: should only call once"""
    import codecs
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)

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



