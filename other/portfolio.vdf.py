# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:06:49 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
from record import TradeRecord, RecordBase, PfEntry
import itertools
from parse_tdx_trades import parse_file as parse_tdx_file
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
import util
getter = util.getter
from security import Security
#portfolio = dict()
#history = []
#els = [] # record of not BS entries

TablularHeader = RecordBase._fields +  ('dVol', 'cost', 'fee', 'flag')
class TabularRecord(namedtuple('Record', TablularHeader)):
    #Memo = namedtuple("Memo", "fee, est_fee, other_cost")
    @classmethod
    def fromRecord(cls, rec):
        #memo = cls.Memo(rec.fee, rec.est_fee, rec.other_cost)
        return cls(*(rec + (rec.dVol, rec.cost, rec.fee, None)))


HistoryHeader = ["code", "start", "end", "trades", "profit", "fee"]
class TradeHistory(namedtuple("TradeHistory", HistoryHeader)):
    dtype = [Security, datetime, datetime, int, float, float]
    @classmethod
    def fromEntry(cls,entry):
        return cls(entry.code, entry.start, entry.end,
                   len(entry.records), entry.profit, entry.fee)
    __repr__ = util.tuple_str

class PfRecords(pd.DataFrame):
    dtype = TabularRecord
    def __init__(self, data=None):
        super(self.__class__,self).__init__(data,
                columns=self.__class__.dtype._fields)
    def addrow(self, row, flag):
        self.loc[self.shape[0],:] = row
        if flag is not None:
            self.loc[self.shape[0]-1,'flag'] = flag


class Portfolio:
    def __init__(self):
        self.records = PfRecords()
        self.history = pd.DataFrame(None, columns=TradeHistory._fields)
        self.history.addrow = lambda x: util.df_addrow(self.history, x)
        self.position = dict()
        #self.last = dt.min
        None
    def add_trades(self, records):
        recList = map(TabularRecord.fromRecord, records)
        #df['flag'] = None
        recList.sort(key=getter('date'), reverse=True)
        #df.start = df.date.min()
        #df.codes = df.code.unique()
        #if df.start > self.last:
        while len(recList) > 0:
            self.trade(recList.pop())


#        else:
#            aff = self.records.date >= df.start and self.records.co
#        if self.records.shape[0] == 0:
#            self.records
#        start = df.date.min()

    def trade(self, rec):
        #sys.stdout.write(rec.__repr__().decode('utf8'))
        if rec.BS not in PfEntry.BS_type:
            self.records.addrow(rec, 'UnRec')
            return
        if rec.code in self.position:
            entry = self.position[rec.code]
            try:
                entry.trade(rec)
                flag = 'Open'
            except TypeError as e:
                #print e.message
                flag = 'Untreated'
            self.records.addrow(rec, flag)
            if entry.closed():
                self.history.addrow(TradeHistory.fromEntry(entry))
                rdf = self.records
                rdf.loc[(rdf.code == entry.code) & \
                    (rdf.date >= entry.start) & (rdf.date <= entry.end) & \
                    (rdf.flag == 'Open'), 'flag'] = 'Closed'
                self.position.pop(rec.code)
        else:
            try:
                self.position[rec.code] = PfEntry(rec)
                flag = 'Open'
            except TypeError:
                flag = 'Untreated'
            self.records.addrow(rec, flag)



if __name__ == '__main__':
    path = "D:\\Personal\\Finnance\\Stock\\wt.xls"
    testA = util.test_file("tdxTradeA.xls")
    testB = util.test_file("tdxTradeB.xls")
    testBig = util.test_file("tdxTradeBig.xls")

    #data = pd.DataFrame(map(TabularRecord.fromRecord, parse_tdx_file(testA)),
    #                columns = TabularRecord._fields)
    #data = map(TabularRecord.fromRecord, parse_tdx_file(testA))[:10]

    pf = Portfolio()
    pf.add_trades(parse_tdx_file(testA))
    month = timedelta(days=31)
    def shift(rec):
        l = list(rec)
        l[1] += month
        return TradeRecord(*l)
    def test():
        pf = Portfolio()

        for i in xrange(100):
            pf.add_trades(itertools.imap(shift, parse_tdx_file(testBig)))






#i = itertools.imap(TabularRecord.fromRecord, parse_tdx_file(path))
