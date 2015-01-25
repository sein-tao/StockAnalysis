# -*- coding: utf-8 -*-
"""
Created on Tue Jan 20 10:23:36 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""
import numpy as np
import pandas as pd

class TradeRecord:
    def __init__(self, code, direct, price, amount, date,
                 fee=None, other_cost = 0):
        self.code = code
        self.direct_type = direct
        self.price = price
        self.amount = self.directFactor(direct) * amount
        self.date = date
        self.est_fee = fee is None
        self.fee = self.estFee() if self.est_fee else fee
        self.other_cost = other_cost

        self.cap = self.amount * self.price
        self.cost = self.cap + self.fee + self.other_cost

    def estFee(self):
        None
    def directFactor(self, direct):
        if direct == 'B' :
            return 1
        elif direct == 'S':
            return -1



class TradeEntry:
    def __init__(self, record):
        if record.direct != 'B':
            raise TypeError("only Buy records can init %s" % self.__class__.__name__)
        self.code = record.code
        self.init = record.date
        self.close = None
        self.records = []
        self.trade(record)

    def trade(self, record):
        self.records.append(record)
        self.amount += record.direct * record.amount
        self.cost += record.cost()
        self.fee += record.fee()
        if self.amount == 0:
            self.close = record.date
            self.profit = -1 * self.cost
        else:
            self.buy = self.cost / self.amount

    def closed(self):
        return self.close is not None

    def __str__(self):
        pref = self.__class__.__name__ + ": %s, " % self.code
        if self.closed():
            rec = "%s TO %s, %d Trades, Earn %.2f" %  (
                self.init, self.close, len(self.records), self.profit)
        else:
            rec = "%s TO %s, %d Trades, Current: %d @ %.3f" % (
                self.init, "NOW", len(self.records), self.amount, self.buy)
        return pref + rec





