# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:00:50 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

from collections import namedtuple
from security import Security, account2market
import datetime as dt
import pandas as pd

def elt_parser(s):
    unquote = s.strip(u'="')
    if unquote == '---':
        return '0'
    else:
        return unquote

class FlowRecord(object):
    Columns = ("Currency", "StockName", "Date", "Price", "Quantity",
    "Amount", "MRest", "TradeID", "TradeName",
    "Fee1", "Fee2", "Fee3", "Fee4", "StockID", "Account")
    Raw = namedtuple("Raw", Columns)
    def __init__(self, line):
        elts = map(elt_parser, line.rstrip().split("\t"))
        self.raw = raw = self.Raw(*elts)
        self.security = Security(raw.StockID,
                                 account2market(raw.Account), raw.StockName)
        self.fee = sum((float(getattr(raw, 'Fee'+str(i))) for i in (1,2,3,4)))
        self.quantity = float(raw.Quantity)
        self.date = dt.datetime.strptime(raw.Date[0:8], "%Y%m%d").date()
        self.amount = float(self.raw.Amount)

    def __getattr__(self, attr):
        return getattr(self.raw, attr)
        #self.security = 'sz'
    
    def __str__(self):
        fields = ['date', 'security', 'quantity', 'amount', 'fee']
        return " ".join(['{}'] * len(fields)).format(
            *(getattr(self, i) for i in fields ))

if __name__ == '__main__':
    f = u'test_data/flow2014066-06.xls'
    file_encode = 'gb2312'
    #df = pd.read_table(f, encoding=file_encode)
    #print(df)
    #df= df.applymap(elt_parser)
    for i, line in enumerate(open(f)):
        if i < 2:
            continue
        rec = FlowRecord(line)
        #print(rec.raw)
        #print(rec.amount, rec.raw.Amount)
        print(rec.security)
        print(rec)
