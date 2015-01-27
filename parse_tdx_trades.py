# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 20:23:32 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

import io
import pandas as pd
import numpy as np
from datetime import datetime as dt
import security
import trades
import collections
import sys
pd.set_option('display.encoding', 'utf8')


file_encode = 'gb2312'
codec = 'utf8'
datefmt, timefmt = "%Y%m%d","%H:%M:%S"
bs_state = {u'买入': 'Buy', u'卖出': 'Sell'}
def get_market(account):
    if account[0] == 'A':
        return 'SS'
    elif account[0] == '0':
        return 'SZ'
#证券名称,成交日期,成交时间,买卖标志,成交价格,成交数量,成交金额,成交编号,委托编号,证券代码,股东代码
RawHeader = ['Name', 'Date', 'Time', 'BS', 'Price', 'Volume', 'Amount',
          'TradeNo','OrderNo', 'Code', 'Account']
RawRecord = collections.namedtuple('RawRecord', RawHeader)
RawRecord.toRecord = _toRecord
def _toRecord(self):
    date = dt.combine(dt.strptime(self.Date,datefmt).date(),
            dt.strptime(self.Time,timefmt).time())
    BS = bs_state.get(self.BS, self.BS)
    #market = get_market(self.Account)
    code = security.Security(self.Code, self.Name, get_market(self.Account))
    return [code, date, BS, self.Price, self.Volume]

def _raw(self):
    return self

header = ['Code', 'Date', 'BS', 'Price', 'Volume']


def _parse_file(path):
    with io.open(path, 'r') as f:
        f.readline() # header line
        for line in f.readlines():
            cols = (x.strip("=\"") for x in line.rstrip().split("\t"))
            yield RawRecord(*cols).toRecord()


def parse_file(path):
    data = pd.DataFrame(_parse_file(path), columns = header)
    return data

if __name__ == '__main__':
    path = "D:\\Personal\\Finnance\\Stock\\wt.xls"
    data = parse_file(path)

