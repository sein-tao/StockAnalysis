# -*- coding: utf-8 -*-
"""
Created on Fri Jan 09 09:35:10 2015

@author: xuyu
"""

import pandas as pd
import numpy as np
import pandas.io.data as web
import dateutil.parser

path = "C:\\zd_zszq\\vipdoc\\sz\\lday\\sz000001.day"
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
#df.f0 = df.f0.astype(str).apply(dateutil.parser.parse)


