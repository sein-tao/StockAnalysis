# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:06:49 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
from record import TradeRecord, RecordBase, PfEntry
from itertools import imap
import pandas as pd
from parse_tdx_trades import parse_file as parse_tdx_file
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
import util
getter = util.getter

TablularHeader = RecordBase._fields +  ('dVol', 'cost', 'fee')
class TabularRecord(namedtuple('Record', TablularHeader)):
    #Memo = namedtuple("Memo", "fee, est_fee, other_cost")
    def __init__(self,*args):
        super(self.__class__, self).__init__(*args)
        self.flag = None
    @classmethod
    def fromRecord(cls, rec):
        #memo = cls.Memo(rec.fee, rec.est_fee, rec.other_cost)
        return cls(*(rec + (rec.dVol, rec.cost, rec.fee)))
    @staticmethod
    def selector(code=None, begin=None, end=None):
        return lambda self: \
            (code is None or self.code == code) and \
            (begin is None or self.date >= begin) and \
            (end is None or self.date <= end)


    def __repr__(self):
        return util.tuple_str(self + (self.flag,))

class PfRecords(list):
    _fileds = ["code", "date", "BS", "price", "volume",
               'dVol', 'cost', 'fee', 'flag']
    dtype = TradeRecord
    def _tabluar(self, elt):
        return (elt.code, elt.date, elt.BS, elt.price, elt.volume,
                elt.dVol, elt.cost, elt.fee, getattr(elt, 'flag', None))
    def todf(self):
        return pd.DataFrame(map(self._tabluar,self), columns=self._fileds)




HistoryHeader = ["code", "start", "end", "trades", "profit", "fee"]
class TradeHistory(namedtuple("TradeHistory", HistoryHeader)):
    def __new__(cls, entry):
        return super(cls, cls).__new__(cls,
            entry.code, entry.start, entry.end,
            entry.tradeNo, entry.profit, entry.fee)
    __repr__ = util.tuple_str

class PfHistory(list):
    _fields = TradeHistory._fields
    dtype = TradeHistory
    _tabluar = list
    def todf(self):
        return pd.DataFrame(map(self._tabular,self), columns=self._fields)

class PfPosition(dict):
    _fields = ['code', 'start', 'price', 'volume',
                   'cost', 'profit', 'tradeNo', 'fee', 'end']
    dtype = PfEntry
    def _tabular(self,elt):
        return (elt.code, elt.start, elt.price, elt.volume,
                elt.cost, elt.profit, elt.tradeNo, elt.fee, elt.end)
    def todf(self):
        return pd.DataFrame(map(self._tabular, self.itervalues()),
                            columns=self._fields)


class Portfolio:
    def __init__(self):
        self.records = PfRecords()
        self.history = PfHistory()
        self.position = PfPosition()
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
            rec.flag = 'UnRec'
            self.records.append(rec)
        if rec.code in self.position:
            entry = self.position[rec.code]
            try:
                entry.trade(rec)
                rec.flag = 'Open'
            except TypeError as e:
                #print e.message
                rec.flag = 'Untreated'
            self.records.append(rec)
            if entry.closed():
                self.history.append(TradeHistory(entry))
                need_switch = TabularRecord.selector(entry.code, entry.start, entry.end)
                for i in xrange(len(self.records)):
                    if need_switch(self.records[i]):
                        self.records[i].flag = 'Closed'
                self.position.pop(rec.code)
        else:
            try:
                self.position[rec.code] = PfEntry(rec)
                rec.flag = 'Open'
            except TypeError:
                rec.flag = 'Untreated'
            self.records.append(rec)
    def __repr__(self):
        return "%s(Records:%d, History:%d, Position:%d)" % (
            self.__class__.__name__, len(self.records),
            len(self.history), len(self.position))


if __name__ == '__main__':
    path = "D:\\Personal\\Finnance\\Stock\\wt.xls"
    testA = util.test_file("tdxTradeA.xls")
    testB = util.test_file("tdxTradeB.xls")
    testC = util.test_file("tdxTradeBig.xls")

    pf = Portfolio()
    pf.add_trades(parse_tdx_file(testA))
    pf.add_trades(parse_tdx_file(testB))
    print pf


    # performance test
    month = timedelta(days=31)
    def shift(rec,i ):
        l = list(rec)
        l[1] += month * i
        return TradeRecord(*l)
    def test():
        pf = Portfolio()

        for i in xrange(10):
            pf.add_trades(itertools.imap(
                lambda x:shift(x,i), parse_tdx_file(testC)))
            yield pf
    #for i in test(): print i


