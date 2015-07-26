# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 15:50:50 2015

simple portfolio from cash flow
@author: xuyu
"""
import datetime
import os
from collections import defaultdict
from security import Security
from parse_flow import FlowRecord
from tdx_parser.parse_tdx_day import parse_tdx_day


cash = Security('0', 'SZ')
class PF(defaultdict):
    # add from flow file

    def __init__(self, file = None):
        self.end = dt.date.min
        self.default_factory = lambda:0
        if file is not None:
            self.add_from_file(file)
        #self.securities = set()
    def append(self, flow):
        assert(flow.date >= self.end)
        # print(flow.security, flow.quantity)
        self[flow.security] += flow.quantity
        if self[flow.security] == 0:
            del self[flow.security]
        self[cash] += flow.amount
        self[cash] -= flow.fee
        self.end = flow.date
            
    def add_from_file(self, file):
        for i, line in enumerate(open(file)):
            if i < 2:
                continue
            self.append(FlowRecord(line))

                   
if __name__ == '__main__':
    f = 'test_data/flow2014066-06.xls'
    datadir = 'E:\Stock\zd_zszq'
    pf = PF()
    pf.add_from_file(f)
    print(list(zip(pf.keys(),pf.values())))
    #print(pf.end)
    print(get_close_line())