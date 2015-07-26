# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:00:50 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

from collections import namedtuple
from security import Security, account2market
import datetime as dt


def elt_parser(s):
    unquote = s.strip(u'="')
    if unquote == '---':
        return '0'
    else:
        return unquote

class FlowRecord(object):
    _rawFields = ("Currency", "StockName", "Date", "Price", "Quantity",
    "Amount", "MRest", "TradeID", "TradeName",
    "Fee1", "Fee2", "Fee3", "Fee4", "StockID", "Account")
    _fields = ['date', 'security', 'quantity', 'amount', 'fee']
    Raw = namedtuple("Raw", _rawFields)
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
        return " ".join(['{}'] * len(self._fields)).format(
            *(getattr(self, i) for i in self._fields ))
    #def __repr__(self):
    #    return str(list((i, getattr(self, i)) for i in self._fields))
    __repr__ = __str__

def parse_tdx_flow(file):
    with open(file) as fh:
        fh.readline()
        fh.readline()
        return [FlowRecord(line) for line in fh]
if __name__ == '__main__':
    f = u'test_data/flow2014066-06.xls'
    import pprint
    pprint.pprint(parse_tdx_flow(f))

    
