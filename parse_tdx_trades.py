# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 20:23:32 2015

@author: Sein Tao
@email: sein.tao@gmail.com
"""

import io
import pandas as pd
import numpy as np
from datetime import datetime
import security
import trades
import collections
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')
file_encode = 'gb2312'
codec = 'utf8'
datefmt, timefmt = "%Y%m%d","%H:%M:%S"
bs_state = {u'买入'.encode(codec): 'B', u'卖出'.encode(codec): 'S'}
def get_market(account):
    if account[0] == 'A':
        return 'SS'
    elif account[0] == '0':
        return 'SZ'
#证券名称,成交日期,成交时间,买卖标志,成交价格,成交数量,成交金额,成交编号,委托编号,证券代码,股东代码
header = ['Name', 'Date', 'Time', 'BS', 'Price', 'Volume', 'Amount',
          'TradeNo','OrderNo', 'Code', 'Account']
RawRecord = collections.namedtuple('RawRecord', header)
def parse_record(line):
    cols = (x.strip("=\"") for x in line.encode(codec).rstrip().split("\t"))
    raw = RawRecord(*cols)
    date = datetime.strptime(raw.Date + raw.Time, datefmt+timefmt)
    BS = bs_state.get(raw.BS, raw.BS)
    code = security.Security(raw.Code, raw.Name, get_market(raw.Account))
    record = trades.TradeRecord(code,BS,float(raw.Price), int(raw.Volume), date)
    return record


def parse_file(path):
    f = io.open(path, 'r',encoding=file_encode)
    f.readline() # header line
    records = (parse_record(line) for line in f.readlines())
    return records

if __name__ == '__main__':
    path = "D:\\Personal\\Finnance\\Stock\\wt.xls"
    for record in parse_file(path):
        print record


