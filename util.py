# -*- coding: utf-8 -*-
"""
Created on Tue Jan 27 20:49:57 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
import pandas as pd
import os.path
import sys
#pd.set_option('display.encoding', 'utf8')
#workDir = "E:\\home\\StockAnalysis"
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

#def pl(l):
#    for i in l:
#        print str(i)

def df(namedtuplelist):
    if not isinstance(namedtuplelist, list):
        raise TypeError("namedtuplelist is not a list")
    if len(namedtuplelist) == 0: return []
    return pd.DataFrame(namedtuplelist, columns=namedtuplelist[0]._fields)

def getter(attr):
    return lambda self: getattr(self, attr)

#def getattrs(attrs):
#    return lambda elt: map(lambda x:getattr(elt, x), attrs)

def todf(self, fields = None):
    if fields is None:
        fields = self._fields
    if isinstance(self, dict):
        it = self.itervalues()
    else:
        it = iter(self)
    gets = lambda elt:map(lambda x:getattr(elt, x), fields)
    return pd.DataFrame(map(gets,it), columns=fields)




class Enum(set):
    def __get__(self, name):
        if name in self:
            return name
        raise AttributeError("%s in not in %s" % (name, type(self)))

