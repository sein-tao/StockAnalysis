# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 10:23:36 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

class TradeRecord:
    def __init__(self, code, direct, price, volume, date,
                 fee=None, other_cost = 0):
        """ Trade Record init
        :parm code: Security, security for trade
        :parm direct: string "B" or "S", Buy or Sell
        :parm price: float
        :parm volume: int
        :parm date: datetime:datetime, date of trade,
        :parm fee: float
        :parm other_cost: float
        """
        self.code = code
        self.direct = direct
        self.price = price
        self.volume = volume
        self.vol_delta = self.directFactor() * volume
        self.date = date
        self.est_fee = fee is None
        self.fee = self.estFee() if self.est_fee else fee
        self.other_cost = other_cost

        self.cap =  self.vol_delta * self.price
        self.cost = self.cap + self.fee + self.other_cost

    def estFee(self):
        return 0

    def directFactor(self):
        if self.direct == 'B' :
            return 1
        elif self.direct == 'S':
            return -1
        else:
            return 0

    def __str__(self):
        return "%s %s: %s%d@%.3f" % (self.date, self.code,
                    self.direct, self.volume, self.price)




class TradeEntry:
    def __init__(self, record):
        if record.direct != 'B':
            raise TypeError("only Buy records can init %s" % self.__class__.__name__)
        self.code = record.code
        self.init = record.date.date()
        self.close = None
        self.records = []
        self.profit = 0
        self.trade(record)

    def trade(self, record):
        assert record.code == self.code, "Record code do not match"
        self.records.append(record)
        self.volume += record.vol_delta
        self.cost += record.cost
        self.fee += record.fee
        if record.direct == 'B':
            self.buy = self.cost / self.volume
        elif record.direct == 'S':
            rest_value = self.buy * self.volume
            self.profit += rest_value - self.cost
            self.cost = rest_value

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
