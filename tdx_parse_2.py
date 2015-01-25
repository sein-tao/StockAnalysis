# -*- coding: utf-8 -*-
"""
Not tested yet
Created on Sat Jan 10 16:02:01 2015

@author: xuyu
"""

import pandas as pd
import numpy as np
import pandas.io.data as web
import dateutil.parser

def min_datetime_parse(dt):
    tnum, dnum = dt>>16, dt << 16 >> 16  #little endian
    (ym, res) = divmod(dnum, 2048)
    y = ym + 2004
    (m, d) = divmod(res, 100)
    h, t = divmod(tnum, 60)
    return pd.datetime(y, m, d, h, t)
#dtype = np.dtype("i4," + 'i4,' * 4 + 'f4,' + 'i4,' + 'i4,')
def idx_parse(path, type = 'day'):
    ohlc_type = {'day':'i4', 'min': 'f4'}[type]
    date_parser = {'day': lambda x: dateutil.parser.parse(str(x)),
                   'min': min_datetime_parse}[type]
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Amount', 'Volume', 'NA']
               
    formats = ['i4'] + [ohlc_type] * 4 + ['f4'] + ['i4'] * 2
    dtype = np.dtype({'names': columns, 'formats': formats})
    data = np.fromfile(path, dtype=dtype)
    df = pd.DataFrame(data)
    df.Date = df.Date.apply(date_parser)
    df = df.set_index('Date')
    
    #if np.dtype(ohlc_type
    if type =='day':
        tmp = df[:10]
        r = tmp.Amount /tmp.Volume / tmp.Close
        type_unit = np.power(10,np.round(np.log10(r))).median()
        df.ix[:,:4] = df.ix[:, :4] * type_unit
    df = df.drop('NA', 1)
    return df

if __name__ == '__main__':
    day_path = "C:\\zd_zszq\\vipdoc\\sz\\lday\\sz000001.day"
    df = idx_parse(day_path)
    print df[:10]
    min_path = path = "C:\\zd_zszq\\vipdoc\\sz\\fzline\\sz000001.lc5"
    dfm = idx_parse(min_path, type='min')
    print dfm[:10]
