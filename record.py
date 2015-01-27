# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 10:23:36 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

class TradeRecord:
    def __init__(self, date, code, BS, price, volume,
                 fee=None, other_cost = 0):
        """ Trade Record init
        :parm code: Security, security for trade
        :parm BS: string, Buy or Sell
        :parm price: float
        :parm volume: int
        :parm date: datetime:datetime, date of trade,
        :parm fee: float
        :parm other_cost: float
        """
        self.code = code
        self.BS = BS
        self.price = price
        self.volume = volume
        self.vol_delta = self.direct() * volume
        self.date = date
        self.est_fee = fee is None
        self.fee = self.estFee() if self.est_fee else fee
        self.other_cost = other_cost

        self.cap =  self.vol_delta * self.price
        self.cost = self.cap + self.fee + self.other_cost

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


    from_tdx = None






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
        self.volume += record.vol_delta
        self.cost += record.cost
        self.fee += record.fee
        if record.BS == 'B':
            self.buy = self.cost / self.volume
        elif record.BS == 'S':
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
