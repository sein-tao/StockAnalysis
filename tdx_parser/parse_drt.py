# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:18:01 2015

@author: xuyu
"""
from struct import unpack, unpack_from
root = "/data/e/"
path = root + "home/StockAnalysis/tdx/test_data/gbbq"
f = open(path, 'rb')
size = unpack('I', f.read(4))
while line = f.read(29):
    print unpack_from("4f",line[-16:])
    
