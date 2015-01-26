# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:06:49 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
import trades
import parse_tdx_trades
import collections
portfolio = dict()
history = []
els = [] # record of not BS entries
path = "D:\\Personal\\Finnance\\Stock\\wt.xls"
for record in parse_tdx_trades.parse_file(path):
    if record.direct
    if record.code not in portfolio:
        portfolio[record.code] =  trades.TradeEntry(record)
    else:
        portfolio[record.code].trade(record)

