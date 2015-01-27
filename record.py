# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 10:23:36 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
from collections import namedtuple

RecordBase = namedtuple("RecordBase", ["code", "date", "BS", "price", "volume"])
class TradeRecord(RecordBase):
    def __init__(self, code, date, BS, price, volume,
                 fee=None, other_cost = 0):
        """ Trade Record init
        :parm code: Security, security for trade
        :parm date: datetime:datetime, date of trade,
        :parm BS: string, Buy or Sell
        :parm price: float
        :parm volume: int
        :parm fee: float
        :parm other_cost: float
        """
        super(self.__class__, self).__init__(code, date, BS, price, volume)
        self.dVol = self.direct() * self.volume
        self.est_fee = fee is None
        self.fee = self.estFee() if self.est_fee else fee
        self.other_cost = other_cost

        self.cap =  self.dVol * self.price
        self.cost = (self.cap + self.fee + self.other_cost) * -1

    def estFee(self):
        return 0

    def direct(self):
        if self.BS == 'B' :
            return 1
        elif self.BS == 'S':
            return -1
        else:
            return 0

    def __str__(self):
        return "%s %s: %s%d@%.3f" % (self.date, self.code,
                    self.BS, self.volume, self.price)




class TradeEntry:
    def __init__(self, record):
        if record.BS != 'B':
            raise TypeError("only Buy records can init %s" % self.__class__.__name__)
        self.code = record.code
        self.init = record.date.date()
        self.close = None
        self.records = []
        self.profit = 0
        self.volume = 0
        self.cost = 0
        self.fee = 0
        self.trade(record)

    def trade(self, record):
        assert record.code == self.code, "Record code do not match"
        self.records.append(record)
        self.volume += record.dVol
        self.cost += record.cost
        self.fee += record.fee
        if record.BS == 'B':
            self.buy = self.cost / self.volume
        elif record.BS == 'S':
            rest_value = self.buy * self.volume
            self.profit += rest_value - self.cost
            self.cost = rest_value
        else:
            raise TypeError("Unable to handle trade type")

        if self.volume == 0:
            self.close = record.date.date()


    def closed(self):
        return self.close is not None

    def __str__(self):
        pref = self.__class__.__name__ + ": %s, " % self.code

        rec = "%s TO %s, %d Trades, Earned %.2f, " %  (
            self.init, self.close, len(self.records), self.profit)
        pos = "Closed." if self.closed() else \
                "Current: %d @ %.3f" % (self.volume, self.buy)
        return pref + rec + pos
