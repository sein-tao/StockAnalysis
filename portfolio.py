# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:06:49 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
import trades
import parse_tdx_trades
portfolio = dict()
history = []
path = "D:\\Personal\\Finnance\\Stock\\wt.xls"
for record in parse_tdx_trades.parse_file(path):
    parse_tdx_trades.

