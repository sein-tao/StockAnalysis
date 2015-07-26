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
from tdx_parser.parse_tdx_day import get_dayline
from dzh_parser import parse_dzh_div
from dump_flow import load_flow
import pandas as pd

cash = Security('0', 'SZ')

def generate_amount_line(flow_file):
    div_file="E:\Stock\dzh365\Download\PWR/full.PWR"
    flow = load_flow(flow_file)
    div = parse_dzh_div(div_file)
    closeLines = dict()
    pf = PF()
    
    start_date, end_date = flow[0].date, flow[-1].date
    dates = pd.date_range(start_date, end_date, freq='B')
    #current = next(dates)
    line = list()
    i = 0
    for day in dates:
        day = day.date()
        deal_div(pf, day, div)
        while i < len(flow) and flow[i].date <= day:
            pf.append(flow[i])
            i += 1
        cash_rest = float(flow[i-1].MRest)
        if abs(cash_rest - pf[cash]) > 0.001:
            print(day, cash_rest, pf[cash])
        amount = calc_amount(pf, day, closeLines)
        line.append(amount)
    return pd.DataFrame(line, index=dates)
        
class PF(defaultdict):
    # add from flow file

    def __init__(self, file = None):
        self.end = datetime.date.min
        self.default_factory = lambda:0
        if file is not None:
            self.add_from_file(file)
        #self.securities = set()
    def append(self, flow):
        # assert(flow.date >= self.end)
        # print(flow.security, flow.quantity)
        self[flow.security] += flow.quantity
        if self[flow.security] == 0:
            del self[flow.security]
        self[cash] += flow.amount
        # fee already include in amount
        #self[cash] -= flow.fee
        self.end = flow.date
            
    def add_from_file(self, file):
        for i, line in enumerate(open(file)):
            if i < 2:
                continue
            self.append(FlowRecord(line))

def get_pad_close(sec, start_date, end_date):
    return get_dayline(sec).Close.resample('B', fill_method='ffill')

def get_price(sec, date, closeLines):
    ## TODO: get amount for new stock befor listed (IPO)
    try:
        if sec == cash:
            return 1.0
        elif sec in closeLines:
                return closeLines[sec][date]
        else:
            closeLines[sec] = get_pad_close(sec, date, datetime.date.today())
            return closeLines[sec][date]
    except KeyError as e:
        raise KeyError("%s %s" % (sec, date))

def calc_amount(pf, date, closeLines):
    return sum(get_price(k, date, closeLines) * v for k,v in pf.items())       

def deal_div(pf, day, div):
    pass

                   
if __name__ == '__main__':
    f = 'test_data/flow2014066-06.xls'
#    pf = PF()
#    pf.add_from_file(f)
#    print(list(zip(pf.keys(),pf.values())))
    #print(pf.end)
    flow_file = 'test_data/test.pickle'
    line = generate_amount_line(flow_file)
    import matplotlib.pyplot as plt
    plt.plot(line.index, line)
    print(line.resample('W-FRI'))