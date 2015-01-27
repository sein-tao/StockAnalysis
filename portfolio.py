# -*- coding: utf-8 -*-
"""
Created on Mon Jan 26 10:06:49 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
from record import TradeRecord, RecordBase, TradeEntry
import itertools
from parse_tdx_trades import parse_file as parse_tdx_file
import pandas as pd
from datetime import datetime as dt
from collections import namedtuple, defaultdict
#portfolio = dict()
#history = []
#els = [] # record of not BS entries

Tablularheader = RecordBase._fields +  ('dVol', 'cost', 'memo')
class TabularRecord(namedtuple('TabularRecord', Tablularheader)):
    Memo = namedtuple("Memo", "fee, est_fee, other_cost")
    @classmethod
    def fromRecord(cls, rec):
        memo = cls.Memo(rec.fee, rec.est_fee, rec.other_cost)
        return cls(*(rec + (rec.dVol, rec.cost, memo)))

path = "D:\\Personal\\Finnance\\Stock\\wt.xls"

data = pd.DataFrame(map(TabularRecord.fromRecord, parse_tdx_file(path)),
                    columns = TabularRecord._fields)


TradeHistory = namedtuple("TradeHistory",
                          ["code", "start", "end", "trades", "profit"])

class Position:
    None
class Portfolio:
    pfEntry = TradeEntry
    def __init__(self):
        self.records = pd.DataFrame(None, columns = TabularRecord._fields)
        self.history = pd.DataFrame(None, columns = TradeEntry._fields)
        self.position = defaultdict(Position)
        self.last = dt.min
        None
    def add_trades(self, records):
        df = pd.DataFrame(map(TabularRecord.fromRecord, parse_tdx_file(path)),
                    columns = TabularRecord._fields)
        #df['hands'] = None
        df.sort('date', inplace=True)
        df.start = df.date.min()
        df.codes = df.code.uniq()
        if df.start > self.last:
            self.records.append()
            self._tr
        else:
            aff = self.records.date >= df.start and self.records.co
        if self.records.shape == 0:
            self.records
        start = df.date.min()

    def trade(self, rec):
        if rec.code in self.position:
            try:
                self.position[rec.code].trade(rec)
                rec.flag = 'Open'
            except TypeError:
                rec.flag = 'Untreated'
            self.records.append(rec)
            if self.position[rec.code].closed():
                #TODO: deal with opened records, add history, and remove position
                self.history.append(TradeHistory())






#i = itertools.imap(TabularRecord.fromRecord, parse_tdx_file(path))
