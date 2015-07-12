# -*- coding: utf-8 -*-
"""
tdx dividend and right parser
source: http://blog.sina.com.cn/s/blog_c08d065d01015a05.html
  0        1-7     8-11      12         13-16       17-20      21-24         25-28
市场类型  股票代码   日期   信息类型   每10股派几元   配股价  每10股送几股   每10股配几股
Created on Fri Jul 10 21:44:37 2015
@author: xuyu
"""

import pandas as pd
import numpy as np
import pandas.io.data as web
import dateutil.parser

# 

def parse_dr(path):
    #dtype = np.dtype("i4," + 'i4,' * 4 + 'f4,' + 'i4,' + 'i4,')
    columns = ['Market', 'ID', 'Date', 'Type', 'Right', 'RationPrice', 'Div', 'RationQuant' ]
    formats = ['i1', 'c7', 'i4', 'i1', 'f4', ]
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Amount', 'Volume', 'NA']
    formats = ['i4'] + ['i4'] * 4 + ['f4'] + ['i4'] * 2
    dtype = np.dtype({'names': columns, 'formats': formats})
    data = np.fromfile(path, dtype=dtype)
    df = pd.DataFrame(data)
    df.Date = df.Date.astype(str).map(dateutil.parser.parse)
    df = df.set_index('Date')
    
    tmp = df[:10]
    r = tmp.Amount /tmp.Volume / tmp.Close
    type_unit = np.power(10,np.round(np.log10(r))).median()
    df.ix[:,:4] = df.ix[:, :4] * type_unit
    df = df.drop('NA', 1)
    return df

if __name__ == '__main__':
    path = 'E:/Stock/tdx/gbbq/gbbq'
    path = datadir + "\\vipdoc\\sz\\lday\\sz000001.day"
    df = parse_day(path)
    print(df[:10])