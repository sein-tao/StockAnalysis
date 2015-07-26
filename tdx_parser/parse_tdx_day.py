# -*- coding: utf-8 -*-
"""
Created on Fri Jan 09 09:35:10 2015

@author: xuyu
"""

import os
import pandas as pd
import numpy as np
import pandas.io.data as web
import dateutil.parser

datadir = 'E:\Stock\zd_zszq'

def parse_tdx_day(path):
    #dtype = np.dtype("i4," + 'i4,' * 4 + 'f4,' + 'i4,' + 'i4,')
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

def get_dayline(sec, basedir=datadir):
    path = os.path.join(basedir, "vipdoc", sec.market.lower(), 'lday', 
                        sec.symbol().lower() + ".day")
    return parse_tdx_day(path)
    #return day_line.Close.resample('B', fill_method='ffill')

if __name__ == '__main__':
    import sys
    sys.path.append("..")
    from security import Security
    datadir = 'E:\Stock\zd_zszq'
    path = datadir + "\\vipdoc\\sz\\lday\\sz000001.day"
    df = parse_tdx_day(path)
    print(df[:10])
    day = get_dayline(Security('sh000001'), datadir)
    print(day.shape)
    print(day[-10:-1])



