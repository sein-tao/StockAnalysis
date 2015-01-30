# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:06:49 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
from record import TradeRecord, PfEntry
import itertools
import pandas as pd
from parse_tdx_trades import parse_file as parse_tdx_file
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict
#from bisect import bisect #not work for __lt__, __cmp__ comparasion
import util
getter = util.getter

class TabularRecord(TradeRecord):
    flags = (None, "UnRec", "Untreated", "Open", "Closed")
    def __init__(self, rec, flag = None):
        self.record = rec
        self.flag = flag
    def __getattr__(self, attr):
        return getattr(self.record, attr)

    @property
    def flag(self):
        return getattr(self,'_flag', None)
    @flag.setter
    def flag(self, flag):
        if flag in self.flags:
            self._flag = flag
        else:
            raise ValueError("Unrecognized flag")

    @staticmethod
    def selector(code=None, begin=None, end=None):
        return lambda self: \
            (code is None or self.code == code) and \
            (begin is None or self.date >= begin) and \
            (end is None or self.date <= end)

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self.date < other
        else:
            return self.date < other.date

    def __repr__(self):
        return util.tuple_str(self + (self.flag,))

class PfRecords(list):
    _fields = ("code", "date", "BS", "price", "volume",
               'dVol', 'cost', 'fee', 'flag')
    dtype = TabularRecord
    todf = util.todf

HistoryHeader = ("code", "start", "end", "trades", "profit", "fee")
class TradeHistory(namedtuple("TradeHistory", HistoryHeader)):
    def __new__(cls, entry):
        return super(cls, cls).__new__(cls,
            entry.code, entry.start, entry.end,
            entry.tradeNo, entry.profit, entry.fee)
    # sorted by elt.end
    def __lt__(self, other):
        return self.end < other.end

    __repr__ = util.tuple_str

class PfHistory(list):
    _fields = TradeHistory._fields
    dtype = TradeHistory
    todf = util.todf

class PfPosition(dict):
    _fields = ('code', 'start', 'price', 'volume',
                   'cost', 'profit', 'tradeNo', 'fee', 'end')
    dtype = PfEntry
    todf = util.todf


class Portfolio:
    def __init__(self):
        self.records = PfRecords()
        self.history = PfHistory()
        self.position = PfPosition()
        #self.last = dt.min
        None
    def add_trades(self, records):
        recList = map(TabularRecord, records)
        #df['flag'] = None
        recList.sort(key=getter('date'), reverse=True)
        if len(self.records) == 0 or \
            self.records[-1].date < recList[-1].date:
            while len(recList) > 0:
                self.trade(recList.pop())
        else:
            recList.extend(self._pop_affected(recList))
            recList.sort(reverse=True)
            while len(recList) > 0:
                self.trade(recList.pop())
            self.history.sort()
            self.records.sort()

    def _pop_affected(self, recList):
        trace = dict()
        for rec in recList:
            trace[rec.code] = min(rec.date, trace.get(rec.code, datetime.max))
        ih = []
        for i, h in enumerate(self.history):
            if h.code in trace and h.end >= trace[h.code]:
                trace[h.code] = min(trace[h.code], self.history[i].start)
                ih.append(i)
        for i, x in enumerate(ih):
            self.history.pop(x-i)
        for code in trace:
            if code in self.position:
                trace[code] = min(trace[code], self.position.pop(code).start)
        recs = []
        ir = []
        for i, r in enumerate(self.records):
            if r.code in trace and r.date >= trace[r.code]:
                recs.append(self.records[i])
                ir.append(i)
        for i, x in enumerate(ir):
            self.records.pop(x-i)
        return recs

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
            except TypeError:
                rec.flag = 'Untreated'
            self.records.append(rec)
            if entry.closed():
                self.history.append(TradeHistory(entry))
                need_switch = TabularRecord.selector(
                                entry.code, entry.start, entry.end)
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

    pf1 = Portfolio()
    pf1.add_trades(parse_tdx_file(testB))
    pf1.add_trades(parse_tdx_file(testA))
    print "Using Insertion:", pf1


    # performance test
    month = timedelta(days=31)
    def shift(rec,i ):
        rec.date += month * i
        return rec

    def test(cycle):
        pf = Portfolio()
        for i in xrange(cycle):
            pf.add_trades(itertools.imap(
                lambda x:shift(x,i), parse_tdx_file(testC)))
            yield pf
    for i in test(5): print i


