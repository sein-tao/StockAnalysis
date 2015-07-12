# -*- coding: utf-8 -*-
"""
Created on Fri Jan 09 16:30:41 2015

@author: xuyu
"""

import pandas as pd
import numpy as np
import pandas.io.data as web
import dateutil.parser

def tdx_datetime_parse(dt):
    dnum, tnum = dt
    (ym, res) = divmod(dnum, 2048)
    y = ym + 2004
    (m, d) = divmod(res, 100)
    h, t = divmod(tnum, 60)
    return pd.datetime(y, m, d, h, t)


def parse_min(path):
    #dtype = np.dtype("i4," + 'i4,' * 4 + 'f4,' + 'i4,' + 'i4,')
    columns = ['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Amount', 'Volume', 'NA']
    formats = ['i2'] * 2 + ['f4'] * 4 + ['f4'] + ['i4'] * 2
    dtype = np.dtype({'names': columns, 'formats': formats})
    #dtype = [i4, (i4, 4), np.float64, i4, i4]
    data = np.fromfile(path, dtype=dtype)
    df = pd.DataFrame(data)
    df.index = df[['Date','Time']].apply(tdx_datetime_parse, axis=1)
    df = df.drop(['Date', 'Time', 'NA'],1)
    return df

if __name__ == '__main__':
    path = "C:\\zd_zszq\\vipdoc\\sz\\fzline\\sz000001.lc5"
    df = parse_min(path)
    print df[:10]
