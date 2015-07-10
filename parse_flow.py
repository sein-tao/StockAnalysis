# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 11:00:50 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

from collections import namedtuple
import security

def elt_parser(s):
    return s.strip(u'="')#.encode('utf-8')

class FlowRecord(object):

    Columns = ("Currency", "Name", "Date", "Price", "Amount",
    "MAmount", "MRest", "TradeID", "TradeName",
    "Fee1", "Fee2", "Fee3", "Fee4", "StockID", "Account")
    Raw = namedtuple("Raw", Columns)
    def __init__(self, line):
        elts = map(elt_parser, line.rstrip().split("\t"))
        raw = self.Raw(*elts)
        #self.security = 'sz'
        self.raw = raw
if __name__ == '__main__':
    f = u'test_data/flow2014066-06.xls'
    #df = pd.read_table(f)
    #df= df.applymap(elt_parser)
    for i, line in enumerate(open(f)):
        if i < 2:
            continue
        rec = FlowRecord(line)
        print(rec.raw.Account)